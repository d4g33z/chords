from copy import copy 

import numpy as npy
from music21 import serial,harmony,pitch

m21_spellingMap = {names[0] if names[0] is not '' else 'M':
                       tuple(['R'] + intstr.split(',')[1:]) for key,(intstr,names) in harmony.CHORD_TYPES.items()}

m21_chord_names = {names[0] if names[0] is not '' else 'M':
                        chord_name for chord_name,(intstr,names) in harmony.CHORD_TYPES.items()}

m21_intervals = \
  {
    #use if spelling not in extChords
  0 : {
    0:('R',),
    1:('-2',),
    2:('2',),
    3:('-3',),
    4:('3',),
    5:('4',),
    6:('-5','#4'),
    7:('5',),
    8:('-6','#5'),
    9:('6','--7'),
    10:('-7','#6'),
    11:('7',) },
    #use if spelling in extChords
  1 : {
    0:('R',),
    1:('-9',),
    2:('9',),
    3:('-3','#9'),
    4:('3',),
    5:('11',),
    6:('-5','#4'),
    7:('5',),
    8:('-6','#5',),
    9:('13',),
    10:('-7',),
    11:('7',) },
    #use if spelling in extChords

  }

m21_spellings = list(m21_spellingMap.keys())

m21_extChords=('M9', '9', 'mM9', 'm9', '+M9', '9#5', '/o9', '/ob9', 'o9', 'ob9', '11', 'M11', 'mM11', 'm11', '+M11', '+11', '/o11', 'o11', 'M13', '13', 'mM13', 'm13', '+M13', '+13', '/o13')
m21_extIntervals = ( '9', '-9', '#9', '11','-11', '13' )
m21_minorSpellings = ( 'm', 'm7', 'm9', 'm11', 'm13')


