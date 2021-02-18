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
		# find the posting title
		post_headline = post_soup.find('div', attrs={'class':'posting-headline'})
		title = post_headline.find('h2').text
		location = post_headline.find('div', attrs={'sort-by-time'}).text
		commitment = post_headline.find('div', attrs={'sort-by-commitment'}).text
		team_cat = post_headline.find('div', attrs={'sort-by-team'}).text
		if ' – ' in team_cat:
			team, category = team_cat.split(' – ', 1)
		else:
			team = team_cat
			category = None
			warning = "Posting, {0}: does not contain both team and category".format(title)
			print(colored(warning, 'red'))
		print(colored([title, location, commitment, team, category],'yellow'))

		# 	data.append({
		# 		'Position Title': title,
		# 		'Position Location': location,
		# 		'Team': team,
		# 		'Category': category,
		# 		'Posting Link': link['href']
		# 		})
		# # write data to the JSON file
		# with open("EmsiJobs.json", "w") as json_file:
		# 	json.dump({
		# 		'JobPostings':data
		# 		}, json_file)


