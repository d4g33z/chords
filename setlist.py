#!/usr/bin/python
from __future__ import print_function
import os, sys, glob, copy, pickle
# Cat a list of .txt files into html

class bcolors:
  BLUE = '\033[94m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

helpString = bcolors.WARNING +   \
  "\nArrow to navigate.\n"       \
  "m   - Toggle Move mode.\n"    \
  "s,o - Save/Open setlist.\n"   \
  "r   - Rename setlist.\n"      \
  "a,d - Add/Delete a set.\n"    \
  "c,p - Cut/Paste clipboard.\n" \
  "x   - eXport as html.\n"      \
  "n   - Name the set.\n"        \
  "R   - Remove song.\n"         \
  "S   - Scan for new songs.\n"  \
  "1~9 - Jump to set.\n"         \
  "A   - Alphabetize.\n"         \
  "q   - quit." + bcolors.ENDC

class Set( object ):
  def __init__( self, name=None ):
    self.name = name
    self.songList = []

class Song( object ):
  # Song is just a name for now but may add attributes later
  def __init__( self, name ):
    self.name = name # file name

setLists = []
clipboard = []

unassignedSetName = "Unassigned Songs"
statusString = None
setListName = "SetList"
currentSet = 0 # these represent the 'cursor'
currentSong = 0
setListExt = ".set"

SONG_COLUMNS = 4
MAX_SETS = 10

# input modes
MODE_NORMAL = 0
MODE_MOVE   = 1

inputMode = MODE_NORMAL

unassignedSet = Set( unassignedSetName )
setLists.append( unassignedSet )

def loadSetList():
  global statusString, setLists, setListName
  selectedfileIx = 0
  re = "./*" + setListExt

  matchList = glob.glob( re )

  if not matchList:
    statusString = "No setlists."
    return None

  if selectedfileIx >= len( matchList ):
    selectedfileIx = len( matchList ) - 1

  while True:
    selSong = None
    os.system( 'clear' )
    print( "Use arrow keys to select or exit.\n" )
    index = 0
    for s in matchList:
      line = "  "
      if index == selectedfileIx:
        line = "> "
        selSong = s
      line += s[ 2 : ].split( "." )[ 0 ]
      index += 1

      print( line )

    c = getInput()
    if c == "LEFT" or c == "h":
      return None
    if c == "RIGHT" or c == "l":
      with open( selSong, 'rb' ) as f:
        setLists = pickle.load( f )
      setListName = selSong[ 2 : ].split( "." )[ 0 ]
      return
    if c == "DOWN" or c == "j":
      if selectedfileIx < len( matchList ) - 1:
        selectedfileIx += 1
    if c == "UP" or c == "k":
      if selectedfileIx > 0:
        selectedfileIx -= 1

    # add any local songs not in the list to unassigned

def getSetByName( name ):
  for s in setLists:
    if s.name == name:
      return s
  return None

def getLocalSongs():
  songList = []
  re = "*.txt"
  matchList = glob.glob( re )
  for s in matchList:
    song = Song( s )
    songList.append( song )

  return songList

def displayUI():
  global songIx, setListName, setLists, statusString

  os.system( 'clear' )

  print( "Setlist:%s" % ( setListName ) )

  setNumber = 0

  for l in setLists:
    if setNumber == currentSet and not len( setLists[ currentSet ].songList ):
      print( bcolors.BLUE, end = "" ) # This set is empty, highlight the name
    if l.name:
      print( "\n-", l.name, "-", "/", len( l.songList ) )
    else:
      print( "\nSet:", setNumber + 1, "/", len( l.songList ) )

    if setNumber == currentSet:
      print( bcolors.ENDC, end="" )
    songIx = 0
    for s in l.songList:
      if songIx and songIx % SONG_COLUMNS == 0:
        print()
      cursor = True if setNumber == currentSet and songIx == currentSong else False
      if cursor:
        print( bcolors.BLUE if inputMode == MODE_NORMAL else bcolors.FAIL, end="" )
      print( "%-24s " % ( s.name[ : -4 ] ), end="" )
      if cursor:
        print( bcolors.ENDC, end="" )
      songIx += 1
    print()
    setNumber += 1

  if clipboard:
    print( "\n- Clipboard -" )
    songIx = 0
    for s in clipboard:
      print( "%-24s " % ( s.name[ : -4 ] ), end="" )
      if ( songIx + 1 ) % SONG_COLUMNS == 0:
        print( "" )
      songIx += 1

  if statusString:
    print( bcolors.WARNING )
    print( statusString )
    print( bcolors.ENDC, end="" )

    statusString = None

