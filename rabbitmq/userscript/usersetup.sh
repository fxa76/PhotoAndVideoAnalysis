#!/usr/bin/env bash
set -e

(
count=0;
# Execute list_users until service is up and running
until timeout 5 rabbitmqctl list_users >/dev/null 2>/dev/null || (( count++ >= 60 )); do sleep 1; done;
if rabbitmqctl list_users | grep guest > /dev/null
then
   # Delete default user and create new users
   rabbitmqctl delete_user guest

   rabbitmqctl add_user admin ${RABBITMQ_ADMIN_PASSWORD}
   rabbitmqctl set_user_tags admin administrator
   rabbitmqctl set_permissions -p / admin  ".*" ".*" ".*"

   rabbitmqctl add_user app ${RABBITMQ_APP_PASSWORD}
   rabbitmqctl set_permissions -p / app  ".*" ".*" ".*"

   #application set_permissions
   rabbitmqctl add_user mime_engine 908790172834598012374
   rabbitmqctl add_vhost mime_engine_vhost
   rabbitmqctl set_permissions -p / mime_engine ".*" ".*" ".*"

   echo "setup completed"
else
   echo "already setup"
fi
) &

# Call original entrypoint
exec docker-entrypoint.sh rabbitmq-server $@
