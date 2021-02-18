""" 
	Description: This spider scrapes Emsi's job board 
	and saves the job postings to a JSON file. Saved fields
	include a job title, a location, a team, a category,
	and a link to the job posting.
	Author: Tanner Varrelman
"""

import scrapy
from bs4 import BeautifulSoup
import json
from termcolor import colored

class EmsiSpider(scrapy.Spider):
	name = "Emsi"
	# start_requests is a generator fuction
	def start_requests(self):
		# list of urls that we will be crawling for data
		urls = ["https://jobs.lever.co/economicmodeling/"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	# parse parses the document accessed from the request
	def parse(self, response):
		# parse the page
		soup = BeautifulSoup(response.text, features="lxml")
		# find the full list of postings
		posting_list = soup.find_all('div', attrs={'class':'posting'}) 
		data = []
		# iterate through the list of postings
		for posting in posting_list:
			# find the posting title
			title = posting.find('h5').text
			# find the location of the job
			location = posting.find('span', attrs={'class':'sort-by-location'}).text
			# find the team and category for the position
			team_cat = posting.find('span', attrs={'class':'sort-by-team'}).text
			# separate the team and category
			if ' – ' in team_cat:
				team, category = team_cat.split(' – ', 1)
			else:
				team = team_cat
				category = None
				warning = "Posting, {0}: does not contain both team and category".format(title)
				print(colored(warning, 'red'))
			# find the link to each posting
			link = posting.find('a', href=True)
			data.append({
				'Position Title': title,
				'Position Location': location,
				'Team': team,
				'Category': category,
				'Posting Link': link['href']
				})
		# write data to the JSON file
		with open("EmsiJobs.json", "w") as json_file:
			json.dump({
				'JobPostings':data
				}, json_file)


