import subprocess
import logging
import json
from tkinter import *
from tkinter.ttk import Scale
from tkinterweb import HtmlFrame
import reapy
from song_library import SongLibraryElement, SongPart, song_library_from_dict
from song_structurer import generateStructure
from parts_item import addMidiItems
from tracks import makeTracks
from colors import randColorByHue
from reapy import reascript_api as RPR
import sys
from __init__ import __version__

__author__ = "manchuwook"
__copyright__ = "manchuwook"
__license__ = "mit"

_logger = logging.getLogger(__name__)

project: reapy.Project = reapy.Project()

sys.argv = ['Main']
root = Tk()


def rprint(msg):
    with reapy.reaprint():
        print(msg)


def write_to_console(url, data, method):
    response = data.decode('utf-8')
    items = {}
    for kvpair in response.split('&'):
        kv = kvpair.split('=')
        key, value = kv[0], kv[1]
        items[key] = value
    return items


@reapy.prevent_ui_refresh()
def main():
    # reapy.config.enable_dist_api()
    reapy.print('Creating template')

    frame = HtmlFrame(root)
    frame.load_file('file:///static/index.html')
    # whole_note_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # half_note_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # quarter_note_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # eighth_note_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # sixteenth_note_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # whole_rest_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # half_rest_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # quarter_rest_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # eighth_rest_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)
    # sixteenth_rest_weight = Scale(
    #     master=root, orient='horizontal', from_=-1, to=1, tickinterval=0.0125)

    # frame.replace_element('#wholeNotesWeight', whole_note_weight)
    # frame.replace_element('#halfNotesWeight', half_note_weight)
    # frame.replace_element('#quarterNotesWeight', quarter_note_weight)
    # frame.replace_element('#eighthNotesWeight', eighth_note_weight)
    # frame.replace_element('#sixteenthNotesWeight', sixteenth_note_weight)
    # frame.replace_element('#wholeRestsWeight', whole_rest_weight)
    # frame.replace_element('#halfRestsWeight', half_rest_weight)
    # frame.replace_element('#quarterRestsWeight', quarter_rest_weight)
    # frame.replace_element('#eighthRestsWeight', eighth_rest_weight)
    # frame.replace_element('#sixteenthRestsWeight', sixteenth_rest_weight)

    # whole_note_weight.pack()
    # half_note_weight.pack()
    # quarter_note_weight.pack()
    # eighth_note_weight.pack()
    # sixteenth_note_weight.pack()
    # whole_rest_weight.pack()
    # half_rest_weight.pack()
    # quarter_rest_weight.pack()
    # eighth_rest_weight.pack()
    # sixteenth_rest_weight.pack()

    frame.on_form_submit(write_to_console)

    # weights = {}
    # weights['whole_note_weight'] = whole_note_weight.get()
    # weights['half_note_weight'] = half_note_weight.get()
    # weights['quarter_note_weight'] = quarter_note_weight.get()
    # weights['eighth_note_weight'] = eighth_note_weight.get()
    # weights['sixteenth_note_weight'] = sixteenth_note_weight.get()
    # weights['whole_rest_weight'] = whole_rest_weight.get()
    # weights['half_rest_weight'] = half_rest_weight.get()
    # weights['quarter_rest_weight'] = quarter_rest_weight.get()
    # weights['eighth_rest_weight'] = eighth_rest_weight.get()
    # weights['sixteenth_rest_weight'] = sixteenth_rest_weight.get()

    frame.pack(fill="both", expand=True)
    root.mainloop()

    p = subprocess.Popen('py generate_measures.py')

    # the fourth item holds the input values
    composerTool = 'Captain'

    # Disable undo since it has internal functions
    project.begin_undo_block()

    # For producing balances and such
    project.master_track.add_fx('Ozone 9')
    mVol = project.master_track.get_info_value('P_VOL')
    project.master_track.set_info_value('P_VOL', mVol * 0.5)

    # Song library has a collection of song structures
    # lf = open(r's:/song-patterns.json')
    # data = lf.read()
    # j = json.loads(data)
    # song: SongLibraryElement = song_library_from_dict(j)[2]
    song = generateStructure()

    # Create a reference region map
    # Metadata isn't available in-app for grouping and pools
    refRegion: list[SongPart] = []

    # Regions are cumulative and added in seconds
    accumulator: float = 0.0
    for idx, part in enumerate(song.structure):
        # Region colors are are grouped by part
        p: SongPart = part

        # Each song has a BPM and may start with different sets of seconds
        out_time = project.beats_to_time(4)
        out_time = out_time * int(p.bars)

        # Each region has a type (Verse, Choruse, et al.)
        # Prefix the type for pooling
        region: reapy.Region = project.add_region(
            accumulator,
            accumulator + out_time,
            p.type.value + ": " + p.name,
            randColorByHue(p.color)
        )
        # Map back the region index since region names are unavailable
        p.index = region.index
        refRegion.append(p)
        accumulator = accumulator + out_time

    tracks = makeTracks(project, composerTool)
    # MIDI items here are added with reference data
    # Remaining regions are pulled from the project param
    print(refRegion)
    addMidiItems(project, refRegion)

    # Add a click track
    clickTrack = RPR.NamedCommandLookup(
        '_SWS_AWINSERTCLICKTRK')
    RPR.Main_OnCommandEx(clickTrack, 0, project)

    # Add a track template - command _S&M_ADD_TRTEMPLATEl
    loadTemplate = RPR.NamedCommandLookup(
        '_S&M_ADD_TRTEMPLATEl')
    RPR.Main_OnCommandEx(loadTemplate, 0, project)

    # Stop blocking the undo history
    project.end_undo_block("Null Angel Template")


if __name__ == '__main__':
    main()
