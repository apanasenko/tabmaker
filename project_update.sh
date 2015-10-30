#!/bin/bash

echo -n "Would you like to do 'git pull' (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   git checkout master
   if ! git pull origin master; then
      echo "Pull conflicts!"
      exit
   fi
   git checkout google_code
   if ! git rebase master; then
      echo "Rebase conflicts!"
      exit
   fi
fi

echo -n "Would you like to do collect static (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   source /home/ubuntu/tabmaker_env/bin/activate
   python manage.py collectstatic
   deactivate
fi

echo -n "Would you like to do migrate (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   source /home/ubuntu/tabmaker_env/bin/activate
   python manage.py migrate
   deactivate
fi

echo -n "Would you like restart server (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   sudo service nginx restart
   sudo supervisorctl restart tabmaker
fi

echo "Done!"
