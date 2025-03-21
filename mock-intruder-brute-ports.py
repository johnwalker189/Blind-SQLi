import requests
import urllib.parse
from bs4 import BeautifulSoup

#Create different ports to scan
PREFIX_URL = 'http://localhost:'
#  url = 'http://localhost:9001/feature.php?url={}'.format(TARGET_URL)

#for i in range(0, 65536):
TARGET_URL = urllib.parse.quote(PREFIX_URL+str(8888))
URL = ''
#print(TARGET_URL)
url = URL.format(TARGET_URL)
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
img_tags = soup.find_all('img')
if (img_tags):
    print(f"{8888}: {img_tags}")

