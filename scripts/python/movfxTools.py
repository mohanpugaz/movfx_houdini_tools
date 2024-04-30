import hou,shutil,os,time,re
from time import gmtime, strftime
import webbrowser as wb

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
            msg = f"viewport background set to {next_scheme.name()}"
            hou.ui.setStatusMessage(msg)
    return
    
    
def viewport_grab(filepath,name):
    """takes filepath and name as argument and saves viewport snapshot"""
    
    ###grabbing cur_viewport and other objects
    cur_desktop = hou.ui.curDesktop()
    desktop = cur_desktop.name()
    viewer = hou.paneTabType.SceneViewer
    panetab = cur_desktop.paneTabOfType(viewer).name()
    persp = cur_desktop.paneTabOfType(viewer).curViewport().name()
    camera_path = desktop + '.' + panetab + '.' + 'world.' + persp   
    
    # saving snapshot to desired path
    filename = filepath+"/"+name+".jpg"
    if filename is not None:
        frame = hou.frame()
        hou.hscript("viewwrite -c -f %d %d -r 500 500 %s '%s'" % (frame, frame,camera_path, filename))
    return

def backup_save(new_file):
    dup_file = new_file
    dup_file_path = os.path.dirname(dup_file)
    print(dup_file_path)
    cur_file = hou.hipFile.path()
    if os.path.exists(dup_file_path):
        print("exists")
        shutil.copy(cur_file, dup_file)
    else:
        print("not exists")
        os.makedirs(dup_file_path)
        shutil.copy(cur_file, dup_file)
    return     

def snap_tool():
    """ makes snapshot of current viewport and saves a backupfile in snaps folder"""
    
    ###get current scene details
    hip = os.getenv("HIP")
    hipname = os.getenv("HIPNAME")

    snaps = hip+"/snaps/"
    cur_time = time.ctime()
    cur_file = hou.hipFile.path()

    name = hipname + "_" + cur_time 
    name = name.replace(" ","_")
    name = name.replace(":","_")
    
    dup_file_path = snaps + "_hips/" 
    dup_file = dup_file_path + name + ".hiplc"

    backup_save(dup_file)
    viewport_grab(snaps,name)
    return

    
def filecache_backupsave():
    hou.hipFile.save()

    nodepath = hou.node("../").path()
    node = hou.node(nodepath)

    cache_name = node.parm("cachename").eval()
    cache_name = cache_name.replace(".","_")
    cache_dir = node.parm("cachedir").eval()

    backup_file = cache_dir + "/" + cache_name + ".hiplc"
    backup_save(backup_file)
    viewport_grab(cache_dir,cache_name)
    return   
  

def flipbook_backupsave(path,name):
    hou.hipFile.save()
    cur_file = hou.hipFile.path()
    dup_file = path +"/"+ name + ".hiplc"
    backup_save(dup_file)
  

def explore_movfxtools():
    path = os.environ["MOVFX"]
    wb.open(path)

def explore_hip():
    path = os.environ["HIP"]
    wb.open(path)
    
def explore_lib():
    path = os.environ["MOLIB"]
    wb.open(path)
    
def add_to_gallery():
    gal_path = os.getenv("MOVFX")
    gal_path = gal_path+"/gallery/"
    node = hou.selectedNodes()[0]
    type = node.type().name()
    type_cat = node.type().category().name()
    category = "movfx_"
    name = category + type_cat + "_" + type+"_"+node.name()
    gal_path = gal_path + name + ".gal" 
    print(gal_path)
    entry = hou.galleries.createGalleryEntry(gal_path, name, node)
    entry.setCategories(["movfx"])
    label = node.name().replace("_"," ")
    entry.setLabel(label)
    entry.setName(node.name())
    entry.setKeywords(["movfx"])
    entry.setDescription(hou.ui.readInput("Give a discription")[1])
    if type == "redshift_vopnet":
        entry.setKeywords(["Redshift","RS","movfx"])

def make_new_shot(path):
    name = hou.ui.readInput("name",title="New Shot")[1]
    path = path + "/" + name 
    make_workspace(path)
    return
  
    
