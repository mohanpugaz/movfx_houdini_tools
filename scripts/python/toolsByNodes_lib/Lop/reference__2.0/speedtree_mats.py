# sample.py
# copy this file and edit the tool name and function for each buttons, dont change the name of the function 
# it must be tool_function() to work


import voptoolutils
import hou
import os
import re
import xml.etree.ElementTree as ET


TOOL_NAME = "Create Speedtree Mats"

def tool_function():
    sel = hou.selectedNodes()[0]
    usdfile = sel.parm("filepath1").eval()
    global STMAT
    STMAT = usdfile.replace(".usd",".stmat")
    if not os.path.exists(STMAT):
        raise FileNotFoundError("STMAT not found: " + STMAT)
    global STMAT_DIR
    global STMAT_FILE
    STMAT_DIR = os.path.dirname(STMAT)
    STMAT_FILE = os.path.basename(STMAT)
    build_materials()






# Houdini Python — SpeedTree .stmat -> MaterialX (improved path resolution)
# Uses your fixed path: C:/Users/mohan/Desktop/plam_tree/v2/Palm.stmat
# Behavior:
#  - Tries Source, File, and then searches the .stmat directory recursively to find real textures.
#  - Picks best local match when absolute Source/File don't exist.
#  - Only creates mtlximage nodes for textures that actually exist.
#  - Maps Color->base_color, Normal->normal, Gloss->specular_roughness (inverted), Specular, Metallic, Opacity, Subsurface*
#  - Ignores AO.
# Run inside Houdini (Solaris /stage) Python shell or shelf tool.



def _norm(p):
    return os.path.normpath(p) if p else p

def _basename(p):
    return os.path.basename(p) if p else ""

def _stem(p):
    return os.path.splitext(_basename(p))[0].lower() if p else ""

def _is_abs_exists(p):
    if not p:
        return False
    pnorm = _norm(p)
    return os.path.isabs(pnorm) and os.path.exists(pnorm)

def _try_join_and_exists(p):
    if not p:
        return None
    joined = os.path.join(STMAT_DIR, p)
    joined_norm = _norm(joined)
    return joined_norm if os.path.exists(joined_norm) else None

def _recursive_find_candidates(target_names):
    """
    Search STMAT_DIR recursively and return list of file paths whose basenames or stems
    match any of the strings in target_names (case-insensitive).
    """
    matches = []
    target_lower = [t.lower() for t in target_names if t]
    for root, _, files in os.walk(STMAT_DIR):
        for f in files:
            fl = f.lower()
            fstem = os.path.splitext(f)[0].lower()
            for tgt in target_lower:
                if fl == tgt or fstem == tgt or tgt in fl or tgt in fstem:
                    matches.append(os.path.normpath(os.path.join(root, f)))
                    break
    return matches

def _find_texture_path(file_attr, source_attr):
    """
    Robust resolution:
      1) Source absolute path (if exists)
      2) File absolute path (if exists)
      3) file joined to stmat dir (exact)
      4) source basename joined to stmat dir
      5) recursive search in stmat dir using source stem / file stem (best match)
      6) fallback None
    """
    file_attr = file_attr.strip() if file_attr else ""
    source_attr = source_attr.strip() if source_attr else ""

    # 1,2: absolute paths
    if _is_abs_exists(source_attr):
        return _norm(source_attr)
    if _is_abs_exists(file_attr):
        return _norm(file_attr)

    # 3: file in same directory as stmat
    if file_attr:
        local = _try_join_and_exists(file_attr)
        if local:
            return local

    # 4: try source basename in stmat dir
    sb = _basename(source_attr)
    if sb:
        local = _try_join_and_exists(sb)
        if local:
            return local

    # 5: recursive fuzzy search using stems (higher priority: source stem, then file stem)
    candidates = []
    sstem = _stem(source_attr)
    fstem = _stem(file_attr)
    # try exact basenames first
    if sb:
        candidates = _recursive_find_candidates([sb, _basename(file_attr)])
    if not candidates:
        # try stems (source stem then file stem)
        candidates = _recursive_find_candidates([sstem, fstem])

    # choose best candidate:
    if candidates:
        # prefer exact filename equals file_attr or source basename
        file_lower = (file_attr or "").lower()
        source_base_lower = sb.lower()
        for c in candidates:
            bn = _basename(c).lower()
            if bn == file_lower or bn == source_base_lower:
                return _norm(c)
        # otherwise return shortest path (heuristic: likely closest)
        candidates.sort(key=lambda p: (len(p), p))
        return _norm(candidates[0])

    # nothing found
    return None

def safe_name(name):
    if not name:
        return "speedtree_mat"
    s = re.sub(r"[^\w\d_]", "_", name)
    if re.match(r"^\d", s):
        s = "_" + s
    return s

