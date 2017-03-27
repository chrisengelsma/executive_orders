#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from executiveorder import ExecutiveOrder
from pprint import pprint
import sys
import json

documents_total = 0
base_url = "https://en.wikisource.org"
url = "/wiki/Category:United_States_executive_orders"

def main():
  pages = get_all_pages(url)
  eos = []
  i, total = 0, len(pages)
  for page in pages:
    print page
    result = crawl(page)
    eos.append(result)
    i = i + 1
  output(eos)
  

def output(eos):
  with open("executive_orders.json","w") as openfile: 
    json.dump([eo.__dict__ for eo in eos], openfile)


def get_all_pages(url):
  i = 0
  soup = get_soup(url)
  links = soup.find_all('a', { 'class': 'CategoryTreeLabel' } )
  links = [link for link in links if is_int(link.text[-4:]) ]
  result = []
  n = len(links)

  for link in links:
    link_text = link.text[-4:]
    print link_text,"...",
    soup_page = get_soup(link['href'])
    sub_pages = soup_page.find(id='mw-pages').find_all('a')
    print "found",str(len(sub_pages))
    for sub_page in sub_pages:
      result.append(sub_page['href'])

  return result


def crawl(url):
  soup = get_soup(url)
  result = parse_page(soup)
  return result


def parse_page(soup):
  global documents_total
  eo = ExecutiveOrder()

  parse_heading(eo,soup)

  if soup.find(id='nav_cite_bar') is None:
    return eo

  parse_cite_bar(eo,soup)
  parse_amendments(eo,soup)
  documents_total = documents_total + 1

  return eo


def parse_heading(eo,soup):
  number = soup.find(id='firstHeading').text.split(' ')[-1]

  div = soup.find(id='navigationHeader')
  section_title = div.find(id='header_section_text')
  if section_title is not None:
    title = section_title.text
  else:
    title = div.find(id='header_title_text').text

  eo.number = number
  eo.title = title
  return eo


def parse_cite_bar(eo,soup):
  div = soup.find(id='nav_cite_bar')
  links = div.find_all('a')
  links = [link for link in links if 'Signed' not in link.text]

  if links[0] is not None:
    name = links[0].text.split(' ')
    first_name = name[0].decode('utf-8').upper()
    last_name = name[-1].decode('utf-8').upper()
    eo.author = " ".join([unicode(first),unicode(last)])
    
  for link in links[1:]:
    if 'Stat' in link.text:
      eo.statute = link.text
    if is_int(link.text):
      eo.fr = int(link.text)
      eo.pdf = link['href']à

  cite_bar = div.text.strip()
  ind = cite_bar.index(eo.author)
  date_and_cite = cite_bar[ind+len(eo.author):].split('\n')

  eo.signed_date = date_and_cite[0]

  for cite in date_and_cite[1:]:
    if 'FR' in cite:
      fr = cite.split(' ')[2]
      ind = cite.index(fr)
      eo.published_date = cite[ind+len(fr):]

  return eo


def parse_amendments(eo,soup):
  div = soup.find(id='Notes')
  if div is None:
    return
  amends = []
  div = div.parent.parent
  dt = div.find('dt')
  if dt is not None and 'Amends' in dt.text:
    items = dt.parent.find_next('ul').find_all('li')
    for item in items:
      link = item.find('a')
      if link is not None:
        amends.append(link.text.split(' ')[-1])
  eo.amends = amends

  return eo
    

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