def getInput ():
  # Copied from http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
  import termios, fcntl, sys, os
  fd = sys.stdin.fileno()
  flags_save = fcntl.fcntl( fd, fcntl.F_GETFL )
  attrs_save = termios.tcgetattr( fd )
  attrs = list( attrs_save )
  attrs[ 0 ] &= ~( termios.IGNBRK | termios.BRKINT | termios.PARMRK | termios.ISTRIP |
                   termios.INLCR  | termios.IGNCR  | termios.ICRNL  | termios.IXON )
  attrs[ 1 ] &= ~termios.OPOST
  attrs[ 2 ] &= ~( termios.CSIZE | termios.PARENB )
  attrs[ 2 ] |= termios.CS8
  attrs[ 3 ] &= ~( termios.ECHONL | termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN )
  termios.tcsetattr( fd, termios.TCSANOW, attrs )
  fcntl.fcntl( fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK )
  try:
    ret = sys.stdin.read( 1 )
    if ord( ret ) == 27: # Escape
      ret = sys.stdin.read( 1 )
      ret = sys.stdin.read( 1 )
      if ret == 'A':
        ret = 'UP'
      elif ret == 'B':
        ret = 'DOWN'
      elif ret == 'C':
        ret = 'RIGHT'
      elif ret == 'D':
        ret = 'LEFT'

  except KeyboardInterrupt:
    ret = 0
  finally:
    termios.tcsetattr( fd, termios.TCSAFLUSH, attrs_save )
    fcntl.fcntl( fd, fcntl.F_SETFL, flags_save )
  return ret

def saveList ():
  global setListName, setListExt, setLists, statusString

  statusString = "Saved."

  fileName = setListName + setListExt

  with open( fileName, 'wb' ) as f:
    pickle.dump( setLists, f )

# a decorator for functions that move the cursor to handle song move
def cursorMover( func ):
  def decor( *args, **kwargs ):
    global currentSet, currentSong

    if inputMode == MODE_MOVE:
      tmpSet = currentSet
      tmpSong = currentSong
      temp = setLists[ tmpSet ].songList[ tmpSong ]

      func( *args, **kwargs )

      if tmpSet == currentSet:
        del setLists[ tmpSet ].songList[ tmpSong ]
        setLists[ currentSet ].songList.insert( currentSong, temp )
      else:
        if currentSong is None: # moved to empty set
          currentSong = 0
        del setLists[ tmpSet ].songList[ tmpSong ]
        setLists[ currentSet ].songList.insert( currentSong, temp )
    else:
      func( *args, **kwargs )

  return decor

@cursorMover
def songFwd (count):
  global currentSong, currentSet

  if currentSet == len( setLists ) - 1 and \
    ( ( currentSong == len( setLists[ currentSet ].songList ) - 1 ) or
        currentSong == None ):
    return

  if currentSong == None:
    if currentSet < len( setLists ):
      currentSet += 1
      if len( setLists[ currentSet ].songList ):
        currentSong = 0
  else:
    l = len( setLists[ currentSet ].songList )
    if currentSong == l - 1: # at the end of the set
      if currentSet < len( setLists ) - 1:
        currentSet += 1
        currentSong = 0 if len( setLists[ currentSet ].songList ) else None
    elif currentSong + count < l:
      currentSong += count
    else:
      currentSong = l - 1

@cursorMover
def songBack( count ):
  global currentSong, currentSet

  if not currentSong:
    if currentSet:
      currentSet -= 1
      l = len( setLists[ currentSet ].songList )
      currentSong = l - 1 if l else None
  elif currentSong > count:
    currentSong -= count
  else:
    currentSong = 0

