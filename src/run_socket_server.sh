#!/bin/bash

last_free_port=8999
function get_unused_port()
{
  last_free_port=`expr 1 + $last_free_port`
  for port in `seq $last_free_port 65000`;
    do
      pid=$(lsof -i:$port);
      # echo $pid
      if [ -z "$pid" ]; then
        echo $port
        break;
      fi
    done
}

# echo "$(get_unused_port)"
# # FREE_PORT="$(get_unused_port)"
# # echo $FREE_PORT
for i in `seq 0 500`;
  do
    free_port="$(get_unused_port)"
    name="/robot$i"
    last_free_port=$free_port
    echo $free_port
    echo $name
    python app.py $free_port $name &
  done

# python app.py 9000 '/robot1' &
# python app.py 9001 '/robot2' &