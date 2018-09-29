# Tsukumogami

Identifying vulnerabilities in software products has been an important area of security research for many years. One of the most successful approaches to this problem so far has been that of fuzz testing or fuzzing. This process involves repeatedly passing invalid inputs into an application at runtime and monitoring it with a debugger or other instrumentation for evidence of potential vulnerabilities being triggered, such as observing a segmentation fault or memory corruption. 

One of the main ways of measuring how thoroughly the fuzzing process has tested a given piece of software is by measuring code coverage throughout the process. If part of the target program has not been executed during fuzzing then any vulnerabilities in that part obviously cannot be detected. This repo contains a suite of software tools that were developed in late 2016 and early 2017 as part of an MSc project. The tools' purpose is to enable the fuzzing of a web browser such that the code coverage obtained during the testing is increased compared to traditional approaches. Some of the key parts of this included building a thorough specification of HTML which included old tags and attributes that are no longer in use but which may still trigger unique code branches in browsers when parsed, creating a Context-Free Grammar to generate syntactically correct web pages that use all these tags and attributes, and experimenting with different DOM fuzzing strategies from JavaScript that mutate the pages in memory in ways likely to trigger memory corruption bugs.

The prototype system was evaluated through a number of experiments and was finally used to fuzz a selection of web browsers. Multiple previously unknown bugs were detected in several different web browsers including Edge, Internet Explorer and Firefox, some of which appeared to be exploitable security vulnerabilities.

The papers directory of this repo contains both a short conference-style precis paper giving an overview of the project, as well as the full thesis report. It is recommended to read these before diving in with the fuzzing tools.


### Installing

Note that development was done using Python 2.7 and this should be used for execution.

* `git clone https://github.com/TartarusLabs/tsukumogami.git`
* `cd tsukumogami/code`
* `pip install -r requirements.txt`


### The Tools

The following five tools are provided. In each case, running the tools with no parameters will print usage instructions.

* HTMLscan – Analyse an existing corpus of web pages and advise on how it could be improved to get better code coverage. This tool will report which HTML tags and attributes exist but are not present anywhere in the corpus. The specification of existing HTML tags and attributes was created by researching as many obsolete, proprietary and historical tags as possible and combining these with the current HTML 5 specification.

* HTMLscrape – Create a new corpus of web pages by random web crawling.

* HTMLgen – Generate a new corpus of web pages from a Context-Free Grammar that was developed as part of this project. The resulting corpus is ideal for use in browser fuzzing sessions due to the superior code coverage that it provides.

* HTMLharness – Test harness to read a corpus of web pages from disk and sequentially deliver each test case to a web browser in order to fuzz it.

* HTMLfuzz – A self-contained DOM fuzzer. Continuously generate test cases using the same grammar as HTMLgen, deliver them to a target web browser and then apply a collection of fuzzing strategies to the DOM tree using JavaScript in order to trigger memory corruption bugs.




