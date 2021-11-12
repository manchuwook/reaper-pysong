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
    """Add Processing or Composition FX, set icons, output routing"""
    tVol: float = track.get_info_value('D_VOL')
    track.set_info_value('D_VOL', tVol * 0.5)

    track.color = randColorByHue('red')
    # region Orb Composer
    if track.name == 'Chords - Orb':
        track.set_info_string('P_ICON', 'piano.png')
        oChords = track.add_fx(name=orbChords)
    if track.name == 'Arpeggio - Orb':
        track.set_info_string('P_ICON', 'harp.png')
        oArp = track.add_fx(name=orbArp)
    if track.name == 'Bass - Orb':
        track.set_info_string('P_ICON', 'bass.png')
        oBass = track.add_fx(name=orbBass)
    if track.name == 'Harmony - Orb':
        track.set_info_string('P_ICON', 'female_head.png')
        oHarmony = track.add_fx(name=orbMelody)
    if track.name == 'Melody - Orb':
        track.set_info_string('P_ICON', 'male_head.png')
        oMelody = track.add_fx(name=orbMelody)
    # endregion
    # region Captain Composer (Default)
    if track.name == 'Melody':
        track.set_info_string('P_ICON', 'male_head.png')
        cptMelody = track.add_fx(name=captainMelody)
    if track.name == 'Bass':
        track.set_info_string('P_ICON', 'bass.png')
        cptDeep = track.add_fx(name=captainDeep)
    if track.name == 'Arpeggio':
        track.set_info_string('P_ICON', 'harp.png')
        cp = track.add_fx(name=chordPotion)
        rSynth = track.add_fx(name=reaSynth)
    if track.name == 'Chords - Scratch':
        track.set_info_string('P_ICON', 'piano.png')
        cptChords = track.add_fx(name=captainChords)
        track.add_send(destination=track.project.tracks['Chords'])
        track.add_send(destination=track.project.tracks['Arpeggio'])
        track.select()
        RPR.ReorderSelectedTracks(0, 0)
        track.unselect()
    # endregion

    if track.name == 'Percussion':
        track.set_info_string('P_ICON', 'drums.png')
        btry = track.add_fx(name=battery)

    # region Set only icons
    if track.name in ['FX', 'FX1', 'FX2', 'FX3']:
        track.set_info_string('P_ICON', 'synthbass.png')
    if track.name == 'Harmony':
        track.set_info_string('P_ICON', 'female_head.png')
    if track.name == 'Lead':
        track.set_info_string('P_ICON', 'guitar.png')
    if track.name == 'Pad':
        track.set_info_string('P_ICON', 'pads.png')
    if track.name == 'Rhythmic':
        track.set_info_string('P_ICON', 'cowbell.png')
    if track.name == 'Sub':
        track.set_info_string('P_ICON', 'double_bass.png')
    # endregion

    for idx, fx in enumerate(track.fxs):
        xFx: reapy.FX = fx
        fxParams: reapy.FXParamsList = xFx.params
    track.add_fx(name=reaComp)
    track.add_fx(name=reaEq)

    return track


def makeTracks(project: reapy.Project, composer='Captain'):
    if(composer == 'Captain'):
        tracks = ['Chords - Scratch', 'Chords', 'Arpeggio', 'Bass', 'Sub', 'Pad',
                  'Lead', 'FX1', 'FX2', 'FX3', 'Rhythmic', 'Percussion', 'Harmony', 'Melody']
    if(composer == 'Orb'):
        tracks = ['Chords - Orb', 'Chords', 'Arpeggio - Orb', 'Bass - Orb', 'Sub', 'Pad',
                  'Lead', 'FX1', 'FX2', 'FX3', 'Rhythmic', 'Percussion', 'Harmony - Orb', 'Melody - Orb']
    tracks.reverse()

    trackList: list = list()
    for idx, track in enumerate(tracks):
        t = project.add_track(name=track)
        tr: Track = extendTrack(t, idx, project.tracks)
        trackList.append(tr)

    # Get the first FX1 and insert a track before it
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
