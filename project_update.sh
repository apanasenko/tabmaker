#!/bin/bash
# as sudo

cd <path_to_project>

echo -n "Would you like to do 'git pull' (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   git checkout master
   if ! git pull origin master; then
      echo "Pull conflicts!"
      exit
   fi
   git checkout <prod_branch>
   if ! git rebase master; then
      echo "Rebase conflicts!"
      exit
   fi
fi

# start env
source <pant_to_env>/bin/activate

python manage.py collectstatic

echo -n "Would you like to do migrate (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   python manage.py migrate
fi

deactivate
# end env

echo -n "Would you like restart server (\"y\" or \"n\", default: \"n\"): "
read answer
if [ "$answer" = "y" ]; then
   service nginx restart
   supervisorctl restart tabmaker
fi

echo "Done!"
