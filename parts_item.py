import json
import reapy
import random
from reapy import reascript_api as RPR
# from graph_from_edges import generate_measures
from song_library import SongPart
from typing import Dict, List
from pydash import _, uniq
from reapy.core.track.track import Track
from replicate_parts import poolGroupItems

import song_library


def rprint(msg):
    with reapy.reaprint():
        print(msg)


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
            tk: reapy.Take = mi.active_take

            if(track.name == 'Lead'):
                part_notes = []
                p = refregions[idx].name

                if 'Pre-Chorus' in p:
                    sp = 'prechorus_'
                elif 'Chorus' in p:
                    sp = 'chorus_'
                elif 'Pre-Verse' in p:
                    sp = 'preverse_'
                elif 'Verse' in p:
                    sp = 'verse_'
                else:
                    sp = 'measure_'

                fileName = "s:\\dev\\" + sp + str(int(end - start)) + ".json"
                with open(fileName) as infile:
                    part_notes = json.load(infile)

                current = 0.0
                for measure in part_notes:
                    for noteOrRest in measure:
                        if(noteOrRest < 0):
                            tk.add_note(current, current + noteOrRest, 64, 0, 0,
                                        False, True, "beats", True)
                            # The note is a rest, leave a positive space open
                            current = current + (noteOrRest * -1)
                        elif (noteOrRest > 0):
                            # This is a note

                            # Choose pitches in the C Maj. scale
                            pitch = random.choice([60, 62, 64, 65,
                                                   67, 69, 71, 72])
                            tk.add_note(current, current + noteOrRest, pitch, 100, 0,
                                        False, False, "beats", True)
                            current = current + noteOrRest
                # 40038 - File: Export contents as .MID

            # newTk: reapy.Take = RPR.GetSetMediaItemTakeInfo_String(
            #     tk, 'P_NAME', track.name + ' - ' + refregions[idx].name, 1)
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
