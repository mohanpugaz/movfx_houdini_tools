import hou,shutil,os,time,re
from time import gmtime, strftime
import webbrowser as wb

def explore_movfxtools():
    path = os.environ["MOVFX"]
    wb.open(path)

def explore_hip():
    path = os.environ["HIP"]
    wb.open(path)
    
def explore_lib():
    path = os.environ["MOLIB"]
    wb.open(path)

def make_new_shot(path):
    name = hou.ui.readInput("name",title="New Shot")[1]
    root = path + "/hip/"
    path = root + name + "/" 
    file = path + name + "_001.hiplc"

    hou.hipFile.save(file)

    folders  = ["flipbook","images","render","temp","geo","comp","backup","ref","misc","snaps"]


    for folder in folders:
        dir  = path + "/" + folder
        os.mkdir(dir)
        
    set_shot()
    return