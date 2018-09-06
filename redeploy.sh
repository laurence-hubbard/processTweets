#! /bin/bash

if [ -f running.pid ]; then
  kill -9 "$(cat running.pid)"
fi
python stream-tweets.py 1> nohup.out 2> nohup.err &
echo $! > running.pid
