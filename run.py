#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import datetime

date_format = "%A, %B %d, %Y"
documents_total = 0
base_url = "https://en.wikisource.org"

def main():
  crawl("/wiki/Executive_Order_1")
  

def crawl(url):
  global documents_total
  r = requests.get(base_url+url, proxies=proxies)
  html = r.text.encode('utf-8')
  html = html.replace(b'\xEF\xBB\xBF',b'')
  soup = BeautifulSoup(html,'html5lib')
  result,next_page = parse_old_template(soup)
  print documents_total, result['title']

  if next_page is not None:
    crawl(next_page)



def parse_old_template(soup):
  global documents_total
  div = soup.find(id='navigationHeader')
  title = div.find(id='header_title_text').text.strip()
  description = div.find(id='header_section_text').text.strip()
  next_page = div.find(id='headernext').find('a')['href']
  
  div = soup.find(id='nav_cite_bar')
  president = div.find('a').text.strip()

  cite = div.text.strip()
  ind = cite.index(president)
  date = cite[ind+len(president):]

  result = {}
  result['title'] = title
  result['description'] = description
  result['president'] = president
  result['date'] = date
  documents_total = documents_total + 1
  return result,next_page


if __name__=="__main__":
  main()
