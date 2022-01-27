# reaper-pysong
Scripts written in python for reaper to generate a template with composer FX

## Main.py
* Adds Ozone 9 to the master track
* Sets the master track volume because it is too loud 
* Opens a song structure file (from an absolute path) and chooses item 3
* Creates a reference because of a bug where I can't get the region name back
* Adds regions at the top level for song part types
* Adds tracks for theory parts (Melody, Harmony, Bass, Chords, et al)
* Adds blank MIDI items for Groups and Pools

## colors.py
* Changes colors format from randomcolor to Reaper format

## song_library.py
* Equivalent to strongly-typing the song parts JSON

## parts_items.py
* Add midi items
* Tries to name the takes (currently not working)
* Groups by song part type (Verse, Chorus, Intro, etc.)

## replicate_parts.py
* (NOTE: uses me2beats_Pool active takes of selected items.lua)
* Loops through midi items and re-pools groups
* First available midi item take gets the source

## tracks.py
* Details the plugins to use
* Sets the track names, FX, icons, colors (mostly reds)
* Also sets FX to put on all tracks (Comp and EQ)
* Groups FX1-3 under an FX Group folder