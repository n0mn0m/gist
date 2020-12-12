"""
Quick script to parse an HTML page and extract zip files.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import zipfile
import io

"""
Fails if file extraction requires a password
"""

home = 'http://www.dndjunkie.com'
url = 'http://www.dndjunkie.com/rpgx/datasets/'
data = urlopen(url).read()
page = BeautifulSoup(data,'html.parser')
files = []

for link in page.findAll('a'):
    l = link.get('href')
    files.append(l)

for l in files[2:]:
    full_path = home + l
    r = requests.get(full_path)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
