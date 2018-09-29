#!/usr/bin/env python

# Test harness for reading web pages from disk and feeding them to a web browser
# james.fell@alumni.york.ac.uk

import os
import sys
from twisted.internet import reactor, endpoints
from twisted.web.server import Site
from twisted.web.resource import Resource



# Read and sanity check all the command line arguments from the user
def readArgs():

	# Check the correct number of arguments have been supplied
	if (len(sys.argv) != 3):
		print "Test harness for reading web pages from disk and feeding them to a web browser."
		print "Usage: htmlharness.py directory port"
		exit()

	# Get directory to read the corpus from.
	corpusInDir = sys.argv[1]

	# Check that the input directory exists.
	if (os.path.isdir(corpusInDir) == False):
		print "Error: Directory does not exist", corpusInDir
		exit()

	# Get the TCP port on localhost that the HTTP server should listen on
	try: 
		listenPort = int(sys.argv[2])
	except ValueError:
		print "Error: TCP port must be an integer."
		exit()

	# Check that it is a valid port number
	if ((listenPort < 1024) or (listenPort > 65535)):
		print "Error: TCP port should be between 1024 and 65535."
		exit()

	return corpusInDir, listenPort


# Code to execute whenever the HTTP server receives a request from a web browser
class FuzzPage(Resource):

	isLeaf = True

	# Handle GET requests
	def render_GET(self, request):

		global testCaseCounter, testCases, logFilename

		# If the GET request is for the web root
		if (request.uri == '/'):
			
			# If we have reached the end of the corpus, return a message stating this
			if (testCaseCounter >= len(testCases)):
				print "Finished."
				return "<html><head><title>All done!</title></head><body><p>Finished!</p></body></html>"

			# Otherwise read in the next HTML test case to return to the web browser
			else:
				# Add a meta refresh tag to the start of the page and disable caching
				fuzzyText = '<meta http-equiv="refresh" content="1"> <meta http-equiv="cache-control" content="no-cache">'
	
				# Read the next test case from disk
				f = open(testCases[testCaseCounter], 'r')
				fuzzyText += f.read()
				f.close()

				# Save the filename of the current test case to the log to track our progress
				f = open(logFilename, 'a')
				f.write(testCases[testCaseCounter] + '\n')
				f.close

				# Increment the test case counter
				testCaseCounter += 1

				# Return the web page to the web server to be fed to the browser
				return fuzzyText

		# If the GET request is for anything else return an empty string
		else:
			return ""


# Spin up a HTTP server on localhost
def startFuzzServer(listenPort):
	print "Starting HTTP Server. Please point the web browser to be tested at http://127.0.0.1:" + str(listenPort)
	resource = FuzzPage()
	factory = Site(resource)
	endpoint = endpoints.TCP4ServerEndpoint(reactor, listenPort)
	endpoint.listen(factory)
	reactor.run()
	return 0


# Recurse through the corpus directory and any subdirectories building a list of all the files
def scanCorpus(corpusInDir):
	filesList = []
	for subdir, dirs, files in os.walk(corpusInDir):
		for file in files:
	        	filesList.append(os.path.join(subdir, file))
	print "Found", str(len(filesList)), "files in corpus"
	return filesList


# Main function
def startup():

	global testCaseCounter, testCases, logFilename

	# Read command line arguments from user
	corpusInDir, listenPort = readArgs()

	# Set the filename of the log file and create the empty log file
	logFilename = 'htmlharness-log-' + str(listenPort) + '.txt'
	f = open(logFilename, 'w')
	f.close

	# Initialise counter for number of test cases served so far
	testCaseCounter = 0

	# Read all test case file names into a list ready to process
	testCases = scanCorpus(corpusInDir)

	# Start up the web server and wait for the web browser to connect
	startFuzzServer(listenPort)


startup()



