#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class ExecutiveOrder(object):
  def __init__(self):
    self._title           = None
    self._author          = None
    self._number          = None
    self._signed_date     = None
    self._published_date  = None
    self._fr              = None
    self._statute         = None
    self._amends          = []
    self._pdf             = None

  @property
  def amends(self):
    return self.amends

  @amends.setter
  def amends(self, value):
    self._amends = value

  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, value):
    self._title = self.format_str(value)

  @property
  def author(self):
    return self._author

  @author.setter
  def author(self, value):
    self._author = self.format_str(value)

  @property
  def number(self):
    return self._number

  @number.setter
  def number(self, value):
    self._number = self.format_str(value)

  @property
  def fr(self):
    return self._fr

  @fr.setter
  def fr(self, value):
    self._fr = value

  @property
  def signed_date(self):
    return self._signed_date

  @signed_date.setter
  def signed_date(self, value):
    self._signed_date = self.format_date(value)

  @property
  def published_date(self):
    return self._published_date

  @published_date.setter
  def published_date(self, value):
    self._published_date = self.format_date(value)

  @property
  def statute(self):
    return self._statute

  @statute.setter
  def statute(self, value):
    self._statute = self.format_str(value)

  @property
  def pdf(self):
    return self._pdf

  @pdf.setter
  def pdf(self, value):
    self._pdf = self.format_str(value)

  def format_str(self, value):
    if value is not None:
      value = value.replace(u'\xa0',u' ').strip()
    return value

  def format_date(self,value):
    if value is not None:
      value = self.format_str(value)
      date_formats = ["%A, %B %d, %Y","%A %B %d, %Y"]
      for fmt in date_formats:
        try:
          return datetime.strptime(value,fmt).isoformat()
        except ValueError:
          pass