def get_or_create_matlib(stage_node, lib_name="speedtree_materials"):
    existing = stage_node.node(lib_name)
    return existing if existing else stage_node.createNode("materiallibrary", lib_name)

def build_materials():
    tree = ET.parse(STMAT)
    root = tree.getroot()

    stage = hou.node("/stage")
    if stage is None:
        raise RuntimeError("Couldn't find /stage. Run this in Solaris (LOPs) context.")

    matlib = get_or_create_matlib(stage,  STMAT_FILE.replace(".stmat",""))
    matlib.setInput(0,hou.selectedNodes()[0])
    matlib.parm("matpathprefix").set(r"/$OS/Materials/")

    for mat in root.findall("Material"):
        # attribute Name (capitalized in your file)
        mat_name = mat.get("Name") or mat.get("name") or "speedtree_mat"
        sname = safe_name(mat_name)

        # ensure unique name in matlib
        uname = sname
        idx = 1
        while matlib.node(uname):
            uname = f"{sname}_{idx}"; idx += 1

        #subnet = matlib.createNode("subnet", uname)
        
        subnet = voptoolutils._setupMtlXBuilderSubnet(destination_node=matlib)
        subnet.setName(uname, unique_name=True)
        surf = subnet.node("mtlxstandard_surface")


        

        for map_el in mat.findall("Map"):
            map_name = (map_el.get("Name") or "").strip()
            if not map_name:
                continue
            channel = map_name.lower()
            # ignore AO explicitly
            if channel in ("ao", "ambientocclusion"):
                continue

            file_attr = map_el.get("File") or ""
            source_attr = map_el.get("Source") or ""

            found_path = _find_texture_path(file_attr, source_attr)
            if not found_path:
                print("[SpeedTree] SKIP - no texture found for", map_name, "in material:", mat_name)
                continue

            # create image node
            img_base = re.sub(r"[^\w\d_]", "_", channel) + "_tex"
            img_name = img_base
            j = 1
            while subnet.node(img_name):
                img_name = f"{img_base}_{j}"; j += 1

            img = subnet.createNode("mtlximage", img_name)
            # Houdini friendly path (use forward slashes)
            img_path_for_parm = _norm(found_path).replace("\\", "/")
            # set file parm (try common parm names)
            set_ok = False
            for p in ("file", "filename", "file1"):
                parm = img.parm(p)
                if parm:
                    parm.set(img_path_for_parm)
                    set_ok = True
                    break
            if not set_ok:
                # fallback: try all parms and set first string parm we can
                for parm in img.parms():
                    try:
                        parm.set(img_path_for_parm)
                        set_ok = True
                        break
                    except Exception:
                        continue

            # wire according to channel
            if channel in ("color", "diffuse", "albedo"):
                surf.setNamedInput("base_color", img, "out")
            elif channel == "normal":
                nm_base = "normalmap"
                nm_name = nm_base
                k = 1
                while subnet.node(nm_name):
                    nm_name = f"{nm_base}_{k}"; k += 1
                nm = subnet.createNode("mtlxnormalmap", nm_name)
                nm.setNamedInput("in", img, "out")
                surf.setNamedInput("normal", nm, "out")
            elif channel == "opacity":
                surf.setNamedInput("opacity", img, "out")
            elif channel in ("gloss",):
                inv_base = "invert_gloss"
                inv_name = inv_base
                k = 1
                while subnet.node(inv_name):
                    inv_name = f"{inv_base}_{k}"; k += 1
                inv = subnet.createNode("mtlxinvert", inv_name)
                inv.setNamedInput("in", img, "out")
                surf.setNamedInput("specular_roughness", inv, "out")
            elif channel in ("specular_roughness", "roughness"):
                surf.setNamedInput("specular_roughness", img, "out")
            elif channel == "specular":
                surf.setNamedInput("specular", img, "out")
            elif channel == "metallic":
                surf.setNamedInput("metalness", img, "out")
            elif channel == "subsurfacecolor":
                surf.setNamedInput("subsurface_color", img, "out")
            elif channel == "subsurfaceamount":
                surf.setNamedInput("subsurface", img, "out")
            elif channel in ("height", "displacement"):
                disp_base = "displacement"
                disp_name = disp_base
                k = 1
                while subnet.node(disp_name):
                    disp_name = f"{disp_base}_{k}"; k += 1
                disp = subnet.createNode("mtlxdisplacement", disp_name)
                disp.setNamedInput("displacement", img, "out")
            else:
                print("[SpeedTree] UNMAPPED map:", map_name, "for material:", mat_name)

        subnet.layoutChildren()

    matlib.layoutChildren()
    print("[SpeedTree] Done. Materials created under:", matlib.path())

# Run


