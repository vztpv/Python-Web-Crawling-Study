
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# access xml
url = 'http://api.plos.org/search?q=title:DNA'

data = urllib.request.urlopen(url, context=ctx).read()

import json

info = json.loads(data)


for item in info['response']['docs']:
    print(item)


conn = sqlite3.connect('test.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS docs')

cur.execute('''
CREATE TABLE docs (id TEXT, journal TEXT, eissn TEXT,
    publication_date TIME, article_type TEXT,
    author_display TEXT, 
    abstract TEXT, 
    title_display TEXT,
    score NUMBER
)''') # more..

for item in info['response']['docs']:
    id = item['id']
    journal = item['journal']
    eissn = item['eissn']
    publication_date = item['publication_date']
    author_display = item['author_display']
    author_display = '  '.join(author_display)
    abstract = item['abstract']
    abstract = '  '.join(abstract)
    title_display = item['title_display']
    score = float(item['score'])

    cur.execute('''INSERT INTO docs (id, journal, eissn, publication_date, 
    author_display, abstract, title_display, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id, journal, eissn,
                publication_date, author_display, abstract, title_display,
                 score))
    
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = '''SELECT id, journal,eissn, publication_date, 
    author_display, abstract, title_display, score FROM docs'''

print()
print()
for row in cur.execute(sqlstr):
    print(row[0], '\n', row[1], '\n', row[2], '\n', row[3], '\n', row[4], '\n', row[5], '\n', row[6], '\n', row[7])
    print()
    print()

cur.close()
