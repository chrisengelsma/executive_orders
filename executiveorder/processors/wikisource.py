#!/usr/bin/env python
# -*- coding: utf-8 -*-
from executiveorder.util import *
from executiveorder.executiveorder import ExecutiveOrder

base_url = "https://en.wikisource.org"
url = "/wiki/Category:United_States_executive_orders"
eos = []

def run():
  pages = get_all_pages(url)
  for page in pages:
    print page,'...'
    result = crawl(page)
    eos.append(result)
  output_results(eos)
  

def get_all_pages(url):
  '''
  Gets all the pages in the base site.
  '''
  soup = get_soup(base_url+url)
  links = soup.find_all('a', { 'class': 'CategoryTreeLabel' } )
  links = [link for link in links if is_int(link.text[-4:]) ]
  result = []

  for link in links:
    link_text = link.text[-4:]
    print link_text,"...",
    soup_page = get_soup(base_url+link['href'])
    sub_pages = soup_page.find(id='mw-pages').find_all('a')
    print "found",str(len(sub_pages))
    for sub_page in sub_pages:
      result.append(sub_page['href'])
  return result


def crawl(url):
  '''
  Crawls a url.
  '''
  soup = get_soup(base_url+url)
  result = parse_page(soup)
  return result


def parse_page(soup):
  '''
  Parses the HTML of a page.
  '''
  eo = ExecutiveOrder()

  parse_heading(eo,soup)

  if soup.find(id='nav_cite_bar') is None:
    return eo

  parse_cite_bar(eo,soup)
  parse_amendments(eo,soup)

  return eo


def parse_heading(eo,soup):
  '''
  Parses the heading for the title and number.
  '''
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
  '''
  Parses the cite bar for author, statute, FR, publication and signed date.
  '''
  div = soup.find(id='nav_cite_bar')
  links = div.find_all('a')
  links = [link for link in links if 'Signed' not in link.text]
  cite_bar = div.text.strip()

  if links[0] is not None:
    author = links[0].text.split(' ')
    lenauthor = len(links[0].text)
    ind = cite_bar.index(links[0].text)

    eo.author = format_president_name(author)
    date_and_cite = cite_bar[ind+lenauthor:].split('\n')
    eo.signed_date = date_and_cite[0]
    
  for link in links[1:]:
    if 'Stat' in link.text:
      eo.statute = link.text
    if is_int(link.text):
      eo.fr = int(link.text)
      eo.pdf = link['href']

  for cite in date_and_cite[1:]:
    if 'FR' in cite:
      fr = cite.split(' ')[2]
      ind = cite.index(fr)
      eo.published_date = cite[ind+len(fr):]

  return eo


def parse_amendments(eo,soup):
  '''
  Parses the Notes section for any possible amendments.
  '''
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


def format_president_name(name):
  ''' 
    Formats the president name to be FIRST-NAME MIDDLE-INITIALS LAST-NAME.
  '''
  out_name = [i[0].upper() for i in name]
  out_name[0] = name[0].decode('utf-8').upper()
  out_name[-1] = name[-1].decode('utf-8').upper()
  return " ".join([unicode(i) for i in out_name])

