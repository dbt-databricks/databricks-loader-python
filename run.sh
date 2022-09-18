#!/bin/sh

cd postgresql/db-migrate && db-migrate up -v
cd ../..

# use supervisor to start module sbin
supervisord -c /var/task/dataloader/supervisord.conf

# use supervisord
if [ $? -eq 0 ]
then
    echo "supervisorctl restart all"
    supervisorctl -c /var/task/dataloader/supervisord.conf restart all

# not use supervisord
else
    echo "not use supervisord"
fi
