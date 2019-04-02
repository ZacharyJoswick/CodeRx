#!/bin/bash

#Colored output function
cecho(){
    RED="\033[0;31m"
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[1;34m'
    NC='\033[0m' # No Color
    
    printf "${!1}${2} ${NC}\n"
}

check_if_docker_installed()
{
    if [ -x "$(command -v docker)" ]; then
        cecho "GREEN" "Docker installed"
        echo
    else
        cecho "RED" "Docker not installed, correct this before proceeding"
        exit 1
    fi
    
}

check_if_node_modules_exists()
{
    if [ -d ./components/application/CodeRx/static/node_modules ]
    then
        cecho "GREEN" "Node Modules already present, skipping."
        echo
    else
        cecho "YELLOW" "Node_modules folder not present, using docker to install"
        
        docker run -v $(pwd)/components/application/CodeRx/static:/code node /bin/bash -c "cd /code; npm install"
        if [ $? -eq 0 ]; then
            echo
            cecho "GREEN" "Node Modules installed correctly"
            echo
        else
            echo
            cecho "RED" "ERROR while installing node modules"
            echo
            exit 1
        fi
    fi
}

check_if_database_volume_created()
{
    volume="$(docker volume ls -q -f name=dbdata)"
    volume_name="dbdata"
    if [ $volume == $volume_name ]; then
        cecho "GREEN" "Database volume exists, not doing anything"
        echo
    else
        cecho "YELLOW" "Database volume does not exist, creating it"
        echo
        docker volume create dbdata
    fi
}

case "$1" in
    "setup")
        echo
        cecho "BLUE" "Running setup command"
        echo
        check_if_docker_installed
        check_if_node_modules_exists
        check_if_database_volume_created
    ;;
    "migrate")
        echo
        cecho "BLUE" "Performing database migration"
        
    ;;
    "start")
        echo
        cecho "GREEN" "Starting system"
        docker-compose up -d
    ;;
    "stop")
        echo
        cecho "YELLOW" "Stopping system"
        docker-compose down
    ;;
    "build")
        echo
        cecho "BLUE" "Building Containers"
        docker-compose build
    ;;
    "migrate")
        echo
        cecho "GREEN" "migrating and updating database"
        docker run -it /bin/bash -c "flask db migrate -d ./CodeRx/migrations && flask db upgrade -d ./CodeRx/migrations"
    ;;
    "r")
        cecho "GREEN" "restarting probably because you fucked something up"
        docker-compose down
        docker-compose build
        docker-compose up -d
    ;;
    *)
        cecho "RED" "Error, Command $1 unrecognized"
        echo
        echo "Valid Commands are:"
        echo
        cecho "BLUE" "setup"
        echo " - performs initial setup. Only needs to be run once"
        echo
        cecho "BLUE" "migrate"
        echo " - performs database migration if necessary"
        echo
        cecho "BLUE" "start"
        echo " - starts system"
        echo
        cecho "BLUE" "stop"
        echo " - stops system"
        echo
        cecho "BLUE" "build"
        echo " - Builds system containers"
        exit 1
    ;;
esac
# echo
# check_if_docker_installed
# check_if_node_modules_exists
# check_if_database_volume_created

