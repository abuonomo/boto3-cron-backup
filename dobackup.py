import boto3
import tarfile
import os
import plac
import time
import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

AWS_PROFILE = "default"
BUCKET_NAME = os.environ['BUCKET_NAME']
BACKUP_NAME = os.environ['BACKUP_NAME']


@plac.annotations(
    backup_interval=plac.Annotation("weekly, monthly, or yearly", "positional", type=str),
)
def main(backup_interval="weekly"):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    backup_fileout_name = f'{BACKUP_NAME}-{timestamp}.tar.gz'

    if backup_interval == "weekly":
        copies = 4
    elif backup_interval == "monthly":
        copies = 12
    elif backup_interval == "yearly":
        copies = 10
    else:
        LOG.error(f'backup_interval "{backup_interval}" is invalid. Choose "weekly", "monthly", or "yearly"')
        exit()

    out_tar_local = f'/tmp/{backup_fileout_name}'
    with tarfile.open(out_tar_local, 'w') as tar:
        tar.add('/data/', recursive=True)

    LOG.info(f'Getting aws s3 sessions.')
    session = boto3.Session()

    LOG.info(f'Using bucket {BUCKET_NAME}')
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    key = f'backups/{BACKUP_NAME}/{backup_interval}'
    out_tar_remote = f'{key}/{backup_fileout_name}'  # where in s3 bucket to dump the tar

    LOG.info(f'Uploading {backup_interval} backups.')
    bucket.upload_file(out_tar_local, out_tar_remote)

    LOG.info(f'Removing the local {out_tar_local}.')
    os.remove(out_tar_local)

    objects = [obj for obj in bucket.objects.filter(Prefix=key)]
    # order present backups from newest to oldest
    objects.sort(key=lambda x: x.last_modified, reverse=True)

    LOG.info(f'Reducing to {str(copies)} backups by removing old backups.')
    for obj in objects[copies:]:
        # Assuming that all backups are in top level "backups" folder.
        assert 'backups' == obj.key[0:7], LOG.critical("You may be deleting non-backup data! Abort!")
        obj.delete()

    LOG.info('Done.')


if __name__ == "__main__":
    plac.call(main)