@cursorMover
def moveToSet( set ):
  global statusString, currentSet, currentSong

  if set >= len( setLists ):
    statusString = "Invalid set"
  else:
    currentSet = set
    l = len( setLists[ currentSet ].songList )
    if l == 0:
      currentSong = None
    elif currentSong >= l:
      currentSong = l - 1
    elif currentSong == None:
      currentSong = 0

def alphabetize():
  def getKey( item ):
    return item.name

  setLists[ currentSet ].songList.sort( key=getKey )

def addSet():
  global currentSet, setLists
  newSet = Set()
  setLists.insert( currentSet, newSet )
  currentSet += 1

def deleteSet():
  # move all songs to unassigned
  global currentSet, currentSong

  l = len( setLists )
  if l > 1 and currentSet < l - 1:
    u = getSetByName( unassignedSetName ).songList
    for s in setLists[ currentSet ].songList:
      u.append( s )
    del setLists[ currentSet ]
    l = len( setLists[ currentSet ].songList )
    currentSong = 0 if l else None

def cutSong ():
  # Delete the current song and return it
  global currentSet, currentSong

  s = None
  if currentSong is not None:
    s = setLists[ currentSet ].songList[ currentSong ]
    del( setLists[ currentSet ].songList[ currentSong ] )
    l = len( setLists[ currentSet ].songList )
    if l == 0:
      currentSong = None
    elif currentSong == l:
      currentSong -= 1
  return s

def cutSongToClipboard ():
  global clipboard, statusString

  s = cutSong()
  if s:
    clipboard.append(s)
  else:
    statusString = "No song."

def pasteClipboard():
  global currentSong, clipboard

  if currentSong == None:
    currentSong = 0
  else:
    currentSong += 1

  for s in clipboard:
    setLists[ currentSet ].songList.insert( currentSong, s )
    currentSong += 1

  clipboard = []

tabMode = False

def exportSet():
  global statusString, setLists

  fname = setListName + ".html"
  f = open( fname, "w" )

  f.write( "<!DOCTYPE html>\n"
           "<html>\n"
           "<head>\n"
           "<style type=\"text/css\">a {text-decoration: none}</style>\n"
           "</head>\n"
           "<body>\n"
           "<h1>%s</h3>\n" % ( setListName ) )
  # setlist summary
  setNumber = 0
  for l in setLists[0 : -1 ]:
    songNumber = 0
    f.write( "<h2>%s</h2><font size=\"5\">\n" % ( l.name if l.name else setNumber + 1 ) )
    for s in l.songList:
      f.write( "<a id=\"t%dt%d\" href=\"#s%ds%d\">%s</a><br>\n" %
              ( setNumber, songNumber, setNumber, songNumber, s.name[ 0 : -4 ] ) )
      songNumber += 1
    f.write( "</font></br>\n" )
    setNumber += 1
  # songs
  setNumber = 0
  numSets = len( setLists ) - 1
  for l in setLists[ 0 : -1 ]: # Don't include the Unassigned
    numSongs = len( l.songList )

    f.write( "<hr><h2>%s</h2>\n" % ( l.name if l.name else setNumber + 1 ) )
    songNumber = 0
    for s in l.songList:
      try:
        sName = s.name
        sf = open( sName, "r" )
        fLines = sf.readlines()
        sf.close()
        fileLine = 0

        def toggleTab( f ):
          global tabMode
          if tabMode == True:
            f.write( "</font>\n" )
            tabMode = False
          else:
            f.write( "<font style=\"font-family:courier;\" size=\"3\">\n" )
            tabMode = True

        for line in fLines:
          if fileLine == 0: # Assume first line is song title
            f.write( "<h4 id=\"s%ds%d\">" % ( setNumber, songNumber ) )
            # song name is link back to location in setlist
            f.write( "<a href=\"#t%dt%d\"> %s </a>\n" % ( setNumber, songNumber, line.rstrip() ) )

            # Link to Next
            if setNumber < numSets - 1 or songNumber < numSongs - 1:
              sameSet = True if songNumber < numSongs - 1 else False
              if sameSet or ( sameSet == False and setNumber < numSets ):
                f.write( "&nbsp &nbsp <a href=\"#s%ds%d\"> &darr; </a>" %
                         ( setNumber      if sameSet else setNumber + 1,
                           songNumber + 1 if sameSet else 0 ) )
            # Link to Prev
            sameSet = True if songNumber > 0 else False
            if sameSet or setNumber > 0:
              f.write( "&nbsp &nbsp <a href=\"#s%ds%d\"> &uarr; </a>" %
                       ( setNumber      if sameSet else setNumber - 1,
                         songNumber - 1 if sameSet else len( setLists[ setNumber - 1 ].songList ) - 1 ) )
            f.write ("</h4>\n")

          # some 'pseudo tags' that can be put in the lyric text
          # You can also just put in html in the txt since we paste it directly.
          elif line[ : 2 ] == "t!":
            toggleTab( f )
          elif line[ : 2 ] == "s!":
            f.write( "<b><font style=\"font-family:courier;\" size=\"2\">&nbsp Solo</font></b><br>\n" )
          elif line[ : 2 ] == "c!": # chorus
            f.write( "<b><font style=\"font-family:courier;\" size=\"2\">&nbsp Chorus</font></b><br>\n" )
          # ignore 2nd line if empty. It's unnecessary space in the html
          elif fileLine > 1 or line != "\n":
            # add spaces
            while line[ 0 ] == " ":
              line = line[ 1 : ]
              f.write( "&nbsp" )
            f.write( "%s<br>\n" % ( line.rstrip() ) )

          fileLine += 1
      except:
        print( "Exception.." )
      songNumber += 1
    setNumber += 1
  f.write( "</body></html>\n" )
  f.close()
  statusString = "Export complete."

