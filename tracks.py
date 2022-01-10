import argparse
import sys
import logging
import random
import math
import reapy
from tkinter import *
from enum import Enum
from pydash import chain, for_each
from reapy.core.track.track import Track
from colors import randColorByHue
from reapy import reascript_api as RPR


def rprint(msg):
    with reapy.reaprint():
        print(msg)


class TrackType(Enum):
    AMBIENT = 'Ambient'
    ARPEGGIO = 'Arpeggio'
    BASS = 'Bass'
    CHORDS = 'Chords'
    CHORDS_SCRATCH = 'Chords - Scratch'
    FX1 = 'FX1'
    FX2 = 'FX2'
    FX3 = 'FX3'
    HARMONY = 'Harmony'
    IMITONE = 'Imitone'
    LEAD = 'Lead'
    MELODY = 'Melody'
    PAD = 'Pad'
    PERCUSSION = 'Percussion'
    RISE_AND_HIT = 'Rise and Hit'
    RHYTHMIC = 'Rhythmic'
    SUB = 'Sub'


BATTERY = 'Battery 4 (Native Instruments GmbH) (32 out)'
CHORDPOTION = 'ChordPotion'
MELODICFLOW = 'MelodicFlow'
REASYNTH = 'ReaSynth'
REACOMP = 'ReaComp'
REAEQ = 'ReaEQ'

# Libraries would need to be set in Kontakt after loading
KONTAKT = 'Kontakt (Native Instruments) (64 out)'

# region Captain Composer Plug-ins
CAPTAINBEAT = 'Captain Beat (Mixed In Key LLC)'
CAPTAINCHORDS = 'Captain Chords (Mixed In Key LLC)'
CAPTAINDEEP = 'Captain Deep (Mixed In Key LLC)'
CAPTAINMELODY = 'Captain Melody (Mixed In Key LLC)'
# endregion

# region Orb Option
ORBARP = 'Orb Arpeggios'
ORBBASS = 'Orb Bass'
ORBCHORDS = 'Orb Chords'
ORBMELODY = 'Orb Melody'
# endregion


def extendTrack(track: reapy.Track, idx: int, collection: reapy.TrackList):
    """Add Processing or Composition FX, output routing"""
    tVol: float = track.get_info_value('D_VOL')
    track.set_info_value('D_VOL', tVol * 0.5)

    track.color = randColorByHue('green')

    # region Orb Composer
    if track.name == 'Chords - Orb':
        oChords = track.add_fx(name=ORBCHORDS)
    elif track.name == 'Arpeggio - Orb':
        oArp = track.add_fx(name=ORBARP)
    elif track.name == 'Bass - Orb':
        oBass = track.add_fx(name=ORBBASS)
    elif track.name == 'Harmony - Orb':
        oHarmony = track.add_fx(name=ORBMELODY)
    elif track.name == 'Melody - Orb':
        oMelody = track.add_fx(name=ORBMELODY)
    # endregion

    # region Captain Composer (Default)
    elif track.name == 'Melody':
        cptMelody = track.add_fx(name=CAPTAINMELODY)
    elif track.name == 'Bass':
        cptDeep = track.add_fx(name=CAPTAINDEEP)
    elif track.name == 'Arpeggio':
        cp = track.add_fx(name=CHORDPOTION)
        rSynth = track.add_fx(name=REASYNTH)
    elif track.name == 'Chords - Scratch':
        cptChords = track.add_fx(name=CAPTAINCHORDS)
        track.add_send(destination=track.project.tracks['Chords'])
        track.add_send(destination=track.project.tracks['Arpeggio'])
        track.add_send(destination=track.project.tracks['Imitone'])
        track.select()
        RPR.ReorderSelectedTracks(0, 0)
        track.unselect()
    # endregion

    elif track.name == 'Percussion':
        btry = track.add_fx(name=BATTERY)

    # region Do stuff to other tracks
    # elif track.name in ['FX', 'FX1', 'FX2', 'FX3']:
    # elif track.name == 'Harmony':
    # elif track.name == 'Lead':
    # elif track.name == 'Pad':
    # elif track.name == 'Rhythmic':
    # elif track.name == 'Sub':
    # endregion

    elif track.name == 'Imitone':
        track.add_fx(name=MELODICFLOW)
        track.add_fx(name=REASYNTH)

    else:
        track.add_fx(name=REACOMP)
        track.add_fx(name=REAEQ)

    return track


def makeTracks(project: reapy.Project, composer='Captain'):
    if(composer == 'Captain'):
        tracks = [
            'Chords - Scratch', 'Chords', 'Arpeggio',
            'Bass', 'Sub', 'Pad', 'Lead',
            'FX1', 'FX2', 'FX3', 'Rhythmic',
            'Percussion', 'Harmony', 'Melody', 'Imitone'
        ]
    if(composer == 'Orb'):
        tracks = [
            'Chords - Orb', 'Chords', 'Arpeggio - Orb',
            'Bass - Orb', 'Sub', 'Pad', 'Lead',
            'FX1', 'FX2', 'FX3', 'Rhythmic',
            'Percussion', 'Harmony - Orb', 'Melody - Orb', 'Imitone'
        ]
    tracks.reverse()

    trackList: list = list()
    def add_track(value): return project.add_track(name=value)
    def extend_track(value, idx): return extendTrack(
        value, idx, project.tracks)

    def watch_track(value): trackList.append(value)
    chain(
        tracks
    ).map(
        add_track
    ).map(
        extend_track
    ).tap(
        watch_track
    ).value()

    # Get the first FX1 for insert
    fx1 = project.tracks['FX1']
    # Add the FX track above FX1
    fx = project.add_track(fx1.index, 'FX')
    # Add the other FX tracks
    fx2 = project.tracks['FX2']
    fx3 = project.tracks['FX3']

    # Select the tracks to move
    fx1.select()
    fx2.select()
    fx3.select()

    # Reorder and move to the FX track (as a folder)
    RPR.ReorderSelectedTracks(fx1.index, 1)

    project.unselect_all_tracks()

    # for idx in range(16):
    #     if(idx == 0):
    #         kTrack = project.add_track(name='Kontakt 1')
    #         kFolder = project.add_track(index=kTrack.index, name='Kontakt')
    #     else:
    #         kTrack = project.add_track(name='Kontakt ' + str(idx + 1))

    #     watch_track(kTrack)
    #     kTrack.select()

    # Reorder and move to the Kontakt track (as a folder)
    # RPR.ReorderSelectedTracks(kFolder.index, 1)

    return trackList
