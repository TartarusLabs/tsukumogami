#!/usr/bin/env python

# HTML test case corpus generator
# james.fell@alumni.york.ac.uk

import os
import sys
import random
from collections import defaultdict


# Read and sanity check all the command line arguments from the user
def readArgs():

	# Check the correct number of arguments have been supplied
	if (len(sys.argv) != 3):
		print "Generate a corpus of web pages from a built-in grammar."
		print "Usage: htmlgen.py directory number-of-files"
		exit()

	# Get directory to write the corpus to and check that it exists
	corpusOutDir = sys.argv[1]
	if (os.path.isdir(corpusOutDir) == False):
		print "Error: Directory does not exist. Please create it."
		exit()

	# Get the number of files to generate and check that its an integer
	try: 
		numFiles = int(sys.argv[2])
	except ValueError:
		print "Error: Second argument must be an integer."
		exit()

	return corpusOutDir, numFiles


# Class to represent a context free grammar
class htmlGrammar(object):

	def __init__(self):
		self.productionRules = defaultdict(list)

	# Generate web page by recursively expanding non-terminal symbols using random choices until there are none left
	def generateWebpage(self, symbol):
		
		randProdRule = random.choice(self.productionRules[symbol])
		webpage = ''

		for gramSymbol in randProdRule:
			if gramSymbol in self.productionRules:
				webpage += self.generateWebpage(gramSymbol)
 			else:
				webpage += gramSymbol + ' '
		return webpage

	# Add a new rule to the grammar
	def newRule(self, nonTerminal, rightHandSide):
		prodRules = rightHandSide.split('|')
		for prodRule in prodRules:
			self.productionRules[nonTerminal].append(tuple(prodRule.split()))


