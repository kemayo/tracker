#!/usr/bin/python

import urllib2
import gzip
import re
import yaml
import sqlite3
from StringIO import StringIO

__author__ = 'David Lynch (kemayo at gmail dot com)'
__version__ = '0.1'
__copyright__ = 'Copyright (c) 2009 David Lynch'
__license__ = 'New BSD License'

USER_AGENT = 'tracker/%s +http://github.com/kemayo/tracker/tree/master' % __version__

cache = {}

def _fetch(url, cached = True):
    """A generic URL-fetcher, which handles gzipped content, returns a string"""
    if cached and url in cache:
        return cache[url]
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-agent', USER_AGENT)
    f = urllib2.urlopen(request)
    data = f.read()
    if f.headers.get('content-encoding', '') == 'gzip':
        data = gzip.GzipFile(fileobj=StringIO(data)).read()
    f.close()
    cache[url] = data
    return data

class SequenceStore(object):
    def __init__(self, storepath):
        store = sqlite3.connect(storepath)
        self.store = store
        c = store.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, type TEXT, date TEXT, value TEXT)""")
        c.execute("""CREATE INDEX IF NOT EXISTS bytype on store (type, date DESC)""")
        self.store.commit()
        c.close()
    def add(self, type, value):
        c = self.store.cursor()
        c.execute("""INSERT INTO store (type, date, value) VALUES (?, DATETIME(), ?)""", (type, value,))
        self.store.commit()
        c.close()
    def get(self, type):
        c = self.store.cursor()
        c.execute("""SELECT date, value FROM store WHERE type = ? ORDER BY date DESC""", (type,))
        rows = c.fetchall()
        c.close()
        return rows


if __name__ == "__main__":
    store = SequenceStore('data.sqlite')
    targets = yaml.load(open('targets.yaml'))

    for type, data in targets.iteritems():
        print "Fetching for", type, data['url']
        page = _fetch(data['url'])
        match = re.search(data['pattern'], page, re.M)
        if match:
            value = int(match.group(1).replace(',', ''))
            print "Found value", value
            store.add(type, value)
        else:
            print "No value found"
