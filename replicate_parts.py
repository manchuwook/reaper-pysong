import reapy
from reapy.reascript_api import RPR

project = reapy.Project()


# This is effectively groupby to reduce processing on already processed groups
def poolGroupItems(prj=project):
    # Unselect all items
    RPR.Main_OnCommandEx(40769, 0, project)

    # Ghost will have the command integer to pool selected items
    # You need the me2beats pool script in SWS to pool selected items
    ghost = RPR.NamedCommandLookup(
        '_RSe6bf9a6d610e6dc713e8553c72c576822ba592ef')
    # Just to validate if it exists
    # reGhost = RPR.ReverseNamedCommandLookup(ghost)

    # Unselect all items
    RPR.Main_OnCommandEx(40769, 0, project)

    ignoreItems = []
    for idxMidiItem2, ghostItem in enumerate(project.items):
        grp = ghostItem.get_info_value('I_GROUPID')
        if(grp not in ignoreItems):
            # Get a single midi item
            ghostItem.set_info_value('B_UISEL', 1)

            # Select grouped midi items (Ctrl+G)
            RPR.Main_OnCommand(40034, 0)

            # Only create pools if there is more than one selected midi item
            if(project.n_selected_items > 1):
                # Script: me2beats_Pool active takes of selected items.lua
                #  _RSe6bf9a6d610e6dc713e8553c72c576822ba592ef
                RPR.Main_OnCommandEx(ghost, 0, project)

            # This group has now been processed
            # Ignore the rest of the items in the group
            ignoreItems.append(grp)

        # Unselect all items
        RPR.Main_OnCommandEx(40769, 0, project)
    return True


if __name__ == '__main__':
    poolGroupItems()
