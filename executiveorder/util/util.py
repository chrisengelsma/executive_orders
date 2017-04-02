#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
from bs4 import BeautifulSoup


def output_results(eos, out_file="executive_orders.json"):
  try:
    with open(out_file, 'w') as out:
      json.dump([eo.__dict__ for eo in eos], out)
  except IOError:
    print "Failed to output to file",out_file
      

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False


def get_soup(url):
  r = requests.get(url)
  html = r.text.encode('utf-8')
  html = html.replace(b'\xEF\xBB\xBF',b'')
  return BeautifulSoup(html,'html5lib')
