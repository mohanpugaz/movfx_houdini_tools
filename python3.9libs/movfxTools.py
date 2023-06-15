import hou,shutil,os

def cycle_display_bg():
    # init available schemes
    light = hou.viewportColorScheme.Light
    dark  = hou.viewportColorScheme.Dark
    grey  = hou.viewportColorScheme.Grey
    
    # add them to a list
    schemes = [light,dark,grey]
    
    
    # find the viewport display settings
    viewport = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
    display_settings = viewport.curViewport().settings()
    
    # apply the sceme
    
    current_scheme = display_settings.colorScheme()
    
    for s in schemes:
        if s == current_scheme:
            next_id =  schemes.index(s)+1
            next_id = next_id % len(schemes)
            next_scheme = schemes[next_id]
            display_settings.setColorScheme(next_scheme)
            print(f"set to {next_scheme}")

        

def filecache_backupsave():
    cur_file = hou.hipFile.path()
    nodepath = hou.node("../").path()
    node = hou.node('/obj/geo1/filecache1')
    parm = node.parm("cachename")
    cache_name = parm.eval()
    cache_name = cache_name.replace(".","_")
   
    
    dup_file_path = os.getenv("HIP")+"/geo/_backup/"
    dup_file = dup_file_path + cache_name + ".hiplc"
    print(dup_file)
    
    if os.path.exists(dup_file_path):
        shutil.copy(cur_file, dup_file)
    else:
        os.mkdir(dup_file_path)
        shutil.copy(cur_file, dup_file)
    return         

