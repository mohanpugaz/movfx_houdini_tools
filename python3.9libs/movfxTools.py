import hou,shutil,os
from time import gmtime, strftime

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


                
def viewport_grab(filepath,name):

    cur_desktop = hou.ui.curDesktop()
    desktop = cur_desktop.name()
    viewer = hou.paneTabType.SceneViewer
    panetab = cur_desktop.paneTabOfType(viewer).name()
    persp = cur_desktop.paneTabOfType(viewer).curViewport().name()
    camera_path = desktop + '.' + panetab + '.' + 'world.' + persp
    hn = hou.getenv('HIPNAME')
    
    filename = filepath+"/"+name+".png"
    
    if filename is not None:
        frame = hou.frame()
        hou.hscript("viewwrite -c -f %d %d -r 500 500 %s '%s'" % (frame, frame,
                    camera_path, filename))



def filecache_backupsave():
    hou.hipFile.save()
    cur_file = hou.hipFile.path()
    nodepath = hou.node("../").path()
    node = hou.node(nodepath)
    parm = node.parm("cachename")
    cache_name = parm.eval()
    cache_name = cache_name.replace(".","_")
   
    dup_file_path = os.getenv("HIP")+"/geo/_backup/"
    dup_file = dup_file_path + cache_name + ".hiplc"
        
    if os.path.exists(dup_file_path):
        shutil.copy(cur_file, dup_file)
    else:
        os.mkdir(dup_file_path)
        shutil.copy(cur_file, dup_file)

    viewport_grab(dup_file_path,cache_name)
    
    return         
