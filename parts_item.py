import argparse
import enum
import sys
import logging
import random
import math
from song_library import SongPart
from typing import Dict, List
import reapy
from pydash import _, uniq
from reapy.core.track.track import Track
from colors import randColorByHue
from reapy import reascript_api as RPR
from replicate_parts import poolGroupItems

import song_library


def addMidiItems(project: reapy.Project, refregions: List[SongPart]):
    for idx, region in enumerate(project.regions):
        # Even though regions are added in seconds
        # Quantization lets us go back to theory and add items in beats
        start = project.time_to_beats(region.start)
        end = project.time_to_beats(region.end)
        for idx1, track in enumerate(project.tracks):
            # Add a new MIDI item for pooling later
            mi: reapy.Item = track.add_midi_item(start, end, True)

            # Takes don't seem to be getting renamed
            # Possible the P_NAME isn't correct
            tk: reapy.Take = RPR.GetActiveTake(mi)
            newTk: reapy.Take = RPR.GetSetMediaItemTakeInfo_String(
                tk, 'P_NAME', track.name + ' - ' + refregions[idx].name, 1)
            mi.update()

    for idx, track in enumerate(project.tracks):
        # Select the track
        track.select()

        # Starting in the thousands place to have room for growth
        # This is an arbitrary number
        trackGroupId = (idx + 1) * 1000
        for idxMidiItem1, midiItem in enumerate(track.items):
            if(refregions[idxMidiItem1].type == song_library.TypeEnum.PRE_INTRO):
                midiGroupId = trackGroupId + 100
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.INTRO):
                midiGroupId = trackGroupId + 110
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.PRE_VERSE):
                midiGroupId = trackGroupId + 120
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.VERSE):
                midiGroupId = trackGroupId + 130
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.PRE_CHORUS):
                midiGroupId = trackGroupId + 140
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.CHORUS):
                midiGroupId = trackGroupId + 150
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.PRE_BREAKDOWN):
                midiGroupId = trackGroupId + 160
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.BREAKDOWN):
                midiGroupId = trackGroupId + 170
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.BRIDGE):
                midiGroupId = trackGroupId + 180
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.DROP):
                midiGroupId = trackGroupId + 190
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.INSTRUMENTAL):
                midiGroupId = trackGroupId + 200
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.PRE_OUTRO):
                midiGroupId = trackGroupId + 210
            elif(refregions[idxMidiItem1].type == song_library.TypeEnum.OUTRO):
                midiGroupId = trackGroupId + 220
            midiItem.set_info_value('I_GROUPID', midiGroupId)

    poolGroupItems(project)
