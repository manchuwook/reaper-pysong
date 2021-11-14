import argparse
import sys
import logging
import random
import math
import reapy
from pydash import chain, for_each
from reapy.core.track.track import Track
from colors import randColorByHue
from reapy import reascript_api as RPR


def rprint(msg):
    with reapy.reaprint():
        print(msg)


battery = 'Battery 4 (x86)'
chordPotion = 'ChordPotion'
melodicFlow = 'MelodicFlow'
reaSynth = 'ReaSynth'
reaComp = 'ReaComp'
reaEq = 'ReaEQ'

# region Captain Composer Plug-ins
captainMelody = 'Captain Melody (Mixed In Key LLC)'
captainDeep = 'Captain Deep (Mixed In Key LLC)'
captainBeat = 'Captain Beat (Mixed In Key LLC)'
captainChords = 'Captain Chords (Mixed In Key LLC)'
# endregion

# region Orb Option
orbArp = 'Orb Arpeggios'
orbBass = 'Orb Bass'
orbChords = 'Orb Chords'
orbMelody = 'Orb Melody'
# endregion


def extendTrack(track: reapy.Track, idx: int, collection: reapy.TrackList):
    """Add Processing or Composition FX, output routing"""
    tVol: float = track.get_info_value('D_VOL')
    track.set_info_value('D_VOL', tVol * 0.5)

    track.color = randColorByHue('red')
    # region Orb Composer
    if track.name == 'Chords - Orb':
        oChords = track.add_fx(name=orbChords)
    if track.name == 'Arpeggio - Orb':
        oArp = track.add_fx(name=orbArp)
    if track.name == 'Bass - Orb':
        oBass = track.add_fx(name=orbBass)
    if track.name == 'Harmony - Orb':
        oHarmony = track.add_fx(name=orbMelody)
    if track.name == 'Melody - Orb':
        oMelody = track.add_fx(name=orbMelody)
    # endregion
    # region Captain Composer (Default)
    if track.name == 'Melody':
        cptMelody = track.add_fx(name=captainMelody)
    if track.name == 'Bass':
        cptDeep = track.add_fx(name=captainDeep)
    if track.name == 'Arpeggio':
        cp = track.add_fx(name=chordPotion)
        rSynth = track.add_fx(name=reaSynth)
    if track.name == 'Chords - Scratch':
        cptChords = track.add_fx(name=captainChords)
        track.add_send(destination=track.project.tracks['Chords'])
        track.add_send(destination=track.project.tracks['Arpeggio'])
        track.select()
        RPR.ReorderSelectedTracks(0, 0)
        track.unselect()
    # endregion

    if track.name == 'Percussion':
        btry = track.add_fx(name=battery)

    # region Do stuff to other tracks
    # if track.name in ['FX', 'FX1', 'FX2', 'FX3']:
    # if track.name == 'Harmony':
    # if track.name == 'Lead':
    # if track.name == 'Pad':
    # if track.name == 'Rhythmic':
    # if track.name == 'Sub':
    # endregion

    for idx, fx in enumerate(track.fxs):
        xFx: reapy.FX = fx
        fxParams: reapy.FXParamsList = xFx.params
    track.add_fx(name=reaComp)
    track.add_fx(name=reaEq)

    return track


def makeTracks(project: reapy.Project, composer='Captain'):
    if(composer == 'Captain'):
        tracks = [
            'Chords - Scratch', 'Chords', 'Arpeggio',
            'Bass', 'Ambient', 'Sub', 'Pad',
            'Lead', 'FX1', 'FX2', 'FX3', 'Rhythmic',
            'Percussion', 'Harmony', 'Melody'
        ]
    if(composer == 'Orb'):
        tracks = [
            'Chords - Orb', 'Chords', 'Arpeggio - Orb',
            'Bass - Orb', 'Ambient', 'Sub', 'Pad',
            'Lead', 'FX1', 'FX2', 'FX3', 'Rhythmic',
            'Percussion', 'Harmony - Orb', 'Melody - Orb'
        ]
    tracks.reverse()

    trackList: list = list()
    for idx, track in enumerate(tracks):
        t = project.add_track(name=track)
        tr: Track = extendTrack(t, idx, project.tracks)
        trackList.append(tr)

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

    return trackList
