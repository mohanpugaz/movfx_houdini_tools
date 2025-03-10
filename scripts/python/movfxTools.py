import hou,shutil,os,time,re
from time import gmtime, strftime
import webbrowser as wb

def make_new_shot(path):

    movfx = os.getenv("MOVFX")
    shot_template = f"{movfx}/shot_template"
    source_dir = shot_template
    new_shot_path = f"{path}"

    destination_dir = new_shot_path
    shutil.copytree(source_dir, destination_dir)

    return new_shot_path

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


def snap_save(path):
    """ makes snapshot of current viewport and saves a backup in given path"""

    snaps = path
    cur_time = time.ctime()
    cur_file = hou.hipFile.path()
    hip_name = os.getenv("HIPNAME")

    name = hip_name + "_" + cur_time
    name = name.replace(" ", "_")
    name = name.replace(":", "_")

    dup_file_path = snaps + "/_hips/"
    dup_file = dup_file_path + name + ".hiplc"

    backup_save(dup_file)
    viewport_grab(snaps, name)

    return

def snap_save_shot():
    ### get current scene details
    hip = os.getenv("HIP")
    snaps = hip+"/snaps"
    snap_save(snaps)
    return


def snap_save_dev():
    dev = os.getenv("HOUDINIDEV")
    snaps = dev + "/_snaps"
    snap_save(snaps)
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
    thumb_path = gal_path + "/.thumbs"
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
    just_name = name[6:]
    words = just_name.split('_')
    acronym = ''.join(word[0] for word in words).upper()
    make_icon(name, thumb_path, acronym)

def make_new_shot_shelf(path):
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
    file = hip_path + name + "_001.hip"
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


def prototypes_from_name(node):

    # makes a subnet at object level contaning an obj for each `named pieces` in given node. 
    # which can be used to instance later

    root = "/obj/"
    geo = node.geometry()
    named_pieces = geo.primStringAttribValues("name")
    unique_named_pieces = list(set(named_pieces))  # Get unique names
    
    ins_node_name = "INSTANCES"
    ins_node = hou.node(root).createNode("subnet", ins_node_name, force_valid_node_name=True)
    
    for name in unique_named_pieces:
        piece = ins_node.createNode("geo", name, force_valid_node_name=True)
        exp = f"@name=={name}"
        om = piece.createNode("object_merge",name)
        om.parm("objpath1").set(node.path())
        om.parm("group1").set(exp)

    return 


def prototypes_from_selection():

    # wrapper of prototypes_from_name

    node = hou.selectedNodes()[0]
    prototypes_from_name(node)
    return 


def nodeNearPos(node):
    n = node
    pos  = n.position()
    pos  = [pos[0],pos[1]-1]
    return pos

def copy_node(node,name="new_name"):
    
    # copy a node and returns copied new node
    
    root = node.parent()
    pos = node.position()
    pos[0] += 2
    
    new_node = hou.copyNodesTo([node],root)[0]
    if name!="new_name":
       new_node.setName(name,unique_name=True)
    new_node.setPosition(pos)
    return new_node

    
def write_env_variables_to_file(file_path):
    try:
        # Clear the file if it exists
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.truncate(0)
                
        # Write environment variables to the file
        with open(file_path, "a") as file:
            for var_name, var_value in os.environ.items():
                if var_value:
                    file.write(f"{var_name}={var_value}\n\n")
        
        # Open the file with the default text editor
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() in ["Linux", "Darwin"]:
            subprocess.Popen(["xdg-open", file_path])
        else:
            print("Unsupported platform")
    except Exception as e:
        print(f"Error occurred: {e}")

######____________Communicate_with_Telegram_BOT____________######

import requests,json

def get_tele_cred():
    token = os.getenv("TELEGRAM_TOKEN_HOUNOTIFY")
    chat_id = os.getenv("TELEGRAM_CHATID_HOUNOTIFY")
    return [token,chat_id]


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

def make_icon(name,path,acronym):
    # needs icon_maker hda to run this

    root = hou.node("/obj")

    path = path + "/" + name + ".png"

    icon_maker = root.createNode("icon_maker")
    icon_maker.parm("name").set(acronym)
    icon_maker.parm("out").set(path)
    icon_maker.parm("execute").pressButton()
    icon_maker.destroy()
    return
    
def open_acg():
    wb.open("https://ambientcg.com/list?type=material%2Catlas%2Cdecal&sort=popular")
