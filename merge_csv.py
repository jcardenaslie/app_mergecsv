# import the library
from os import listdir
from os.path import isfile, join
import pandas as pd
from appJar import gui

# create a GUI variable called app
app = gui("Merge CSVs")

def merge_csvs(btname):
	frames = []
	files = app.getListBox("files_merge")
	path = path = app.getEntry("userEnt")
	app.clearListBox("files_folder")
	app.clearListBox("files_merge")
	
	for file in files:
		print("reading {}".format(path+file))
		
		try:
			df = pd.read_csv(path+file)
		except:
			print("Archivo no es un csv")

		frames.append(df)	

	result = pd.concat(frames)
	result.to_csv(path + "result.csv")
	app.errorBox("Merge Complete", "Buscar result.csv en la carpeta")

def read_folder(btname):
	path = app.getEntry("userEnt")
	app.clearListBox("files_folder")
	app.clearListBox("files_merge")
	try:
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		print(onlyfiles)
		for file in onlyfiles:
			app.addListItem("files_folder", file)

			# if '.csv' in file:
			# 	app.setListItemBg("files_folder",file,"Green")
			# else :
			# 	app.setListItemBg("files_folder",file,"Red")
	except:
		app.errorBox("Some Error", "Ruta de carpeta no valida.")

def move(direction):
    if direction == ">":
        for item in app.getListBox("files_folder"):
            app.addListItem("files_merge",item) 
            app.removeListItem("files_folder", item)
    elif direction == "<":
        for item in app.getListBox("files_merge"):
            app.addListItem("files_folder",item) 
            app.removeListItem("files_merge", item)
    elif direction == "<<":
        app.addListItems("files_folder", app.getAllListItems("files_merge"))
        app.clearListBox("files_merge")
    elif direction == ">>":
        app.addListItems("files_merge", app.getAllListItems("files_folder"))
        app.clearListBox("files_folder")


app.setSticky("ew")
app.setExpand("all")
# app.setBg("OrangeRed")

app.addLabel("labInstructions", "Fill the path to the folder", 0, 1)
app.addLabel("labInstructionsExample", "Ejemplo: C:/Users/joaquin/Desktop/cemu1.11.2/", 1, 1)

app.addEntry("userEnt", 2, 1)
app.addButtons( ["Load files in folder"], read_folder, 3,1)

app.addLabel("labFilesFolder", "Files in folder", 3, 0)
app.addLabel("labFilesMerge", "Files to merge", 3, 2)

app.addListBox("files_folder", [], 4, 0, 1, 4)
app.addListBox("files_merge", [], 4, 2, 1, 4)

app.addButton("<", move, 4, 1,colspan=1)
app.addButton("<<", move, 5, 1,colspan=1)
app.addButton(">>", move, 6, 1,colspan=1)
app.addButton(">", move, 7, 1,colspan=1)


app.setListBoxBg("files_folder", "Orange")
app.setListBoxBg("files_merge", "Orange")

app.addButtons( ["Merge CSVs"], merge_csvs, 8,1)
# start the GUI
app.go()


