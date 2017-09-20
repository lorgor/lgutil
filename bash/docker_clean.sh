#!/bin/sh -x
#
# Do some docker cleanup
#
#

echo "######################################################################"
echo "# If you see msgs like 'docker xx requires at least 1 argument(s).'  #"
echo "# then that particular resource has nothing to clean.                #"
echo '######################################################################'
echo
echo

docker ps -a | grep Exited | awk '{print $1}' | xargs docker rm

docker volume rm $(docker volume ls -f dangling=true -q)

# 160726 Consider using docker-compose down -v instead. This will remove named volumes
# that should persist.

docker rmi $(docker images -f "dangling=true" -q)