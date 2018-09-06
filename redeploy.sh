#! /bin/bash

if [ -f running.pid ]; then
  kill -9 "$(cat running.pid)"
fi
python stream-tweets.py &
echo $! > running.pid
