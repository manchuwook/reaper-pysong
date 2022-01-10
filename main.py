import logging
import json
from tkinter import *
import reapy
from song_library import SongLibraryElement, SongPart, song_library_from_dict
from song_structurer import generateStructure
from parts_item import addMidiItems
from tracks import makeTracks
from colors import randColorByHue
from reapy import reascript_api as RPR
from __init__ import __version__

__author__ = "manchuwook"
__copyright__ = "manchuwook"
__license__ = "mit"

_logger = logging.getLogger(__name__)

project: reapy.Project = reapy.Project()


def rprint(msg):
    with reapy.reaprint():
        print(msg)


@reapy.prevent_ui_refresh()
def main():
    # reapy.config.enable_dist_api()
    reapy.print('Creating template')

    names = 'Composer (Orb, Captain)'
    dvalues = ''
    maxreturnlen = 100
    nitems = len(dvalues.split(','))
    res = RPR.GetUserInputs('dialogname', nitems, names, dvalues, maxreturnlen)
    if res[0]:
        # the fourth item holds the input values
        composerTool = res[4].split(',')[0]

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
