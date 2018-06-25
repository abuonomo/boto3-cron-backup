#!/bin/sh
echo "creating crontab"
if [[ "$CRON_WEEKLY_SCHEDULE" != "" ]]; then
    echo -e "$CRON_WEEKLY_SCHEDULE python /dobackup.py weekly\n" >> /etc/crontabs/root
fi
if [[ "$CRON_MONTHLY_SCHEDULE" != "" ]]; then
    echo -e "$CRON_MONTHLY_SCHEDULE python /dobackup.py monthly\n" >> /etc/crontabs/root
fi
if [[ "$CRON_YEARLY_SCHEDULE" != "" ]]; then
    echo -e "$CRON_YEARLY_SCHEDULE python /dobackup.py yearly\n" >> /etc/crontabs/root
fi
echo "starting crond"
crond -f
