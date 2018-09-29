#!/usr/bin/env python

# HTML test case corpus scraper
# james.fell@alumni.york.ac.uk

import os
import sys
import random
import wget
import math
from google import search


# List of keywords that can be searched on Google in order to find a variety of web pages. The user is encouraged to add more here!
keywordsList = ['web development','weather in germany','museums in manchester','artificial intelligence','list of horror movies','furniture stores','how to brew beer','universities in europe','viking history','learn the guitar']


# Read and sanity check all the command line arguments from the user
def readArgs():

	# Check that the correct number of arguments have been supplied
	if (len(sys.argv) != 3):
		print "Create a corpus of web pages by web crawling."
		print "Usage: htmlscrape.py directory number-of-files"
		exit()

	# Get the output directory and check that it exists
	corpusOutDir = sys.argv[1]
	if (os.path.isdir(corpusOutDir) == False):
		print "Error: Directory does not exist. Please create it."
		exit()

	# Get the number of web pages to harvest and check that it is an integer
	try: 
		numFiles = int(sys.argv[2])
	except ValueError:
		print "Error: Second argument must be an integer."
		exit()

	# Return the output directory and the number of web pages to harvest
	return corpusOutDir, numFiles


# Run searches on Google using each keyword and save the required number of result URLs in a list
def googleSearch(numFiles):

	print "\nCollecting URLs from Google search results\n"

	# Calculate how many results we need to download for each keyword
	pagesPerKeyword = int(math.ceil(float(numFiles) / float(len(keywordsList))))

	# Create the empty list
	urlsList = []

	# For each keyword, run the Google search and add the required number of URLs to the list from the results 
	for searchKeyword in keywordsList:

		# If we don't have enough URLs in our list yet
		if (len(urlsList) < numFiles):

			# Execute the search on Google
			searchResults = search(searchKeyword, stop=pagesPerKeyword)

			# Add the necessary number of URLs to the list from the search results
			urlCounter = 0
			for url in searchResults:
				if (urlCounter < pagesPerKeyword) and (len(urlsList) < numFiles): 
					print "Adding URL to list:", url
					urlsList.append(url)
					urlCounter += 1

	# Return the finished list of URLs
	return urlsList


# Build the corpus. Download each web page in the list and save it to the output directory
def downloadPages(corpusOutDir, urlsList):
	
	print "\nDownloading each web page"

	pageCounter = 0

	# Download each URL and move it to the output directory
	for targetUrl in urlsList:
		pageCounter += 1
		print "\nDownloading web page:", targetUrl
		filename=wget.download(targetUrl)
		os.rename(filename, corpusOutDir + '/page' + str(pageCounter) + '.html')

	print "\n\nFinished. Your new corpus is in", corpusOutDir, "\n"

	return 0


# Main function
def startup():

	# Read command line options from user
	corpusOutDir, numFiles = readArgs()

	# Output some stats
	print "\nNumber of search keywords in list:", str(len(keywordsList))
	print "Number of web pages requested by user:", str(numFiles)

	# Perform Google searches to build list of URLs
	urlsList = googleSearch(numFiles)

	# Attempt to download each of the web pages to the output directory
	downloadPages(corpusOutDir, urlsList)

	return 0



startup()



