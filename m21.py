from copy import copy 

import numpy as npy
from music21 import serial,harmony,pitch

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
chord_symbol_to_intervals = lambda y:list(filter(lambda x:x is not None,
                                map(y.intervalFromChordStep,range(1,len(y.pitches)+24))))

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

chord_intervals = {root+symbol:list(map(lambda x:x.chromatic,chord_symbol_to_intervals(harmony.ChordSymbol(root+symbol)))) \
            for symbol in symbols for root in roots}



