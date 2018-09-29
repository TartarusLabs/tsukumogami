#!/usr/bin/env python

# HTML test case corpus evaluator
# james.fell@alumni.york.ac.uk

import os
import sys
from bs4 import BeautifulSoup


# Define the list of HTML tags that we will check the corpus for.
html5TagList = ["a","abbr","address","area","article","aside","audio","b","base","bdi","bdo","blockquote","body","br","button","canvas","caption","cite","code","col","colgroup","data","datalist","dd","del","dfn","div","dl","dt","em","embed","fieldset","figcaption","figure","footer","form","h1","h2","h3","h4","h5","h6","head","header","hr","html","i","iframe","img","input","ins","kbd","keygen","label","legend","li","link","main","map","mark","meta","meter","nav","noscript","object","ol","optgroup","option","output","p","param","pre","progress","q","rb","rp","rt","rtc","ruby","s","samp","script","section","select","small","source","span","strong","style","sub","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","u","ul","var","video","wbr"]

obsoleteTagList = ["acronym","app","applet","basefont","bgsound","big","blink","center","command","comment","details","dialog","dir","frame","frameset","hgroup","hp0","hp1","hp2","hp3","hype","ilayer","image","isindex","key","layer","listing","marquee","menu","menuitem","multicol","nextid","nobr","noembed","noframes","plaintext","server","sound","spacer","strike","summary","tt","typewriter","xmp"]

fullTagList = html5TagList + obsoleteTagList

# Define the list of HTML attributes that we will check the corpus for.
htmlAttrList = ["abbr","above","accept","accept-charset","accesskey","action","align","alink","alt","archive","async","autocomplete","autofocus","autoplay","axis","background","balance","behavior","below","bgcolor","border","cellpadding","cellspacing","challenge","char","charoff","charset","checked","cite","class","clip","code","codebase","color","cols","compact","content","contenteditable","contextmenu","controls","coords","crossorigin","datetime","declare","default","defer","dir","direction","dirname","download","draggable","dropzone","enctype","face","for","form","formaction","formenctype","formmethod","formnovalidate","formtarget","frame","frameborder","headers","height","hidden","high","href","hreflang","hspace","icon","id","keytype","kind","label","lang","left","link","list","longdesc","loop","low","max","maxlength","marginheight","marginwidth","media","method","min","multiple","name","noresize","noshade","novalidate","nowrap","object","optimum","pagex","pagey","pattern","placeholder","preload","radiogroup","readonly","rel","required","rev","reversed","rows","rules","sandbox","scheme","scope","scoped","scrollamount","scrolldelay","scrolling","selected","sortable","shape","size","sizes","span","spellcheck","src","srcdoc","srclang","standby","start","step","style","summary","tabindex","target","text","title","top","translate","type","value","valuetype","visibility","vlink","vspace","width","wrap","z-index"]


# Read and sanity check all the command line arguments from the user
def readArgs():

	# Check that the correct number of arguments have been supplied.
	if (len(sys.argv) != 2):
		print "Check a corpus of web pages for missing HTML tags and attributes."
		print "Usage: htmlscan.py directory"
		exit()

	# Get directory to read the corpus from.
	corpusInDir = sys.argv[1]

	# Check that the input directory exists.
	if (os.path.isdir(corpusInDir) == False):
		print "Error: Directory does not exist", corpusInDir
		exit()

	# Return the confirmed corpus directory
	return corpusInDir


# Scan the corpus directory, parse the HTML files and build lists of all tags and attributes found
def scanCorpus(corpusInDir):

	# Initialise empty lists for storing the tags and attributes that we find in the corpus.
	corpusTagList = []
	corpusAttributeList = []

	# Keep track of how many pages are in the corpus.
	pageCounter = 0

	# Recurse through the corpus directory and any subdirectories building a list of all the files
	for subdir, dirs, files in os.walk(corpusInDir):
		for file in files:

			# For each file whose extension indicates that it is a HTML file
			if (file.endswith(".html") or file.endswith(".htm")):

		        	print "Scanning:", os.path.join(subdir, file)
	
				# Parse the current HTML file
				soup = BeautifulSoup(open(os.path.join(subdir, file)), 'html.parser')
	
				# Add the tags and attributes from this HTML file to the appropriate lists
				for tag in soup.findAll():
					corpusTagList.append(tag.name)
					corpusAttributeList.append(tag.attrs.keys())
	
				# Increment the web page counter
				pageCounter += 1

	# Flatten the list of attributes found (convert a list of lists into a single list)
	corpusAttributeList = [item for sublist in corpusAttributeList for item in sublist]

	# Return the lists of all tags and attributes found and also how many pages were processed
	return corpusTagList, corpusAttributeList, pageCounter


# Calculate which tags and attributes are missing from the corpus. Report it to the user.
def generateReport(corpusTagList, corpusAttributeList, pageCounter):

	# Calculate the missing HTML tags and attributes by subtracting those we found from the lists of all that exist.
	missingHtml5TagSet = set(html5TagList) - set(corpusTagList)
	missingObsoleteTagSet = set(obsoleteTagList) - set(corpusTagList)
	missingAttributeSet = set(htmlAttrList) - set(corpusAttributeList)

	# Tell the user what we found for this corpus
	print "\nNumber of web pages in corpus:", str(pageCounter)

	print "\nNumber of HTML5 tags in specification:", len(set(html5TagList))
	print "Number of obsolete HTML tags in specification:", len(set(obsoleteTagList))
	print "Total Number of HTML tags in specification:", len(set(fullTagList))
	
	print "\nNumber of HTML5 tags found in corpus:", len(set(html5TagList)) - len(missingHtml5TagSet)
	print "Number of HTML5 tags missing from corpus:", len(missingHtml5TagSet)
	print "Missing HTML5 tags:", missingHtml5TagSet

	print "\nNumber of obsolete HTML tags found in corpus:", len(set(obsoleteTagList)) - len(missingObsoleteTagSet)
	print "Number of obsolete tags missing from corpus:", len(set(missingObsoleteTagSet))
	print "Missing obsolete HTML tags:", missingObsoleteTagSet

	print "\nNumber of HTML attributes in specification:", len(set(htmlAttrList))
	print "Number of HTML attributes found in corpus:", len(set(htmlAttrList)) - len(missingAttributeSet)
	print "Number of HTML attributes missing from corpus:", len(set(missingAttributeSet))
	print "Missing HTML attributes:", missingAttributeSet

	print "\nSummary: Adding the missing HTML tags and attributes shown above to the corpus will increase code coverage and increase the probability of detecting vulnerabilities in the web browser being tested.\n"

	return 0


# Main function
def startup():
	corpusInDir = readArgs()
	corpusTagList, corpusAttributeList, pageCounter = scanCorpus(corpusInDir)
	generateReport(corpusTagList, corpusAttributeList, pageCounter)


startup()

