# Backup to S3 using boto3

Make weekly, monthly, and yearly backups to s3 of a given docker volume.

Included docker-compose file shows an example of how to run. 
Of course, note that if you run this service with the compose file, it will be in its own network and will, therefore, (by default) be unable to access volumes from other networks. 
You could either add this service (in docker compose) to the docker-compose file with the volume you want to snapshot, or use the external volumes command in the extant one. 

The example given simply backs up a local directory called tmp to the given s3 bucket. 

You must go the the env.credentials file and change the values therein to the correct values for your s3 bucket. 
Then change the name of env.example to .env
```
mv env.example .env
```
Make sure you don't commit your API keys!
