import requests
from bs4 import BeautifulSoup
import re

baseURL = 'https://www.cattle.com/markets/archive.aspx?code=MG_LS144'

# Start by getting all links on the right side of the page
page = requests.get(baseURL) # pull HTML
soup = BeautifulSoup(page.content, 'html.parser') # parse HTML

link_data = soup.find_all(class_='list-group-item') # find all list-group-items which are links to the data

# for each list-group-item get the contained link
links = []
for plink in link_data:
	date_link = plink.find('a')['href']
	links.append(date_link)

# Now get all data into text files
pre_crap = r'(\<pre style.*\>)\s+MG_LS144' # regular expression for extraneous html
pre_crap = re.compile(pre_crap)

for link in links[673:]: # need to babysit because I didn't provide for HTTP error correction
	# make direct link to data page
	thisURL = baseURL + '&' + link

	# pull and parse HTML
	page = requests.get(thisURL)
	soup = BeautifulSoup(page.content, 'html.parser')

	# dig to the data
	soup = soup.find(class_='container sitecontainer bgw')
	soup = soup.find(class_='col-md-9 col-sm-12')
	data = soup.find('pre')
	
	# format the data
	data = str(data)
	data = data.replace('<br/>', '\n') # add newlines
	
	extraneous = re.match(pre_crap, str(data))
	extraneous = extraneous.group(1)

	data = data.replace(extraneous, '')
	data = data.replace('</pre>', '')
	data = data.strip()
	
	
	# save formatted data
	with open(f'data/{link[20:]}.txt', 'w') as file:
		file.write(str(data))

	print(link) # show where we are in the process

