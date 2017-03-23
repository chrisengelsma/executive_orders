#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import datetime

date_format = "%A, %B %d, %Y"
documents_total = 0
base_url = "https://en.wikisource.org"
url = "/wiki/Category:United_States_executive_orders"

def main():
  pages = get_all_pages(url)
  for page in pages:
    crawl(page)
  

def get_all_pages(url):
  i = 0
  soup = get_soup(url)
  links = soup.find_all('a', { 'class': 'CategoryTreeLabel' } )
  result = []
  for link in links:
    link_text = link.text[-4:]
    if is_int(link_text):
      soup_page = get_soup(link['href'])
      sub_pages = soup_page.find(id='mw-pages').find_all('a')
      for sub_page in sub_pages:
        result.append(sub_page['href'])
        i = i + 1
        if i>20:
          return result
  return result


def crawl(url):
  global documents_total
  soup = get_soup(url)
  result = parse_old_template(soup)
  print documents_total, result['title']


def parse_old_template(soup):
  global documents_total
  div = soup.find(id='navigationHeader')
  title = div.find(id='header_title_text').text.strip()
  description = div.find(id='header_section_text').text.strip()
  
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
  return result


def get_soup(url):
  r = requests.get(base_url+url)
  html = r.text.encode('utf-8')
  html = html.replace(b'\xEF\xBB\xBF',b'')
  return BeautifulSoup(html,'html5lib')


def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

if __name__=="__main__":
  main()
