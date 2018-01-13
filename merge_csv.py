# import the library
from os import listdir
from os.path import isfile, join
import pandas as pd
from appJar import gui

# create a GUI variable called app
app = gui("Merge CSVs")

def checkFilesForCSV(list_name, files_names):
	for file in files_names:
		app.addListItem(list_name, file)
		if '.csv' in file:
			app.setListItemBg(list_name,file,"Green")
		else :
			app.setListItemBg(list_name,file,"Red")

def checkFileForCSV(list_name,file):
	if '.csv' in file:
		app.setListItemBg(list_name,file,"Green")
	else :
		app.setListItemBg(list_name,file,"Red")

def merge_csvs(btname):
	frames = []
	files = app.getAllListItems("files_merge")
	print("To Merge", files)
	

	# check for csv files
	not_csv = 0
	for file in files:
		if '.csv' not in file:
			not_csv += 1
			
	print(not_csv)

	if not_csv != 0:
		app.errorBox('CSV Error','Todos los archivos deben ser csv')
		return 0

	path = app.getEntry("userEnt")
	app.clearListBox("files_folder")
	app.clearListBox("files_merge")
	
	#merge with pandas
	for file in files:
		print("reading {}".format(path+file))
		
		try:
			df = pd.read_csv(path+file)
		except:
			app.errorBox('CSV Error','Hubo un error con los archivos')

		frames.append(df)	

	result = pd.concat(frames)
	result.to_csv(path + "result.csv")
	app.infoBox("Merge Complete", "Buscar {}result.csv en la carpeta".format(path), parent=None)

def read_folder(btname):
	path = app.getEntry("userEnt")
	app.clearListBox("files_folder")
	app.clearListBox("files_merge")
	
	try:
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		print(onlyfiles)
	except:
		app.errorBox("Path Error", "Ruta de carpeta no valida.")

	checkFilesForCSV("files_folder",onlyfiles)

def move(direction):
    if direction == ">":
        for item in app.getListBox("files_folder"):
            app.addListItem("files_merge",item)
            app.removeListItem("files_folder", item)
            checkFileForCSV("files_merge",item)
    elif direction == "<":
        for item in app.getListBox("files_merge"):
            app.addListItem("files_folder",item)
            app.removeListItem("files_merge", item)
            checkFileForCSV("files_folder",item) 
    elif direction == "<<":
    	checkFilesForCSV("files_folder",app.getAllListItems("files_merge"))
    	app.clearListBox("files_merge")
    elif direction == ">>":
    	checkFilesForCSV("files_merge",app.getAllListItems("files_folder"))
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


