#!/bin/bash

port=$1
pid=$(lsof -i:$1 -t); kill -TERM $pid || kill -KILL $pid
# for i in `seq 1 2`;
#   do
#     port=`expr 9000 + $i`
#     echo $port
#     pid=$(lsof -i:$port -t); kill -TERM $pid || kill -KILL $pid
#   done


  #lsof -i:9000 | grep PID
  #kill PID