#!/usr/bin/env python3

from sys import stdin
from collections import deque

start_times = deque()
end_times = deque()

latest_begin = -1
earliest_finish = 25

def GetTimes():
  try:
    line = stdin.readline()
    line = line.split()
    return line
  except ValueError:
    return -1

state = "begin"
times = GetTimes()

for time in times:
    if state == "begin":
        start_times.append(int(time))
        state = "end"
    else:
        end_times.append(int(time))
        state = "begin"

for time in start_times:
    if time > latest_begin:
        latest_begin = time

for time in end_times:
    if time < earliest_finish:
        earliest_finish = time

print(latest_begin, earliest_finish)