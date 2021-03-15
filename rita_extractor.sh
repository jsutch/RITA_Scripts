#!/bin/bash
# creates a directory and zipfile containing the longconnections and beacons output for the RITA/Zeek notebook analyzer
#
# instance is the database you want to query
# name is the custom name for the outputs
if [ $# -lt 4 ]
  then
    echo "No arguments supplied"
    echo "need a valid rita database and a safe output name"
    echo "e.g. rita_extractor -i sf-firewall1 -n sfext"
    exit 1
fi


while getopts i:n: flag
    do
        case "${flag}" in
            i) instance=${OPTARG};;
            n) name=${OPTARG};;
       \?) echo "Invalid Option: -$OPTARG" 1>&2
           exit 1;;
            :) echo "Invalid Option: -$OPTARG requires an argument" 1>&2
                    exit 1;;
        esac
    done
    echo "instance: $instance";
    echo "name: $name";


DATE=$(/usr/bin/date +\%Y\%m\%d\%H\%M\%S)
TOKEN=${name}_${DATE}
echo $TOKEN, $instance $name

/usr/bin/mkdir ${TOKEN}
cd ${TOKEN}

rita show-long-connections ${instance} >> ${TOKEN}_longconns.csv
rita show-beacons ${instance} >> ${TOKEN}_beacons.csv


/usr/bin/zip ${TOKEN}.zip ${TOKEN}_longconns.csv ${TOKEN}_beacons.csv:
