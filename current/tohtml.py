# tohtml.py:  read a tmpl file, consult the database, and emit an html file
#------------------------------------------------------------------------------------------
import sys, os
import pdb
#------------------------------------------------------------------------------------------
tipTagCount = 0
#------------------------------------------------------------------------------------------
def readDatabase ():

  #f = '%s/%s' % (os.environ ['HOME'], 'proj/lushootseed/words.tsv')
  f = "words.tsv"
  lines = open (f).read().split ('\n')
  #print(lines)
  result = {}
  for line in lines:
    tokens = line.split ('\t')
    #print(tokens)
    if (len (tokens) == 3):
       tokens.append(" ")
    simple = tokens [0]
    #print('simple: %s' % simple)
    lushootseed = tokens [1]
    shortDef = tokens [2]
    longDef = tokens [3]
    result [simple] = (lushootseed, shortDef, longDef)

  return result


#------------------------------------------------------------------------------------------
def printHeader (title):

  print("""<html>
<head><title>%s</title></head>
  <script type="text/javascript" src="../../tooltip.js"></script>
  <!-- script type="text/javascript" src="../../mp3popup.js"></script -->
  <link rel="stylesheet" href="../../tooltip.css" type="text/css" />
  <link rel="stylesheet" href="../../fonts.css" type="text/css" />
</head>
<body>
<center>
""" % title)

#------------------------------------------------------------------------------------------
def printFooter ():

  print("</center></body></html>\n")

#------------------------------------------------------------------------------------------
def formatWord (tipTagCount, db, key):


  #sys.stderr.write ('formatWord: %s, %s\n' % (tipTagCount, key))
  if (key.find ('link::') == 0):
    tokens = key.split ('::')
    # s = '<a href="javascript: popupPlay (\'%s\')">%s</a>' % (tokens [2], tokens [1])

    s = '<audio loop controls style="width:80px" id="%s" src="%s" preload="auto"></audio>' % (tokens[1], tokens[2])
    sys.stdout.write (s)
    return (tipTagCount)

  #pdb.set_trace()
  word = db [key][0]
  definition = '%s; %s' % (db [key][1], db [key][2])
  tipTag = 't%d' % tipTagCount
  tipTagCount += 1

  s = ''
  s += '<span onmouseout="popUp(event,\'%s\')" onmouseover="popUp(event,\'%s\')">%s</span>' \
     % (tipTag, tipTag, word)

  if (not key in ['SP', 'BR']):
    s += '<div id="%s" class="tip">%s</div>' % (tipTag, definition)

  sys.stdout.write (s)
  return tipTagCount
#------------------------------------------------------------------------------------------
def formatGloss (tipTagCount, line):

  tipTag = 't%d' % tipTagCount
  tipTagCount += 1
  s = '<span onmouseout="popUp(event,\'%s\')" onmouseover="popUp(event,\'%s\')"><b><i>G</i></b></span><div id=\'%s\' class="tip">%s</div> &nbsp;' % \
     (tipTag, tipTag, tipTag, line [7:])
  sys.stdout.write (s)
  return tipTagCount

#------------------------------------------------------------------------------------------
#if (__name__ == "main"):
if (len (sys.argv) != 3):
  sys.stderr.write ('usage: python tohtml.py <simple story file> story title\n')
  sys.exit (1)

#print("about to call readDatabase")
db = readDatabase ()

printHeader (sys.argv [2])

lines = open (sys.argv [1]).read().split ('\n')
lineCount = 0
sys.stderr.write ('line count: %d\n' % len (lines))
for line in lines:
  lineCount = lineCount + 1;
  line = line.strip ()
  if (line.find ('#') == 0):
    continue
  if (line.find ('gloss::') == 0):
    tipTagCount = formatGloss (tipTagCount, line)
    sys.stdout.write ('\n')
    continue
  tokens = line.split ()
  sys.stderr.write ('%d) %s\n' % (lineCount, tokens))
  for token in tokens:
    token = token.strip ()
    tipTagCount = formatWord (tipTagCount, db, token)
  sys.stdout.write ('\n')

printFooter ()
