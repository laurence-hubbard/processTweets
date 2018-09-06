#! /bin/bash

if [ -f running-batch.pid ]; then
  kill -9 "$(cat running-batch.pid)"
fi
python batch-tweets.py 1> nohup.out 2> nohup.err &
echo $! > running-batch.pid