def make_workspace(path):
    name = os.path.basename(path)
    hip_path = path + "/work/hip" 
    
    if os.path.exists(hip_path):
        print("hip path exists, creating folders") 
    else:
        os.makedirs(hip_path)

    hip_path = hip_path + "/"
    file = hip_path + name + "_001.hiplc"
    hou.hipFile.save(file)
    folders  = ["flipbook","images","render","temp","geo","comp","backup","ref","misc","snaps"]

    for folder in folders:
        dir  = hip_path + "/" + folder
        os.mkdir(dir)
        
    set_shot()
    return
    
def set_shot():
    hip = os.getenv("HIP")
    os.environ["FLIPBOOK"] = hip + "/flipbook"
    os.environ["RENDER"] = hip + "/render"
    os.environ["VIDEO"] = hip + "/video"
    os.environ["IMAGES"] = hip + "/images"
    os.environ["GEO"] = hip + "/geo"
    os.environ["SNAPS"] = hip + "/snaps"
    os.environ["BACKUP"] = hip + "/backup"
    os.environ["REF"] = hip + "/ref"
    os.environ["SHOTTEMP"] = hip + "/temp"
    
def incrementally_save_file():
    file_path = hou.hipFile.path()
    base_dir = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)

    name, extension = os.path.splitext(base_name)

    version_match = re.search(r"\d+$", name)  # Search for a version number at the end of the name
    if version_match:
        version_str = version_match.group()
        version = int(version_str)
        name = name[:version_match.start()]  # Remove the existing version number
    else:
        version = 0

    version += 1
    version_str = str(version).zfill(3)  # Convert version to a 3-digit string with leading zeros

    if version == 1:
        new_name = f"{name}_{version_str}{extension}"
    else:
        new_name = f"{name}{version_str}{extension}"

    new_file_path = os.path.join(base_dir, new_name)
    new_file_path = new_file_path.replace("\\", "/")
    print(f"File saved as '{new_file_path}'")
    hou.hipFile.save(new_file_path)
    

def get_max_version(folder_path):
    files = os.listdir(folder_path)  # Get a list of files in the folder
    version_numbers = []

    for file_name in files:
        version_match = re.search(r"v(\d+)", file_name)  # Extract the version number using a regular expression
        if version_match:
            version_number = int(version_match.group(1))  # Convert the version number to an integer
            version_numbers.append(version_number)

    if version_numbers:
        max_version = max(version_numbers)
        return max_version
    else:
        return None
        

def create_rndr_nodes_from_selected():
    nodes = hou.selectedNodes()
    for n in nodes:
        name = n.name()
        path = n.path()
        obj_net = hou.node("/obj")
        geo = obj_net.createNode("geo",name)
        geo.setColor(hou.Color((0.1,0.3,0.6)))
        om = geo.createNode("object_merge")
        om.parm("objpath1").set(path)
    return
    
    
def create_objmerge_from_selected():
    nodes = hou.selectedNodes()
    for n in nodes:
        p = n.parent()
        if p.type().name() == "geo":
            name = n.name()
            path = n.path()
            pos  = n.position()
            pos  = [pos[0],pos[1]-1]
            om = p.createNode("object_merge")
            om.parm("objpath1").set(path)
            om.setPosition(pos)
            
    return


######____________Communicate_with_Telegram_BOT____________######

from telegram import Bot
import requests,json

def get_tele_cred():
    with open('C:/Users/mohan/Desktop/tele_tok.json', 'r') as user_file:
        json_data = json.load(user_file)
    TOKEN   = json_data['TOKEN']
    chat_id = json_data['chat_id']
    return [TOKEN,chat_id]


def tele_send(msg,video="filepath"):
    bot_token = get_tele_cred()[0]
    chat_id = get_tele_cred()[1]

    msg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    vid_url = f"https://api.telegram.org/bot{bot_token}/sendVideo"

    # Send text message
    if msg:
        requests.post(msg_url, json={"chat_id": chat_id, "text": msg})

    # Send video file
    if video_file:
        with open(video_file, 'rb') as file:
            files = {'video': file}
            requests.post(vid_url, data={"chat_id": chat_id}, files=files)


#######__________###########


def nodeNearPos(node):
    n = node
    pos  = n.position()
    pos  = [pos[0],pos[1]-1]
    return pos
