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
from datetime import datetime

class EmsiSpider(scrapy.Spider):
	name = "Emsi"

	# start_requests is a generator fuction
	def start_requests(self):
		# list of urls that we will be crawling for data
		urls = ["https://jobs.lever.co/economicmodeling/"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		soup = BeautifulSoup(response.text, features="lxml")
		# find the full list of postings
		posting_list = soup.find_all('div', attrs={'class':'posting'})
		for posting in posting_list:
			# there is one link per job post
			link = posting.find('a', href=True)
			yield scrapy.Request(link['href'], callback = self.parse_post)

	# parse parses the document accessed from the request
	def parse_post(self, response):
		# parse the page
		post_soup = BeautifulSoup(response.text, features="lxml") 
		# find the headline
		post_headline = post_soup.find('div', attrs={'class':'posting-headline'})
		# extract the position title
		title = post_headline.find('h2').text
		# extract the position location
		location = post_headline.find('div', attrs={'sort-by-time'}).text
		# extract the position commitment
		commitment = post_headline.find('div', attrs={'sort-by-commitment'}).text
		# extract the team and category
		team_cat = post_headline.find('div', attrs={'sort-by-team'}).text
		# team and category need to separated
		if ' – ' in team_cat:
			team, category = team_cat.split(' – ', 1)
		else:
			team = team_cat
			category = None
			warning = "Posting, {0}: does not contain both team and category".format(title)
			print(colored(warning, 'red'))
		# find the first div on the page (this is the description)
		first_block = post_soup.find('div', attrs={'section page-centered'})
		# find all divs in the first block
		div_list = first_block.find_all('div')
		# loop through the divs and extract and combine all text
		desc_list = []
		for div in div_list:
			desc_list.append(div.text)
		if len(desc_list) > 1:
			description = ' '.join(desc_list)
		else:
			description = desc_list[0]
		todays_date = datetime.today().strftime('%Y-%m-%d')
		file_date = datetime.today().strftime('%Y_%m_%d')
		file_name = 'EmsiJobPosts_' + file_date +'.json'
		data = {
				'Position Title': title,
				'Position Location': location,
				'Team': team,
				'Category': category,
				'Position Description': description,
				'Retrieval Date': todays_date
				}
		with open(file_name, "a") as json_file:
			json_file.write(json.dumps(data))
			json_file.write('\n')