# Instantiate a grammar object and add production rules to represent syntactically valid HTML. 
# We use 108 HTML5 tags and 44 obsolete tags. We also use 147 attributes. Very limited SVG and CSS support is also included.
def buildGrammar():

	fullHtmlGrammar = htmlGrammar()

	# Begin HTML grammar
	fullHtmlGrammar.newRule('a_tag', '<a accesskey="c" charset="UTF-8" coords="0,0,82,126" download="blah" href="http://127.0.0.1" hreflang="en" media="screen and (min-width:500px)" name="blah" rel="nofollow" rev="alternate" shape="rect" target="_top" type="text/html"> a_content </a>')
	fullHtmlGrammar.newRule('a_content', 'heading | text')
	fullHtmlGrammar.newRule('abbr_tag', '<abbr title="blah"> blah </abbr>')
	fullHtmlGrammar.newRule('acronym_tag', '<acronym title="blah"> blah </acronym>')
	fullHtmlGrammar.newRule('address_tag', '<address> address_content </address>')
	fullHtmlGrammar.newRule('address_content', 'p_tag | text')
	fullHtmlGrammar.newRule('app_tag', '<app code="blah.class"></app>')
	fullHtmlGrammar.newRule('applet_content', '<param name="autoplay" type="blah" value="true" valuetype="object"> body_content')
	fullHtmlGrammar.newRule('applet_tag', '<applet align="left" alt="blah" archive="http://127.0.0.1" code="blah.class" codebase="http://127.0.0.1" height="350" hspace="5" name="blah" object="blah" vspace="5" width="350"> applet_content </applet>')
	fullHtmlGrammar.newRule('area_tag', '<area alt="blah" coords="0,0,82,126" download="blah" href="http://127.0.0.1" hreflang="en" media="screen and (min-color-index:256)" nohref rel="alternate" shape="circle" target="_top" type="text/html">')
	fullHtmlGrammar.newRule('article_tag', '<article> block_content </article>')
	fullHtmlGrammar.newRule('aside_tag', '<aside> h3_tag p_tag </aside>')
	fullHtmlGrammar.newRule('audio_tag', '<audio autoplay controls loop preload="none"> source_tag </audio> | <audio autoplay controls loop preload="none" src="blah.ogg"> </audio>')

	fullHtmlGrammar.newRule('b_tag', '<b> text </b>')
	fullHtmlGrammar.newRule('base_tag', '<base href="http://127.0.0.1" target="_parent">')
	fullHtmlGrammar.newRule('basefont_tag', '<basefont color="red" face="courier, serif" size="5"> body_content </basefont>')
	fullHtmlGrammar.newRule('bdi_tag', '<bdi> blah blah </bdi>')
	fullHtmlGrammar.newRule('bdo_tag', '<bdo dir="rtl"> blah blah </bdo>')
	fullHtmlGrammar.newRule('bgsound_tag', '<bgsound balance="1" loop="3" src="blah.wav" volume="1">')
	fullHtmlGrammar.newRule('big_tag', '<big> text </big>')
	fullHtmlGrammar.newRule('blink_tag', '<blink> text </blink>')
	fullHtmlGrammar.newRule('block', 'block_content')
	fullHtmlGrammar.newRule('block_content', 'article_tag | aside_tag | basefont_tag | blockquote_tag | button_tag | center_tag | datalist_tag | dir_tag | div_tag | dl_tag | figure_tag | footer_tag | form_tag | form_tag label_tag | form_tag output_tag | header_tag | isindex_tag | listing_tag | main_tag | header_tag main_tag footer_tag | menu_tag | multicol_tag | nav_tag | nobr_tag | ol_tag | output_tag | p_tag | pre_tag | svg_tag | table_tag | template_tag | typewriter_tag | ul_tag | xmp_tag')
	fullHtmlGrammar.newRule('blockquote_tag', '<blockquote cite="http://127.0.0.1"> body_content </blockquote>')
	fullHtmlGrammar.newRule('body_content', 'address_tag block | bgsound_tag block | comment_tag block | hgroup_tag block | heading block | hr_tag block | layer_tag block | map_tag block | marquee_tag block | block text')
	fullHtmlGrammar.newRule('body_tag', '<body alink="green" bgcolor="blue" link="red" text="green" vlink="red"> body_content </body> | <body alink="green" background="blah.jpg" link="blue" text="green" vlink="red"> body_content </body> | <body alink="green" bgcolor="red" link="blue" text="green" vlink="red"> body_content </body> | <body alink="green" bgcolor="green" link="blue" text="red" vlink="red"> body_content </body> | <body alink="green" bgcolor="yellow" link="blue" text="red" vlink="red"> body_content </body>')
	fullHtmlGrammar.newRule('br_tag', 'blah <br> blah blah')
	fullHtmlGrammar.newRule('button_tag', '<button autofocus form="form1" formaction="blah.php" formenctype="text/plain" formmethod="post" formnovalidate formtarget="_blank" name="blahbutton" type="button" value="blah"> blah </button>')

	fullHtmlGrammar.newRule('canvas_tag', '<canvas height="200" id="blahcanvas" width="200" style="border:1px solid"></canvas> <script> var canvas = document.getElementById("blahcanvas"); var ctx = canvas.getContext("2d"); ctx.fillStyle = "red"; ctx.fillRect(0, 0, 80, 80); </script>')
	fullHtmlGrammar.newRule('caption_tag', '<caption align="top"> body_content </caption>')
	fullHtmlGrammar.newRule('center_tag', '<center> body_content </center>')
	fullHtmlGrammar.newRule('cite_tag', '<cite> text </cite> | <cite accesskey="sdsd" class="blah" contextmenu="blahmenu" dir="rtl" draggable="false" dropzone="link" lang="en" spellcheck="false" tabindex="200" title="blah" translate="no"> text </cite>')
	fullHtmlGrammar.newRule('code_tag', '<code> text </code>')
	fullHtmlGrammar.newRule('colgroup_content', '<col align="char" char="." charoff="2" span="2" valign="bottom" width="80">')
	fullHtmlGrammar.newRule('colgroup_tag', '<colgroup align="left" char="." charoff="2" span="2" valign="bottom" width="80"> colgroup_content </colgroup>')
	fullHtmlGrammar.newRule('command_tag', '<command type="command" label="Save" icon="blah.png" onclick="save()">')
	fullHtmlGrammar.newRule('comment_tag', '<!-- This is a comment --> | <comment> This is a very old fashioned comment </comment>')
	fullHtmlGrammar.newRule('content_style', 'cite_tag | code_tag | dfn_tag | em_tag | kbd_tag | samp_tag | strong_tag | var_tag')

	fullHtmlGrammar.newRule('data_tag', '<data id="blahdata" value="blah"> blah </data>')
	fullHtmlGrammar.newRule('datalist_tag', '<datalist id="blahdatalist"> option_tag option_tag </datalist>')
	fullHtmlGrammar.newRule('dd_tag', '<dd> flow </dd>')
	fullHtmlGrammar.newRule('del_tag', '<del cite="blah.htm" datetime="2016-11-10T22:55:03Z"> blah </del>')
	fullHtmlGrammar.newRule('details_tag', '<details open> summary_tag p_tag </details>')
	fullHtmlGrammar.newRule('dfn_tag', '<dfn title="blah"> text </dfn>')
	fullHtmlGrammar.newRule('dialog_tag', '<dialog id="dialog1" open> blah </dialog>')
	fullHtmlGrammar.newRule('dir_tag', '<dir compact> li_tag </dir> | <dir> li_tag </dir>')
	fullHtmlGrammar.newRule('div_tag', '<div align="justify" contextmenu="blahmenu"> body_content </div> | <div align="right"> body_content </div>')
	fullHtmlGrammar.newRule('dl_content', 'dt_tag dd_tag')
	fullHtmlGrammar.newRule('dl_tag', '<dl> dl_content </dl>')
	fullHtmlGrammar.newRule('doctype_tag', '<!DOCTYPE html> | <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"> | <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
	fullHtmlGrammar.newRule('dt_tag', '<dt accesskey="h" class="blah" contextmenu="blahmenu" dir="rtl" draggable="true" dropzone="link" lang="fr" spellcheck="true" tabindex="2" title="blah" translate="yes"> text </dt> | <dt> text </dt>')

	fullHtmlGrammar.newRule('em_tag', '<em> text </em>') 
	fullHtmlGrammar.newRule('embed_tag', '<embed height="200" src="blah.swf" type="application/vnd.adobe.flash-movie" width="200"> flash blah')

	fullHtmlGrammar.newRule('figcaption_tag', '<figcaption> blah </figcaption>')
	fullHtmlGrammar.newRule('figure_tag', '<figure> img_tag figcaption_tag </figure>')
	fullHtmlGrammar.newRule('flow', 'flow_content')
	fullHtmlGrammar.newRule('flow_content', 'block | text')
	fullHtmlGrammar.newRule('font_tag', '<font color="green" face="verdana" size="3"> style_text </font>')
	fullHtmlGrammar.newRule('footer_tag', '<footer> p_tag p_tag </footer>')
	fullHtmlGrammar.newRule('form_content', '<input accept="image/*" align="right" alt="blah" autocomplete="off" autofocus checked dirname="fname.dir" form="form1" formaction="demo_admin.asp" formenctype="multipart/form-data" formmethod="post" formnovalidate="formnovalidate" formtarget="_top" height="48" list="blah" max="5" maxlength="10" min="2" multiple name="email" pattern="[A-Za-z]{3}" placeholder="blah" readonly required size="30" src="submit.gif" step="3" type="file" width="40"><input type="submit" value="Submit form"> | body_content | keygen_tag | select_tag | textarea_tag')
	fullHtmlGrammar.newRule('form_tag', '<form accept="image/gif,image/jpeg" accept-charset="ISO-8859-1" action="blah.php" autocomplete="off" enctype="text/plain" method="post" name="form1" novalidate target="_self"> <fieldset> legend_tag form_content </fieldset> </form>')
	fullHtmlGrammar.newRule('frameset_content', '<frame frameborder="1" longdesc="w3s.txt" marginheight="50" marginwidth="25" name="frame_a" noresize="noresize" scrolling="yes" src="http://127.0.0.1"> | noframes_tag')
	fullHtmlGrammar.newRule('frameset_tag', '<frameset cols="25%,*,25%" rows="25%,*,25%"> frameset_content </frameset>')

	fullHtmlGrammar.newRule('h1_tag', '<h1 align="left"> text </h1>')
	fullHtmlGrammar.newRule('h2_tag', '<h2 align="right"> text </h2>')
	fullHtmlGrammar.newRule('h3_tag', '<h3 align="center" draggable="true"> text </h3>')
	fullHtmlGrammar.newRule('h4_tag', '<h4 align="justify"> text </h4>')
	fullHtmlGrammar.newRule('h5_tag', '<h5 class="h5"> text </h5>')
	fullHtmlGrammar.newRule('h6_tag', '<h6 class="h6" dropzone="copy"> text </h6>')
	fullHtmlGrammar.newRule('head_content', 'base_tag | isindex_tag | link_tag | meta_tag | nextid_tag | style_tag | title_tag')
	fullHtmlGrammar.newRule('head_tag', '<head> head_content </head>')
	fullHtmlGrammar.newRule('header_tag', '<header> h1_tag p_tag </header>')
	fullHtmlGrammar.newRule('heading', 'h1_tag | h2_tag | h3_tag | h4_tag | h5_tag | h6_tag')
	fullHtmlGrammar.newRule('hgroup_tag', '<hgroup> h1_tag h2_tag </hgroup>')
	fullHtmlGrammar.newRule('hp_tag', 'hp0_tag | hp1_tag | hp2_tag | hp3_tag')
	fullHtmlGrammar.newRule('hp0_tag', '<hp0> blah </hp0>')
	fullHtmlGrammar.newRule('hp1_tag', '<hp1> blah </hp1>')
	fullHtmlGrammar.newRule('hp2_tag', '<hp2> blah </hp2>')
	fullHtmlGrammar.newRule('hp3_tag', '<hp3> blah </hp3>')
	fullHtmlGrammar.newRule('hr_tag', '<hr align="right" noshade size="30" width="30">')
	fullHtmlGrammar.newRule('html_content', 'head_tag body_tag | head_tag frameset_tag | head_tag body_tag plaintext_tag | head_tag body_tag')
	fullHtmlGrammar.newRule('html_document', 'html_tag')
	fullHtmlGrammar.newRule('html_tag', '<html> html_content </html> | <html manifest="" xmlns="http://www.w3.org/1999/xhtml"> html_content </html>')
	fullHtmlGrammar.newRule('hype_tag', '<hype> blah </hype>')

	fullHtmlGrammar.newRule('i_tag', '<i> text </i>')
	fullHtmlGrammar.newRule('iframe_tag', '<iframe align="right" frameborder="1" longdesc="blah.txt" marginheight="50" marginwidth="50" name="blahiframe" sandbox="allow-same-origin" scrolling="yes" srcdoc="<p>Hello blah!</p>" src="http://127.0.0.1" width="500">')
	fullHtmlGrammar.newRule('ilayer_tag', '<ilayer above="layer1" background="blah.gif" below="layer2" bgcolor="red" class="classname1" clip="1,1,20,20" height="100" id="blahblah1" left="10" name="blah" pagex="10" pagey="10" src="https://127.0.0.1/" style="blah" top="100" visibility="show" width="50" z-index="1"> body_content </ilayer>')
	fullHtmlGrammar.newRule('image_tag', '<image src="blah.gif"></image>')
	fullHtmlGrammar.newRule('img_tag', '<img alt="blah" border="5" crossorigin="anonymous" height="100" hspace="20" src="blah.gif" width="100">')
	fullHtmlGrammar.newRule('ins_tag', '<ins cite="blah.html" datetime="2016-09-15T22:55:03Z"> blah blah </ins>')
	fullHtmlGrammar.newRule('isindex_tag', '<isindex action="http://127.0.0.1" prompt="blah">')

	fullHtmlGrammar.newRule('kbd_tag', '<kbd> text </kbd>')
	fullHtmlGrammar.newRule('key_tag', '<key> blah </key>')
	fullHtmlGrammar.newRule('keygen_tag', '<keygen autofocus challenge form="form1" keytype="rsa" name="security">')

	fullHtmlGrammar.newRule('label_tag', '<label for="blah" form="form1"> blah </label>')
	fullHtmlGrammar.newRule('layer_tag', '<layer id="layer1" top="250" left="50" width="200" height="200" bgcolor="red"> body_content </layer>')
	fullHtmlGrammar.newRule('legend_tag', '<legend align="right"> blah </legend>')
	fullHtmlGrammar.newRule('li_tag', '<li type="square" value="100"> flow </li> | <li hidden> flow </li>')
	fullHtmlGrammar.newRule('link_tag', '<link charset="ISO-2022-JP" crossorigin="anonymous" href="theme.css" hreflang="en" media="print" rel="dns-prefetch" rev="parent" sizes="16x16" target="_blank" type="text/css">')
	fullHtmlGrammar.newRule('listing_tag', '<listing> blah blah </listing>')

	fullHtmlGrammar.newRule('main_tag', '<main> article_tag article_tag </main>')
	fullHtmlGrammar.newRule('map_content', 'area_tag')
	fullHtmlGrammar.newRule('map_tag', '<map name="blahmap"> map_content </map>')
	fullHtmlGrammar.newRule('mark_tag', '<mark> blah </mark>')
	fullHtmlGrammar.newRule('marquee_tag', '<marquee width="200" height="50" direction="left" behavior="alternate" scrolldelay="500" scrollamount="50" bgcolor="yellow" hspace="10" vspace="10" loop="20"> style_text </marquee> | <marquee width="2000" height="500" direction="right" behavior="alternate" scrolldelay="500" scrollamount="80" bgcolor="blue" hspace="50" vspace="50" loop="20"> scrolling along </marquee>')
	fullHtmlGrammar.newRule('menu_tag', '<menu label="blahmenu" type="list" id="mymenu"> li_tag </menu> | <menu label="blahmenu" type="list" id="mymenu"> menuitem_tag </menu>')
	fullHtmlGrammar.newRule('menuitem_tag', '<menuitem checked default icon="blah.png" type="radio" radiogroup="alignment" label="Left"></menuitem>')
	fullHtmlGrammar.newRule('meta_tag', '<meta charset="UTF-8"> | <meta name="keywords" content="HTML,Fuzzing"> | <meta name="date" content="2016-11-07" scheme="YYYY-MM-DD"> | <meta http-equiv="cache-control" content="no-cache">')
	fullHtmlGrammar.newRule('meter_tag', '<meter form="form1" name="x1" min="0" low="40" high="90" max="100" optimum="72" value="95"></meter>')
	fullHtmlGrammar.newRule('multicol_tag', '<multicol width="150" cols="3"> body_content </multicol>')

	fullHtmlGrammar.newRule('nav_tag', '<nav> a_tag a_tag </nav>')
	fullHtmlGrammar.newRule('nextid_tag', '<nextid N="z20">')
	fullHtmlGrammar.newRule('nobr_tag', '<nobr> text </nobr>')
	fullHtmlGrammar.newRule('noembed_tag', '<noembed> blah blah </noembed>')
	fullHtmlGrammar.newRule('noframes_tag', '<noframes> body_content </noframes>')
	fullHtmlGrammar.newRule('noscript_tag', '<noscript> text </noscript>')

	fullHtmlGrammar.newRule('object_content', 'param_tag body_content')
	fullHtmlGrammar.newRule('object_tag', '<object tabindex="3" align="right" border="5" data="blah.swf" declare form="form1" height="200" hspace="100" name="obj1" standby="blah blah" vspace="100" width="200"> object_content </object>')
	fullHtmlGrammar.newRule('ol_tag', '<ol compact reversed start="50" type="I"> li_tag li_tag li_tag </ol>')
	fullHtmlGrammar.newRule('option_tag', '<option label="blah" value="blah" selected> plain_text </option>')
	fullHtmlGrammar.newRule('output_tag', '<output form="form1" name="x" for="a b"></output>')

	fullHtmlGrammar.newRule('p_tag', '<p align="center" contenteditable="false" id="p_fuzz"> text </p> | <p align="left" id="p_fuzz" translate="yes"> text </p>')
	fullHtmlGrammar.newRule('param_tag', '<param name="autoplay" type="blah" value="true" valuetype="object">')
	fullHtmlGrammar.newRule('physical_style', 'b_tag | big_tag | blink_tag | font_tag | i_tag | s_tag | small_tag | span_tag | strike_tag | sub_tag | sup_tag | tt_tag | u_tag')
	fullHtmlGrammar.newRule('plain_text', 'blah blah blah')
	fullHtmlGrammar.newRule('plaintext_tag', '<plaintext> blah blah blah')
	fullHtmlGrammar.newRule('pre_content', 'a_tag | br_tag | hr_tag | style_text')
	fullHtmlGrammar.newRule('pre_tag', '<pre width="30"> pre_content </pre>')
	fullHtmlGrammar.newRule('progress_tag', '<progress value="22" max="100"></progress>')

	fullHtmlGrammar.newRule('q_tag', '<q cite="blah.html"> blah </q>')

	fullHtmlGrammar.newRule('ruby_tag', '<ruby> blah <rb> blah </rb> <rt> <rp>(</rp> blah <rp>)</rp> </rt> <rtc> blah </rtc> </ruby>')

	fullHtmlGrammar.newRule('s_tag', '<s> text </s>')
	fullHtmlGrammar.newRule('samp_tag', '<samp> text </samp>')
	fullHtmlGrammar.newRule('script_tag', '<script async charset="UTF-8"> document.write("blah blah!") </script> | <script defer type="text/javascript" xml:space="preserve"> document.getElementById("demo").innerHTML = "blah!"; </script>')
	fullHtmlGrammar.newRule('section_tag', '<section> h1_tag p_tag </section>')
	fullHtmlGrammar.newRule('select_tag', '<select autofocus form="form1" multiple name="blahselect" required size="5"> <optgroup label="blah"> option_tag option_tag </optgroup> </select>')
	fullHtmlGrammar.newRule('server_tag', '<server> plain_text </server>')
	fullHtmlGrammar.newRule('small_tag', '<small> text </small>')
	fullHtmlGrammar.newRule('sound_tag', '<sound> blah </sound>')
	fullHtmlGrammar.newRule('source_tag', '<source media="screen and (min-width:320px)" src="blah.mp3" type="audio/mpeg">')
	fullHtmlGrammar.newRule('spacer_tag', '<spacer align="left" size="90" type="horizontal"> | <spacer align="right" size="150" type="vertical"> | <spacer align="center" type="block" width="100" height="100">')
	fullHtmlGrammar.newRule('span_tag', '<span style="color:blue"> text </span>')
	fullHtmlGrammar.newRule('strike_tag', '<strike> text </strike>')
	fullHtmlGrammar.newRule('strong_tag', '<strong> text </strong>')
	fullHtmlGrammar.newRule('style_text', 'testing testing')
	fullHtmlGrammar.newRule('sub_tag', '<sub> text </sub>')
	fullHtmlGrammar.newRule('summary_tag', '<summary> blah </summary>')
	fullHtmlGrammar.newRule('sup_tag', '<sup> text </sup>')

	fullHtmlGrammar.newRule('table_cell', 'td_tag | th_tag')
	fullHtmlGrammar.newRule('table_content', '<thead align="char" char="." charoff="5" valign="top"> tr_tag </thead> <tfoot align="char" char="." charoff="1" valign="top"> tr_tag </tfoot> <tbody align="right" char="." charoff="2" valign="bottom"> tr_tag </tbody>')
	fullHtmlGrammar.newRule('table_tag', '<table align="right" bgcolor="yellow" border="1" cellpadding="10" cellspacing="10" frame="box" rules="rows" sortable summary="blah blah" width="400"> caption_tag colgroup_tag table_content </table>')
	fullHtmlGrammar.newRule('td_tag', '<td abbr="blah" axis="blah" bgcolor="red" headers="blah" nowrap scope="row" valign="baseline"> body_content </td>')
	fullHtmlGrammar.newRule('template_tag', '<template id="blah"> tr_tag tr_tag </template>')
	fullHtmlGrammar.newRule('text', 'text_content')
	fullHtmlGrammar.newRule('text_content', 'a_tag | abbr_tag | acronym_tag | app_tag | applet_tag | audio_tag | b_tag | bdi_tag | bdo_tag | big_tag | blink_tag | br_tag | canvas_tag | cite_tag | code_tag | command_tag | comment_tag | data_tag | del_tag | details_tag | dfn_tag | dialog_tag | em_tag | embed_tag | font_tag | hp_tag | hype_tag | i_tag | iframe_tag | ilayer_tag | image_tag | img_tag | ins_tag | kbd_tag | key_tag | mark_tag | meter_tag | noembed_tag | noscript_tag | object_tag | plain_text | progress_tag | q_tag | ruby_tag | s_tag | script_tag | section_tag | server_tag | small_tag | sound_tag | spacer_tag | span_tag | strike_tag | strong_tag | sub_tag | sup_tag | u_tag | samp_tag | svg_tag | time_tag | tt_tag | u_tag | var_tag | video_tag | wbr_tag')
	fullHtmlGrammar.newRule('textarea_tag', '<textarea spellcheck="true" cols="2" dirname="blah.dir" form="form1" maxlength="50" name="blahtextarea" placeholder="blah" required rows="2" wrap="hard"> plain_text </textarea>')
	fullHtmlGrammar.newRule('th_tag', '<th abbr="blah" axis="blah" bgcolor="red" headers="blah" nowrap scope="row" valign="baseline"> body_content </th>')
	fullHtmlGrammar.newRule('time_tag', '<time datetime="2016-02-14"> blah </time>')
	fullHtmlGrammar.newRule('title_tag', '<title> plain_text </title>')
	fullHtmlGrammar.newRule('tr_tag', '<tr align="right" bgcolor="blue" valign="middle"> table_cell </tr>')
	fullHtmlGrammar.newRule('tt_tag', '<tt> text </tt>')
	fullHtmlGrammar.newRule('typewriter_tag', '<typewriter> pre_content </typewriter>')

	fullHtmlGrammar.newRule('u_tag', '<u> text </u>')
	fullHtmlGrammar.newRule('ul_tag', '<ul compact type="square"> li_tag li_tag li_tag </ul> | <ul type="circle"> li_tag li_tag li_tag </ul>')

	fullHtmlGrammar.newRule('var_tag', '<var> text </var>')
	fullHtmlGrammar.newRule('video_tag', '<video autoplay loop preload="metadata" width="320" height="240" controls> <source src="blah.mp4" type="video/mp4"> <track default src="blah.vtt" kind="subtitles" srclang="en" label="English"> </video>')

	fullHtmlGrammar.newRule('wbr_tag', '<wbr> text')

	fullHtmlGrammar.newRule('xmp_tag', '<xmp> <b> should not be bold </b> </xmp>')
	# End HTML grammar


	# Begin limited CSS grammar
	fullHtmlGrammar.newRule('style_tag', '<style media="print" scoped type="text/css"> body_rule </style> | <style media="screen" scoped type="text/css"> code_rule h1_rule hr_rule img_rule p_rule pre_rule svg_rule </style> | <style media="screen" scoped type="text/css"> body_rule </style>')
	fullHtmlGrammar.newRule('body_rule', 'body {margin:0;padding:0;font-family:"Nexa Bold",sans-serif;text-rendering:optimizeLegibility!important;-webkit-font-smoothing:antialiased!important;font-size:16px;color:#58595b;background:#f2f2f2!important;overflow-x:hidden}')
	fullHtmlGrammar.newRule('code_rule', 'code,kbd,pre,samp{font-size:1em}')
	fullHtmlGrammar.newRule('h1_rule', 'h1 {color:red;}')
	fullHtmlGrammar.newRule('hr_rule', 'hr{height:0;-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box}')
	fullHtmlGrammar.newRule('img_rule', 'img {border:0;vertical-align:middle}')
	fullHtmlGrammar.newRule('p_rule', 'p {color:blue;}')
	fullHtmlGrammar.newRule('pre_rule', 'pre,textarea{overflow:auto}')
	fullHtmlGrammar.newRule('svg_rule', 'svg:not(:root){overflow:hidden}')
	# End limited CSS grammar


	# Begin limited SVG grammar
	fullHtmlGrammar.newRule('svg_content', 'svgdesc_tag svgcircle_tag svgellipse_tag svgline_tag svgpolygon_tag svgpolyline_tag svgrect_tag | svgdesc_tag svgcircle_tag svgpolygon_tag svgellipse_tag | svgdesc_tag svgline_tag | svgdesc_tag svgrect_tag | svgpolygon_tag svgellipse_tag')
	fullHtmlGrammar.newRule('svg_tag', '<svg baseProfile="full" contentScriptType="application/ecmascript" focusable="true" height="500" timelineBegin="onStart" version="1.0" viewBox="0 50 1500 1000" width="500" zoomAndPan="magnify"> svg_content </svg> | <svg baseProfile="basic" contentScriptType="application/ecmascript" focusable="false" height="900" timelineBegin="onLoad" version="1.1" viewBox="50 0 1400 1000" width="900" zoomAndPan="disable"> svg_content </svg> | <svg baseProfile="tiny" contentScriptType="application/ecmascript" focusable="auto" height="500" timelineBegin="onStart" version="1.2" viewBox="0 90 1500 1000" width="500" zoomAndPan="magnify"> svg_content </svg>')
	fullHtmlGrammar.newRule('svganimatetransform_tag', '<animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0" to="360" begin="0s" dur="1s" repeatCount="indefinite"></animateTransform>')
	fullHtmlGrammar.newRule('svgcircle_tag', '<circle cx="125" cy="125" r="75" fill="orange"> </circle> | <circle cx="125" cy="125" r="75" fill="yellow"> svganimatetransform_tag </circle>')
	fullHtmlGrammar.newRule('svgdesc_tag', '<desc> SVG Test </desc>')
	fullHtmlGrammar.newRule('svgellipse_tag', '<ellipse transform="translate(900 200) rotate(-30)" rx="250" ry="100" fill="none" stroke="blue" stroke-width="20"> </ellipse> | <ellipse rx="250" ry="100" fill="red"> </ellipse> | <ellipse rx="250" ry="100" fill="yellow"> svganimatetransform_tag </ellipse>')
	fullHtmlGrammar.newRule('svgline_tag', '<line x1="50" y1="50" x2="200" y2="200" stroke="blue" stroke-width="40"> </line> | <line x1="50" y1="50" x2="400" y2="400" stroke="red" stroke-width="8"> svganimatetransform_tag </line>')
	fullHtmlGrammar.newRule('svgpolygon_tag', '<polygon fill="red" stroke="blue" stroke-width="10" points="350,75  379,161 469,161 397,215 423,301 350,250 277,301 303,215 231,161 321,161" /> | <polygon fill="lime" stroke="blue" stroke-width="10" points="850,75 958,137.5 958,262.5 850,325 742,262.6 742,137.5" /> | <polygon fill="red" stroke="blue" stroke-width="10" points="350,75  379,161 469,161 397,215 423,301 350,250 277,301 303,215 231,161 321,161"> svganimatetransform_tag </polygon> | <polygon fill="lime" stroke="red" stroke-width="10" points="850,75 958,137.5 958,262.5 850,325 742,262.6 742,137.5"> svganimatetransform_tag </polygon>')
	fullHtmlGrammar.newRule('svgpolyline_tag', '<polyline points="50,150 50,200 200,200 200,100" stroke="red" stroke-width="4" fill="none"> </polyline> | <polyline points="50,150 50,200 200,200 200,100" stroke="red" stroke-width="4" fill="none"> svganimatetransform_tag </polyline> | <polyline fill="none" stroke="blue" stroke-width="10" points="50,375 150,375 150,325 250,325 250,375 350,375 350,250 450,250 450,375 550,375 550,175 650,175 650,375 750,375 750,100 850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375" /> | <polyline fill="none" stroke="blue" stroke-width="10" points="50,375 150,375 150,325 250,325 250,375 350,375 350,250 450,250 450,375 550,375 550,175 650,175 650,375 750,375 750,100 850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375"> svganimatetransform_tag </polyline>')
	fullHtmlGrammar.newRule('svgrect_tag', '<rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="pink"> </rect> | <rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="pink"> svganimatetransform_tag </rect>')
	# End limited SVG grammar
	
	return fullHtmlGrammar


# Generate requested number of random web pages and write them to the corpus output directory
def generatePages (fullHtmlGrammar, numFiles, corpusOutDir):

	print "Generating", str(numFiles), "random web pages."

	for index in range(numFiles):
		f = open(corpusOutDir + '/page' + str(index+1) + '.html', 'w')
		f.write(fullHtmlGrammar.generateWebpage('html_document'))
		f.close

	print "\nFinished. Your new corpus is in", corpusOutDir, "\n"
	return 0


# Main function
def startup():

	# Read the command line arguments from the user
	corpusOutDir, numFiles = readArgs()

	# Create a new grammar object and add all the production rules
	fullHtmlGrammar = buildGrammar()

	# Use the grammar to generate the requested number of pages and save them to the output directory
	generatePages(fullHtmlGrammar, numFiles, corpusOutDir)


startup()




