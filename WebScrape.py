# DO NOT ABUSE THE CODE. BE RESPONSIBLE.

import requests
from bs4 import BeautifulSoup
import sys

# Workaround to get print work for utf-8 encoding
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# Scrape the web, and return a list of dictionaries.
def GetAllQuotes():
	base_url="http://quotes.toscrape.com/"
	page_url=""

	all_quotes=[]
	while page_url != None:
		url=base_url+page_url
		# Get the content, this is useful for static website
		res=requests.get(url)
		print(url)
		if res.status_code != 200:
			# Exit the loop as something went wrong with the request
			break

		# Otherwise parse the return object
		soup=BeautifulSoup(res.text,'html.parser')

		# Get all quotes under
		quotes=soup.find_all(class_="quote")
		for quote in quotes:
			all_quotes.append({
				"text": quote.find(class_="text").get_text(),
				"author": quote.find(class_="author").get_text(),
				"href":quote.find("a")["href"]
				})

		# See if there is any next page.
		page_url = None
		next_btn = soup.find(class_="next")
		if next_btn:
			page_url=next_btn.find("a")["href"]
	return all_quotes
