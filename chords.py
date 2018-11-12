#!/usr/bin/python

'''
Chord Utility
by Greg Girardin
   Nashua NH
   girardin1972@hotmail.com

   I wrote everything except for the getInput function.

   These chord generators have existed for many years,
   but I wanted one I could easily configure the way I wanted.
'''

# from __future__ import print_function
import os
import sys

from m21 import m21_chord_names,m21_spellings,m21_intervals,m21_spellingMap,m21_extChords

instrumentMap = \
  {
  'Mandolin' :   { "t": ( "E", "A", "D", "G" ),           "f" : ( 0, 0, 0, 0 ) },
  'Guitar' :     { "t": ( "E", "B", "G", "D", "A", "E" ), "f" : ( 0, 0, 0, 0, 0, 0 ) },
  'Dropped D' :  { "t": ( "E", "B", "G", "D", "A", "D" ), "f" : ( 0, 0, 0, 0, 0, 0 ) },
  'Bass' :       { "t": ( "G", "D", "A", "E" ),           "f" : ( 0, 0, 0, 0 ) },
  '5Bass' :      { "t": ( "G", "D", "A", "E", "B" ),      "f" : ( 0, 0, 0, 0, 0 ) },
  'Uke' :        { "t": ( "A", "E", "C", "G" ),           "f" : ( 0, 0, 0, 0 ) },
  'Banjo' :      { "t": ( "D", "B", "G", "D", "G" ),      "f" : ( 0, 0, 0, 0, 5 ) },
  'RGuitar' :    { "t": ( "E", "B", "G", "D", "A", "E" ), "f" : ( 0, 0, 1, 1, 1, 1 ) },
  }

# pick the instruments you care about
instruments = ('RGuitar','Guitar', 'Bass', 'Uke', 'Mandolin', 'Dropped D', '5Bass')

# display with a #/b if that's how we'd display the major key.
dispKeyList    = ( 'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B' )
keyListSharps  = ( 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' )
keyListFlats   = ( 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' )
bKeys          = ( 'F', 'Bb', 'Eb','Ab', 'Db' ) # keys to be displayed as having flats

minorSpellings = ( 'm', 'm7', 'm9', 'm11', 'm13', 'm-Key' )

NUM_FRETS = 13

def showWithSharps( key, spelling ):
  # return True if we should show this key/spelling as having sharps (vs flats)

  def relMajor( key ):
    # input is a minor key, returns the relative major key
    index = dispKeyList.index( key )
    index += 3
    index %= 12
    key = dispKeyList[ index ]
    return key

  if spelling in minorSpellings:
    key = relMajor( key )

  return key not in bKeys

def calcNote( root, fret ):
  rootNum = dispKeyList.index( root )
  rootNum += fret
  rootNum %= 12

  return dispKeyList[ rootNum ]

def calcInterval( note, key ):
  noteNum = dispKeyList.index( note ) + 12 # C = 12, C# = 13, etc
  keyNum = dispKeyList.index ( key )       # C = 0, C# = 1
  intNum = ( noteNum - keyNum ) % 12       # (if C) C = 0, C# = 1

  return intNum

def m21_fretInfoGen( root, fret, fretOffset, key, spelling ):
  '''
  Generate a dictionary entry about the given fret.
  root is the string's fretOffset fret note. Usually fret 0 (open).
  fret is the fret number relative to a zero offset string
  note is the text of the note
  '''
  assert fret >= fretOffset, "Fret below fret offset."

  fretInfo = {
    'root' : root,
    'fret' : fret,
    'note' : calcNote( root, fret - fretOffset )
  }

  interval = calcInterval( fretInfo ['note'], key )

  x = 1 if spelling in m21_extChords else 0

  fretInfo[ 'interval' ] = m21_intervals[ x ][ interval ]
  fretInfo[ 'inSpelling' ] = \
    any(i in m21_spellingMap[ spelling ] for i in m21_intervals[ x ][ interval ])

  # convert note for display
  if showWithSharps( key, spelling ):
    curKeyList = keyListSharps
  else:
    curKeyList = keyListFlats

  fretInfo[ 'note' ] = curKeyList[ dispKeyList.index( fretInfo[ 'note' ] ) ]

  return fretInfo

def m21_generateFretboard( inst, key, spelling ):
  '''
  Returns a dictionary with everything we care about
  strings are keyed by string number (1 - N) and contain a list of dictionaries for each fret
  There are also some other 'global' kinda things.. numStrings, instrument, etc.

  TBD: This should be removed. There is no reason to generate the fretboard in advance,
  just generate frets on the fly while displaying.
  '''

  strings = instrumentMap[ inst ][ 't' ]

  fretBoard = {
                'numStrings' : len ( strings ),
                'instrument' : inst,
                'spelling'   : spelling,
                'fretOffset' : instrumentMap[ inst ][ 'f' ]
              }

  for string in range ( 1, len ( strings ) + 1 ):
    stringList = []
    rootNote = strings[ string - 1 ]
    offset = instrumentMap[ inst ][ 'f' ][ string - 1 ]

    for fret in range ( offset, NUM_FRETS + 1 ):
      fretInfo = m21_fretInfoGen( rootNote, fret, offset, key, spelling )
      stringList.append( fretInfo )

    fretBoard [string] = stringList

  return fretBoard

def m21_displayFretboard( fretboard, interval = False ):
  numStrings = fretboard[ 'numStrings' ]

  print( "\n  ", end = "" )
  for fret in range ( 0, NUM_FRETS + 1 ):
    print( "%2s   " % fret, end = "" )
    if fret == 9: # formatting hack
      print( " ", end="" )

  print()
  for stringNum in range( 1, numStrings + 1 ):
    string = fretboard[ stringNum ]

    print( string[ 0 ][ 'note' ], " ", end = "", sep = "" )
    print( "     " * fretboard[ 'fretOffset' ][ stringNum - 1 ], end = "" )

    for fret in string:
      if fretboard[ 'fretOffset' ][ stringNum - 1 ] == fret[ 'fret' ]:
        fretChar = "x"
      else:
        fretChar = "|"

      if fret[ 'inSpelling' ]:
        if interval:
          value = fret[ 'interval' ][0].replace('-','b') \
            if fret['interval'][0] in m21_spellingMap[fretboard['spelling']] else fret[ 'interval' ][1].replace('-','b')
        else:
          value = fret[ 'note' ]

        if len( value ) == 1:
        # value += "-"
          value += "--"
        elif len( value ) == 2:
          value += "-"

        # print( "-%s-%s" % ( value, fretChar ), end = "", sep='' )
        print( "-%s%s" % ( value, fretChar ), end = "", sep='' )
      else:
        print( "----%s" % fretChar, end = "" )
    print ()

def m21_displayInfo( instrument, key, spelling ):
  os.system( 'clear' )

  fretboard = m21_generateFretboard( instrument, key, spelling )

  print( fretboard[ 'instrument' ], key, m21_chord_names[spelling],'('+fretboard[ 'spelling' ]+')')
  m21_displayFretboard( fretboard )
  m21_displayFretboard( fretboard, True )
  print ()

  # help
  print( "i : Instruments: ", end="" )
  for inst in instruments:
    print( inst, "", end = "" )
  print()
  print( "[] : Cycle Spellings ", end="" )
  # for spel in m21_spellings:
  #   print(spel, "", end="" )
  print()
  print( "a..g -= : Key" )
  print( "q : quit" )

def getInput ():
  """
  Copied from http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
  """
  import termios, fcntl, sys, os
  fd = sys.stdin.fileno()
  flags_save = fcntl.fcntl( fd, fcntl.F_GETFL )
  attrs_save = termios.tcgetattr( fd )
  attrs = list( attrs_save )
  attrs[ 0 ] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK | termios.ISTRIP | termios.INLCR |
                  termios.IGNCR | termios.ICRNL | termios.IXON )
  attrs[ 1 ] &= ~termios.OPOST
  attrs[ 2 ] &= ~(termios.CSIZE | termios.PARENB)
  attrs[ 2 ] |= termios.CS8
  attrs[ 3 ] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN )
  termios.tcsetattr( fd, termios.TCSANOW, attrs)
  fcntl.fcntl( fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK )
  try:
    ret = sys.stdin.read( 1 )
  except KeyboardInterrupt:
    ret = 0
  finally:
    termios.tcsetattr( fd, termios.TCSAFLUSH, attrs_save )
    fcntl.fcntl( fd, fcntl.F_SETFL, flags_save )
  return ret


