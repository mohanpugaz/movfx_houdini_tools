from hutil.Qt import QtWidgets, QtCore, QtUiTools, QtGui
import os
import math
import hou

lib = "D:/work/library/tools/houdini/movfx_tools/gallery"
ui = "D:/work/library/tools/houdini/movfx_tools/python_panels/snippetManager.ui"
main_widget = None
gals = []

def widget():
	global ui
	global main_widget
	global gals

	ui_file = QtCore.QFile(ui)
	ui_file.open(QtCore.QFile.ReadOnly)

	loader = QtUiTools.QUiLoader()
	main_widget = loader.load(ui_file)

	# connect ui parameters to functions
	main_widget.parm_btn_load.clicked.connect(load_sel)
	main_widget.parm_inp_search.textChanged.connect(update_table)
	gals = collect_gals()
	fill_table(gals)
	return main_widget


def fill_table(gals):

	table = main_widget.parm_tbl_snippets

	column_count = 1
	row_count = math.ceil(len(gals) / column_count)
	table.setRowCount(row_count)
	table.setColumnCount(column_count)

	# set table items
	x = y = a = b = 0
	for g in gals:
		if x >= column_count:
			a += 1
			x = 0
		b = y % column_count
		item = QtWidgets.QTableWidgetItem()
		item.setText(g)
		table.setItem(a, b, item)
		x+=1
		y+=1

	# set icons
		icon_name = g.split(".")[0] + ".png"
		icon_path = lib + "/.thumbs/" + icon_name
		icon = QtGui.QIcon(icon_path)
		sizex = 100
		size = QtCore.QSize(sizex,sizex)
		item.setIcon(icon)
		table.setIconSize(size)

	# auto resize
	header = table.horizontalHeader()
	header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
	# header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
	# header.setVisible(False)
	header = table.verticalHeader()
	header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
	# header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
	# header.setVisible(False)
	return


def update_table():
	updated_gals = update_gals()
	fill_table(updated_gals)


def load_sel():
	table = main_widget.parm_tbl_snippets
	sel = table.selectedItems()
	names = [i.text() for i in sel]

	for n in names:
		path = lib + "/" + n
		load_gallery_entry(path)

	return


def load_gallery_entry(gal_file):
	gal = gal_file
	gal = hou.galleries.installGallery(gal).galleryEntries()
	entry = gal[0]

	dict = {
		"LOP": "lopnet",
		"TOP": "topnet",
		"ROP": "ropnet",
		"COP2": "cop2net",
		"SOP": "geo",
		"OBJ": "subnet",
		"CHOP": "chopnet",
		"VOP": "matnet",
		"SHOP": "shopnet"
	}

	category = entry.nodeTypeCategory().typeName()
	category_container = dict[category]
	root = hou.node("/obj")

	# print(category)
	container = root.createNode(category_container)
	container.setName("snippet_" + entry.name())
	entry.createChildNode(container)
	return


def collect_gals():
	global lib
	gals = []
	extension = ".gal"
	for filename in os.listdir(lib):
		if filename.endswith(extension):
			gals.append(filename)

	return gals


def update_gals():
	#gals = collect_gals()
	search = main_widget.parm_inp_search.text()
	filtered_gals = [file for file in gals if search.lower() in file.lower()]
	return filtered_gals
