#!/usr/bin/env python

import Queue
import threading
import urllib2
from collections import deque

# called by each thread
def get_url(q, url):
    q.append(url)

theurls = ["http://google.com", "http://yahoo.com"]

q = deque()

threads = []

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    threads.append(t)
    t.daemon = True
    t.start()

for t in threads:
  t.join()

for s in q:
  print s