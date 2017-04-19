# tohtml.py:  read a tmpl file, consult the database, and emit an html file
#------------------------------------------------------------------------------------------
import sys
#------------------------------------------------------------------------------------------
tipTagCount = 0
#------------------------------------------------------------------------------------------
def readDatabase ():

  f = 'words.tsv'
  lines = open (f).read().split ('\n')
  result = {}
  for line in lines:
    tokens = line.split ('\t')
    #print tokens
    if (len (tokens) != 4):
      continue
    simple = tokens [0]
    #print 'simple: %s' % simple
    lushootseed = tokens [1]
    shortDef = tokens [2]
    longDef = tokens [3]
    result [simple] = (lushootseed, shortDef, longDef)

  return result


#------------------------------------------------------------------------------------------
def printHeader ():

  print """<html>
<head><title>How Daylight Was Stolen</title></head>
  <script type="text/javascript" src="tooltip.js"></script>
  <script type="text/javascript" src="mp3popup.js"></script>
  <link rel="stylesheet" href="tooltip.css" type="text/css" />
</head>
<body>
<center>
"""
#------------------------------------------------------------------------------------------
def printFooter ():

  print "</center></body></html>\n"
#------------------------------------------------------------------------------------------
def formatWord (tipTagCount, db, key):

  
  #sys.stderr.write ('formatWord: %s, %s\n' % (tipTagCount, key))
  if (key.find ('link::') == 0):
    tokens = key.split ('::')
    s = '<a href="javascript: popupPlay (\'%s\')">%s</a>' % (tokens [2], tokens [1])
    sys.stdout.write (s)
    return (tipTagCount)

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
if (len (sys.argv) != 2):
  sys.stderr.write ('usage: python tohtml.py <simple story file>\n')
  sys.exit (1)

db = readDatabase ()

printHeader ()

lines = open (sys.argv [1])
for line in lines:
  line = line.strip ()
  if (line.find ('#') == 0):
    continue
  tokens = line.split ()
  #print tokens
  for token in tokens:
    token = token.strip ()
    tipTagCount = formatWord (tipTagCount, db, token)
  sys.stdout.write ('\n')

printFooter ()