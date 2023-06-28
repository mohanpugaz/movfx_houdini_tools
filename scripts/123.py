import hou,os

start = 1001
end = 1100
hou.playbar.setFrameRange(start, end)
hou.playbar.setPlaybackRange(start, end)
hou.setFrame(1001)
hou.setUpdateMode(hou.updateMode.Manual)
hou.hscript("autosave on")

def save_to_temp():
    version = 1
    version = str(version).zfill(3) #add padding
    default_save_path = f"D:/work/dev/houdini/_unsaved_hips/movfx_{version}.hiplc"

    while os.path.exists(default_save_path):
        version = int(version)
        version += 1
        version = str(version).zfill(3)
        default_save_path = f"D:/work/dev/houdini/_unsaved_hips/movfx_{version}.hiplc"
    
    hou.hipFile.save(default_save_path)