def scanForNew():
  # scan the current directory and add any songs to Unassigned
  global statusString

  def songIsPresent( s ):
    for l in setLists:
      for sng in l.songList:
        if sng.name == s.name:
          return True
    for c in clipboard:
      if c.name == s.name:
        return True
    return False

  added = 0

  u = getSetByName( unassignedSetName ).songList
  l = getLocalSongs()
  # see if songs are not present
  for s in l:
    if songIsPresent( s ) == False:
      u.append( s )
      added += 1

  statusString = "Scan complete"
  if added:
    statusString += ", %d added" % ( added )
  else:
    statusString += "."

# start with all the local txt files.
s = getSetByName( unassignedSetName )
s.songList = getLocalSongs()

displayUI()
while True:
  ch = getInput()
  if ch == "DOWN" or ch == "j":
    songFwd( SONG_COLUMNS )
  elif ch == "RIGHT" or ch == "l":
    songFwd( 1 )
  elif ch == "UP" or ch == "k":
    songBack( SONG_COLUMNS )
  elif ch == "LEFT" or ch == "h":
    songBack( 1 )
  elif ch == 'A':
    alphabetize()
  elif ch == 's':
    if len( clipboard ):
      statusString = "Can't save with songs in clipboard."
    else:
      saveList()
  elif ch == 'o':
    loadSetList()
  elif ch == 'r':
    setListName = raw_input( 'Enter set list name:' )
  elif ch == 'm':
    if currentSong == None:
      statusString = "No song selected."
    elif inputMode == MODE_MOVE:
      inputMode = MODE_NORMAL
    else:
      inputMode = MODE_MOVE
  elif ch == 'a':
    if currentSet == MAX_SETS:
      statusString = "Max sets exceeded."
    else:
      addSet ()
  elif ch == 'd':
    deleteSet()
  elif ch == 'c' and inputMode == MODE_NORMAL:
    cutSongToClipboard()
  elif ch == 'p':
    pasteClipboard()
  elif ch == 'x':
    exportSet ()
  elif ch == 'R':
    cutSong ()
  elif ch == 'n':
    if currentSet == len( setLists ) - 1:
      statusString = "Can't rename Unassigned group."
    else:
      sName = raw_input( 'Enter set name:' )
      setLists[ currentSet ].name = sName
  elif ch == 'S':
    scanForNew()
  elif ch == 'q':
    exit()
  elif ch >= '1' and ch <= '9':
    moveToSet( int( ch ) - 1 )
  elif ch == '?' or ch == 'h':
    print( helpString )

    foo = getInput()

  displayUI()
