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

pmin = pitch.Pitch('C#2').diatonicNoteNum
pmax = pitch.Pitch('D6').diatonicNoteNum
tuning = [5,5,5,5,5] #six strings seperated by p4ths mutually 
capo = [1,1,1,1,0,0] #capo!

#merge n dicts
def merged(*args):
    def merge_dicts(d1,d2):
        assert all([k not in d2.keys() for k in d1.keys()]) #disjoint keysets
        return {k: v for d in (d1, d2) for k, v in list(d.items())}
    d = {}
    for arg in args:
        d = merge_dicts(arg,d)
    return d

#make all data vectors the same length with placeholder None for bokeh ColumnDataSource
def normalize(data):
    n = max(map(len,data.values()))
    return {key:value+[None]*(n-len(value)) for key,value in data.items()}


#construct data for init_source
chromatic = serial.pcToToneRow(range(0,12))

roots = chromatic.noteNames() 
symbols = ['', 'm', '+', 'dim', '7',
        'M7', 'm7', 'dim7', '7+', 'm7b5',
        'mM7', '6', 'm6', '9', 'Maj9', 'm9',
        '11', 'Maj11', 'm11', '13',
        'Maj13', 'm13', 'sus2', 'sus4',
        ]

#diatonic note number chords for all roots and symbols
to_intervals = lambda x:npy.cumsum(npy.diff(x))
# chord_symbol_to_intervals = lambda y:list(filter(lambda x:x is not None,
#                                 map(y.intervalFromChordStep,range(1,len(y.pitches)+24))))

chord_symbol_to_intervals = lambda y:list(filter(lambda x:x is not None,
                                map(y.semitonesFromChordStep,range(1,23))))

# chord_pitches = {root+symbol:[p for p in harmony.ChordSymbol(root+symbol).pitches] \
#             for symbol in symbols for root in roots}
# #
# chord_numbers = {root+symbol:[p.diatonicNoteNum for p in harmony.ChordSymbol(root+symbol).pitches] \
#             for symbol in symbols for root in roots}
#
# chords2 = {root+symbol:harmony.ChordSymbol(root+symbol).pitches \
#             for symbol in symbols for root in roots}


# chord_intervals = {root+symbol:chord_symbol_to_intervals(harmony.ChordSymbol(root+symbol)) \
#             for symbol in symbols for root in roots}

# all_chord_intervals = {root+symbol:list(map(lambda x:x.chromatic.semitones,chord_symbol_to_intervals(harmony.ChordSymbol(root+symbol)))) \
#             for symbol in symbols for root in roots}


# chord_intervals = {symbol if symbol != '' else 'M':list(map(lambda x:x.chromatic.semitones,
#             chord_symbol_to_intervals(harmony.ChordSymbol('C'+symbol)))) \
#             for symbol in symbols}

chord_intervals = { symbol if symbol != '' else 'M':
                        chord_symbol_to_intervals(harmony.ChordSymbol('C'+symbol)) \
                        for symbol in symbols}

intervals_to_names = {
    0   : 'R',
    1   : 'b2',
    2   : '2',
    3   : 'b3',
    4   : '3',
    5   : '4',
    6   : 'b5',
    7   : '5',
    8   : 'b6',
    9   : '6',
    10  : 'b7',
    11  : '7',
    12  : 'R',
    13  : 'b9',
    14  : '9',
    15  : 'b3',
    16  : '3',
    17  : '11',
    18  : 'b5',
    19  : '5',
    20  : 'b13',
    21  : '13',
    22  : 'b7',
    23  : '7'
}

chord_symbols = {symbol:list(map(lambda x:intervals_to_names.get(x),intervals)) for symbol,intervals in chord_intervals.items()}