def m21_runCli ():
  keyIx = 0
  instrumentIx = 0
  spellingIx = 0

  os.system( 'clear' )
  while True:
    m21_displayInfo( instruments[ instrumentIx ], dispKeyList[ keyIx ], m21_spellings[ spellingIx ] )

    ch = getInput ()
    if ch == 'q':
      exit()
    elif ch == 'i':
      instrumentIx += 1
      instrumentIx %= len( instruments )
    elif ch == ']':
      spellingIx += 1
      spellingIx %= len( m21_spellings )
    elif ch == '[':
      if spellingIx > 0:
        spellingIx -= 1
      else:
        spellingIx = len( m21_spellings ) - 1
    elif ch == '=':
      keyIx += 1
      keyIx %= len( dispKeyList )
    elif ch == '-':
      if ( keyIx > 0 ):
        keyIx -= 1
      else:
        keyIx = len( dispKeyList ) - 1
    # elif ch == 'm':
    #   spellingIx = spellings.index( 'M-Key' )
    # elif ch == 'r':
    #   spellingIx = spellings.index( 'm-Key' )
    # elif ch == '7':
    #   spellingIx = spellings.index( '7' )
    elif ch.upper() in dispKeyList:
      keyIx = dispKeyList.index( ch.upper() )

import time
def runAnimation():
  my_spellings = ( 'M',  'm',   '2', '4', '6', 'm6',
                  '7',  'm7',  'M7',
                  '9',  'm9',  'M9',
                  '11', 'm11', 'M11',
                  '13', 'm13', 'M13',)
  chord_sequence = list(zip(('C',)*len(my_spellings),my_spellings))

  chord_sequence = ('CM7','Dm7','Em7','FM7','G7','Am7','Bdim')
  fretboards = list(zip(chord_sequence,tuple(map(lambda x:generateFretboard( 'RGuitar', *x),chord_sequence))))
  i=0
  while True:
    chord, fretboard = fretboards[i%len(fretboards)]
    os.system( 'clear' )
    print( fretboard[ 'instrument' ], chord[0], fretboard[ 'spelling' ] )

    displayFretboard( fretboard )
    displayFretboard( fretboard, True )

    time.sleep(1)
    i += 1



if __name__ == '__main__':
  m21_runCli()
