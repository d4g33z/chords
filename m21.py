from copy import copy 

import numpy as npy
from music21 import serial,harmony,pitch

m21_spellingMap = {names[0] if names[0] is not '' else 'M':
                       tuple(['R'] + intstr.split(',')[1:]) for chord_name,(intstr,names) in harmony.CHORD_TYPES.items()}

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
    6:('-5','#11'),
    7:('5',),
    8:('-6','#5',),
    9:('13','--7'),
    10:('-7','#6'),
    11:('7',) },
    #use if spelling in extChords

  }

def mode_push(scale,n = 1):
  pushed = tuple(map(lambda x:x - scale[0],scale[1:])) + (12 - scale[0],)
  if n == 1:
      return ('R',) + tuple(map(lambda x:m21_intervals[0][x][0],pushed))
  else:
    return mode_push(pushed,n-1)

ionian = (2,4,5,7,9,11)
mode_names = ('ionian','dorian','phrygian','lydian','mixolodian','aeolian','locrian')
m21_modeMap = dict(zip(mode_names,[('R',) + tuple(map(lambda x:m21_intervals[0][x][0],ionian))] + [mode_push(ionian,i) for i in range(1,7)]))

mkint = lambda x:harmony.interval.Interval(x)
iadd = lambda x,y:harmony.interval.add([x,y])

m21_intervalMap = {mkint(i).niceName:('R',m21_intervals[0][mkint(i).chromatic.semitones][0]) for i in range(11)}

#mix the modes and the chords
m21_spellingMap = { **m21_spellingMap, **m21_modeMap }
m21_chord_names = { **m21_chord_names, **dict(zip(mode_names,map(lambda x:x[:3],mode_names)))}

#mix in exotic scales
m21_spellingMap.update({'harmonic minor':('R','2','-3','4','5','-6','7')})
m21_chord_names.update({'harmonic minor':'hm'})

#mix in intervals
m21_spellingMap = { **m21_spellingMap, **m21_intervalMap }
m21_chord_names = { **m21_chord_names, **dict(zip(m21_intervalMap.keys(),m21_intervalMap.keys())) }

m21_spellings = list(m21_spellingMap.keys())

m21_extChords=('M9', '9', 'mM9', 'm9', '+M9', '9#5', '/o9', '/ob9', 'o9', 'ob9', '11', 'M11', 'mM11', 'm11', '+M11', '+11', '/o11', 'o11', 'M13', '13', 'mM13', 'm13', '+M13', '+13', '/o13')
m21_extIntervals = ( '9', '-9', '#9', '11','-11', '13' )
m21_minorSpellings = ( 'm', 'm7', 'm9', 'm11', 'm13','hm','dorian','phrygian','aeolian','locrian')



all_ints = [mkint(i) for i in range(12)]

unisons = [mkint(0)]
seconds = [mkint(1),mkint(2),mkint(10),mkint(11)]
thirds = [mkint(3),mkint(4),mkint(8),mkint(9)]
fourths = [mkint(5),mkint(6),mkint(7)]

#interval class model
us = [0]
ss = [1,2]
ts = [3,4]
fs = [5,6]

from itertools import product

all_iadd = lambda x,y:sorted(list(map(lambda x:iadd(*x),product(x,y))),key=lambda i:i.chromatic.semitones)

all_nice_names = lambda y:list(map(lambda x:x.simpleNiceName,y))

def show_table(ints1,ints2):
    all_added_ints = []
    for x,y in product(ints1,ints2):
      all_added_ints.append((x,y,iadd(x,y)))

    for x,y,z in sorted(all_added_ints,key = lambda x:x[2].chromatic.semitones):
      print("{} + {} = {}".format(x.niceName,y.niceName,iadd(x,y).simpleNiceName))
    return all_added_ints

def show_ic_table(ints1,ints2):
    all_added_ints = []
    for x,y in product(ints1,ints2):
      all_added_ints.append((x,y,iadd(x,y)))

    for x,y,z in sorted(all_added_ints,key = lambda x:x[2].chromatic.semitones):
      print("{} + {} = {}".format(x.chromatic.intervalClass,y.chromatic.intervalClass,iadd(x,y).chromatic.intervalClass))
    return all_added_ints

