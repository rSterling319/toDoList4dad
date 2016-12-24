#To do list GUI
#tutorial from christianthompson.com/node/46

#IDEAS:
"""
Add a save feature.
Automatically populate listbox from save filewhen opening the program
ask if want to save before exiting
-have to greate quit function
-message box to get do you want to save
-then exit program

Show completed/to do items.
-make completed text red?  -- lb_tasks.itemconfig(0, {"fg": "red"}) this changes the 0th item to text to red
-3 states: to do, completed, in progress

Sort by:
-Duration (time it would take to complete)
-Cost ($$)
-Date added
-priority (high, med, low)--when they need to be completed

Stats to keep track of:
-date completed
-cost
-

ADD:
have a materials add, be able to select a multiple to-do items and to a materials list and print/write to text file
	-get active from main window but adds to a listbox on a separate window
	-separate by task name
	-flag a duplicate material just have(duplicate) print out next to it
print a task details page
print a filtered list
possibly a print all tasks sorted by a certain paramerter
Search feature
	-do a percent match.. that way if somethin is mispelled/capitalized it might still show up
have to add a update/edit task feature where you can enter the time in and other features
	- i think i can achieve this by just populating the add task with the current selected item

"""
"""	HOW TO: Iterate through data
print(tasks)
print('\n')
for item in tasks:
	print('\n')
	for value in item.keys():
		print (item[value])
"""
"""FIXME's  
	-previously updated labels -- label no longer exists x2
	-finish search bar!
	--continue working on the search function
		
"""


import tkinter
from tkinter import messagebox
import random
#This is for the save and write functions
import csv
#For sorting dictionaries
from operator import itemgetter
#for date and time function
import datetime
import math
from difflib import SequenceMatcher

#Create The GUI Elements
#create root window
root = tkinter.Tk()

#change root window background color
root.configure(bg="white")

#sets the title bar name
root.title("To-Do-List")

#set the window size
root.geometry("325x350+250+50")

#create empty list
tasks = []
#open save file
saveFile = open("toDoSave.csv",'r')

#functions
def convertToTime(aString):
	if aString == '0':
		return datetime.datetime(1,1,1,1,1,1)
	else:
		year= int(aString[0:4])
		month= int(aString[5:7])
		day= int(aString[8:10])
		hour= int(aString[11:13])
		minute= int(aString[14:16])
		second= int(aString[17:19])
		return datetime.datetime(year, month, day, hour, minute, second)
	
def csv_dict_reader(file_obj):
	"""
	Read a CSV file using a csv.DictReader
	"""
	
	reader = csv.DictReader(file_obj, delimiter=',')
	for line in reader:
		tasks.append(line)
	
	#Iterate throught time and convert to type datetime.datetime
	
	for item in tasks:
		item['tTimeStart'] = convertToTime(item['tTimeStart'])
		item['tTimeFinish'] = convertToTime(item['tTimeFinish'])
		item['tMaterials'] = convertToList(item['tMaterials'])
	
	
def update_listbox():
	#clear listbox
	clear_listbox()
	#populate the list box
	for item in tasks:
		lb_tasks.insert("end", item["tName"])
		#color code when populating listbox
		if item["tStatus"] == "Completed!":
			index = tasks.index(item)
			lb_tasks.itemconfig(index, {"fg" :"red"})
		elif item["tStatus"] == "Started":
			index = tasks.index(item)
			lb_tasks.itemconfig(index, {"fg" :"green"})
		elif item["tStatus"] == "Waiting":
			index = tasks.index(item)
			lb_tasks.itemconfig(index, {"fg" :"orange"})
	

def clear_listbox():
	lb_tasks.delete(0, "end")

def convertToList(item):
	toList = item
	toList = toList.strip('[')
	toList = toList.strip(']')
	toList = toList.replace("\'", "")
	#toList = toList.replace(" ", '')
	toList = toList.split(',')
	for i in range(0, len(toList)):
		toList[i] = toList[i].strip()
		
	return toList

def add_task():
	
	def addTaskIn():
		#get the task to add #tName|tDescription|tLocation|tTimeEst|tTimeStart|tTimeFinish|tCostEst|tCostAct|tPriority|tStatus
		newTask = {"tName":txt_addTask.get().capitalize(),"tDescription":txt_addDesc.get(),"tLocation": txt_addLocation.get(), "tTimeEst":addTimeEst.get(), "tTimeStart": datetime.datetime.today(), "tTimeFinish": datetime.datetime(1,1,1,1,1,1),"tCostEst":addCostEst.get(),"tCostAct":0,"tPriority":addPriority.get(),"tStatus":addStatus.get(), "tMaterials": txt_addMaterials.get()}
		
		duplicate = False
		
		#make sure !empty
		if txt_addTask.get() != "":
			
			#tasks.append(newTask)
			#update_listbox()
			
			for item in tasks:
				if newTask['tName'] == item['tName']:
					confirm = messagebox.askyesno("Duplicate Found", " %s already in To-Do-List!\n Do you want to add anyway?" %newTask["tName"].capitalize())
					if confirm:
						newTask['tMaterials']=convertToList(newTask['tMaterials'])
						tasks.append(newTask)
						update_listbox()
						duplicate = True
						break
					else:
						break
				else:
					continue
			if not duplicate:
				newTask['tMaterials']=convertToList(newTask['tMaterials'])
				tasks.append(newTask)
				update_listbox()
				
				
		else:
			#create an error message warning nothing was entered
			messagebox.showwarning("Warning", "You Need to enter a task!")
		#Reset Values in popup
		txt_addTask.delete(0, "end")
		txt_addDesc.delete(0, "end")
		addTimeEst.set("None")
		txt_addLocation.delete(0, "end")
		addCostEst.set("None")
		addPriority.set("None")
		addStatus.set("Planned")
		txt_addMaterials.delete(0, "end")
		

				
		
	
	
	#create pop up window to enter data
	add_task_PopUp = tkinter.Toplevel()
	add_task_PopUp.title("Add a Task")
	add_task_PopUp.title("Add a Task")
	add_task_PopUp.geometry("300x400+575+0")
	
	#Label and text box for add task
	lbl_addTask = tkinter.Label(add_task_PopUp, text ="Task: ", bg = "white")
	lbl_addTask.grid(row=0, column =0)
	txt_addTask = tkinter.Entry(add_task_PopUp, width = 20)
	txt_addTask.grid(row=0, column = 1)
	
	#label and text box for add description
	lbl_addDesc = tkinter.Label(add_task_PopUp, text= "Description: ", bg ="white")
	lbl_addDesc.grid(row = 1, column = 0)
	txt_addDesc = tkinter.Entry(add_task_PopUp, width = 20)
	txt_addDesc.grid(row =1, column = 1)
	
	#label and DropDown box for add time estimate
	lbl_addTimeEst = tkinter.Label(add_task_PopUp, text= "Time Estimate: ", bg ="white")
	lbl_addTimeEst.grid(row =2 , column =0 )
	addTimeEst = tkinter.StringVar(add_task_PopUp)
	addTimeEst.set("None") #initial value
	drp_addTimeEst = tkinter.OptionMenu(add_task_PopUp, addTimeEst, "None", "Short", "Med", "Long")
	drp_addTimeEst.grid(row =2, column = 1)
	
	
	#label and text box for add location
	lbl_addLocation = tkinter.Label(add_task_PopUp, text= "Location: ", bg ="white")
	lbl_addLocation.grid(row = 3, column = 0)
	txt_addLocation = tkinter.Entry(add_task_PopUp, width = 20)
	txt_addLocation.grid(row =3, column = 1)
	
	#label and DropDown box for add cost estimate
	lbl_addCostEst = tkinter.Label(add_task_PopUp, text= "Cost Estimate: ", bg ="white")
	lbl_addCostEst.grid(row = 4, column = 0)
	addCostEst = tkinter.StringVar(add_task_PopUp)
	addCostEst.set("None") #initialvalue
	drp_addCostEst = tkinter.OptionMenu(add_task_PopUp, addCostEst,"None ($0)", "Low  (<$150)", "Med  ($150-$500)", "High  ($500-$1500)", "Very High  (>$1500)")
	drp_addCostEst.grid(row =4, column = 1)
	
	#Label and dropDown box for priority
	lbl_addPriority = tkinter.Label(add_task_PopUp, text= "Priority: ", bg ="white")
	lbl_addPriority.grid(row =5 , column =0 )
	addPriority = tkinter.StringVar(add_task_PopUp)
	addPriority.set("None") #initial value
	drp_addPriority = tkinter.OptionMenu(add_task_PopUp, addPriority, "None", "Low", "Med", "High")
	drp_addPriority.grid(row =5, column = 1)
	
	#Label and dropDown for Status
	lbl_addStatus = tkinter.Label(add_task_PopUp, text = "Status: ", bg ="white")
	lbl_addStatus.grid(row=6, column =0)
	addStatus = tkinter.StringVar(add_task_PopUp)
	addStatus.set("Planned")#initial value
	drp_addStatus = tkinter.OptionMenu(add_task_PopUp, addStatus, "Planned", "Started", "Waiting", "50%", "90%", "Completed!")
	drp_addStatus.grid(row=6, column=1)
	
	#Label and entry fro materials
	lbl_addMaterials = tkinter.Label(add_task_PopUp, text = "Materials: ", bg = "white")
	lbl_addMaterials.grid(row=7, column = 0)
	txt_addMaterials = tkinter.Entry(add_task_PopUp, width = 20)
	txt_addMaterials.grid(row = 7, column = 1)
	
	#Add the task
	btn_AddTask = tkinter.Button(add_task_PopUp, text = "Add this Task", fg = "green", bg = "white", command =addTaskIn)
	btn_AddTask.grid(row=10, column = 0)
	#Exit popup
	btn_Done = tkinter.Button(add_task_PopUp, text = "Done", fg = "green", bg = "white", command =add_task_PopUp.destroy)
	btn_Done.grid(row=10, column = 1)
	
	

	

def markComplete():
	task=lb_tasks.get("active")
	for item in tasks:
		if item["tName"] == task:
			index = tasks.index(item)
	
	item = tasks[index]
	item['tStatus'] = markStatus.get()
	if item['tStatus'] =="Completed!":
		item['tTimeFinish'] = datetime.datetime.today()
	if item['tStatus'] == "Started":
		item['tTimeStart'] = datetime.datetime.today()
	update_listbox()
	markStatus.set("Change Status..")#initial value
		
def delAll():
	#create message box!
	confirmed = messagebox.askyesno("Please Confirm", "Do you Really want to delete all items?")
	
	if confirmed:
		global tasks
		#clear the tasks list
		tasks = []
		#update the list box
		update_listbox()
	
def delOne():
	#get the text of the currently selected item
	task = lb_tasks.get("active")
	#confirm in the list
	for item in tasks:
		if item["tName"] == task:
			tasks.remove(item)
	#update the list box
	update_listbox()
	
def sortAsc():
	global tasks
	tasks = sorted(tasks, key=itemgetter('tName'))
	#update the list box
	update_listbox()
	
def sortDsc():
	global tasks
	#reverse lists
	tasks = sorted(tasks, key=itemgetter('tName'), reverse = True)
	#update the list box
	update_listbox()

def chooRand():
	#choose a random task
	task = random.choice(tasks)
	#update display label
	lbl_display["text"]=task["tName"]
	
def numOfTasks():
	#get number of tasks
	number_of_tasks = len(tasks)
	#create and format message to dispay
	msg = "Number of Tasks: %s" %number_of_tasks
	#display message
	lbl_display["text"] = msg

def saveTasks():
	#create list that contains the fild names
	fieldnames = ["tName","tTimeStart","tLocation","tStatus","tPriority","tDescription","tTimeEst","tTimeFinish","tCostEst","tCostAct","tMaterials"]
	#write to file
	with open("toDoSave.csv", "w", newline='') as out_file:
		writer = csv.DictWriter(out_file,delimiter=',',fieldnames=fieldnames)
		writer.writeheader()
		for row in tasks:
			writer.writerow(row)
	
	messagebox.showinfo("Saved", "Your To-Do-List has been saved!")

def printMaterials(aList):
	aString = ''
	for item in aList:
		aString += item + '\n'
	
	return aString

def convertTimeDelta(deltaTime):
	years = int(deltaTime.days/365)
	days = deltaTime.days%365
	hours = int(deltaTime.seconds/(60**2))
	minutes=(int(deltaTime.seconds/60))%60
	seconds= deltaTime.seconds%60
	
	return "%s years %s days %s:%s h:m" %(years, days, hours, minutes)
	
def viewTask():
	#function to view the selected task details
	task = lb_tasks.get("active")		
	#create pop up window to display details of selected task
	viewTask_PopUp = tkinter.Toplevel()
	viewTask_PopUp.title(task) #displays task name as the window name
	viewTask_PopUp.geometry("300x400+575+0")
	
	
	#confirm in the list
	for item in tasks:
		if item["tName"] == task:
			selTask = item
	#tName|tDescription|tLocation|tTimeEst|tTimeStart|tTimeFinish|tCostEst|tCostAct|tPriority|tStatus
	lbl_Name = tkinter.Label(viewTask_PopUp, text = "Task name: ", bg ="white",anchor = "w", justify = "left")
	lbl_Name.grid(row=0, column =0)
	lbl_taskName = tkinter.Label(viewTask_PopUp, text = selTask['tName'], bg ="white",justify = 'left',anchor = "w",)
	lbl_taskName.grid(row=0, column =1)
	
	lbl_Priority = tkinter.Label(viewTask_PopUp, text = "Priority", bg ="white",justify = "left",anchor = "w")
	lbl_Priority.grid(row=1, column =0)
	lbl_taskPriority = tkinter.Label(viewTask_PopUp, text = selTask['tPriority'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskPriority.grid(row=1, column =1)
	
	lbl_Description = tkinter.Label(viewTask_PopUp, text = "Description:", bg ="white",justify = "left",anchor = "w")
	lbl_Description.grid(row=2, column =0)
	lbl_taskDescription = tkinter.Label(viewTask_PopUp, text = selTask['tDescription'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskDescription.grid(row=2, column =1)
	
	lbl_Location = tkinter.Label(viewTask_PopUp, text = "Location: ", bg ="white",justify = "left",anchor = "w")
	lbl_Location.grid(row=3, column =0)
	lbl_taskLocation = tkinter.Label(viewTask_PopUp, text = selTask['tLocation'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskLocation.grid(row=3, column =1)
	
	lbl_TimeEst = tkinter.Label(viewTask_PopUp, text = "Time Estimate: ", bg ="white",justify = "left",anchor = "w")
	lbl_TimeEst.grid(row=4, column =0)
	lbl_taskTimeEst = tkinter.Label(viewTask_PopUp, text = selTask['tTimeEst'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskTimeEst.grid(row=4, column =1)
	
	lbl_timeStart = tkinter.Label(viewTask_PopUp, text ="Time Start:" , bg ="white",justify = "left",anchor = "w")
	lbl_timeStart.grid(row=5, column =0)
	lbl_taskStart = tkinter.Label(viewTask_PopUp, text = selTask['tTimeStart'].strftime("%H:%M on %m/%d/%y"), bg ="white",wraplength = 200, justify = "left")
	lbl_taskStart.grid(row=5, column =1)
	
	lbl_timeStart = tkinter.Label(viewTask_PopUp, text ="Time Finish:" , bg ="white",justify = "left",anchor = "w")
	lbl_timeStart.grid(row=6, column =0)
	lbl_taskStart = tkinter.Label(viewTask_PopUp, text = selTask['tTimeFinish'].strftime("%H:%M on %m/%d/%y"), bg ="white",wraplength = 200, justify = "left")
	lbl_taskStart.grid(row=6, column =1)
	
	lbl_timeActual = tkinter.Label(viewTask_PopUp, text = "Time Actual: ", bg ="white",justify = "left",anchor = "w")
	lbl_timeActual.grid(row=7, column =0)
	lbl_taskTimeActual = tkinter.Label(viewTask_PopUp, text = convertTimeDelta((selTask['tTimeFinish']-selTask['tTimeStart'])), bg ="white",wraplength = 200, justify = "left")
	lbl_taskTimeActual.grid(row=7, column =1)
	
	lbl_CostEst = tkinter.Label(viewTask_PopUp, text = "Cost Estimate: ", bg ="white",justify = "left",anchor = "w")
	lbl_CostEst.grid(row=8, column =0)
	lbl_taskCostEst = tkinter.Label(viewTask_PopUp, text = selTask['tCostEst'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskCostEst.grid(row=8, column =1)
	
	lbl_CostActual = tkinter.Label(viewTask_PopUp, text = "Actual Cost", bg ="white",justify = "left",anchor = "w")
	lbl_CostActual.grid(row=9, column =0)
	lbl_taskCostActual = tkinter.Label(viewTask_PopUp, text = selTask['tCostAct'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskCostActual.grid(row=9, column =1)
	
	lbl_Status = tkinter.Label(viewTask_PopUp, text = "Status", bg ="white",justify = "left",anchor = "w")
	lbl_Status.grid(row=10, column =0)
	lbl_taskStatus = tkinter.Label(viewTask_PopUp, text = selTask['tStatus'], bg ="white",wraplength = 200, justify = "left")
	lbl_taskStatus.grid(row=10, column =1)
	
	lbl_Materials = tkinter.Label(viewTask_PopUp, text = "Materials", bg="white", justify = "left", anchor ="w")
	lbl_Materials.grid(row=11, column = 0)
	lbl_taskMaterials = tkinter.Label(viewTask_PopUp, text = printMaterials(selTask['tMaterials']), bg="white", wraplength = 200, justify = "left", fg ="purple")
	lbl_taskMaterials.grid(row=11, column =1)
	
	btn_Done = tkinter.Button(viewTask_PopUp, text = "Done", fg = "green", bg = "white", command =viewTask_PopUp.destroy)
	btn_Done.grid(row=12, column = 1)
	
	
	
	


def about():
	messagebox.showinfo("About", "\t\tTo-do-list\n\nA program to help organize and keep track\nof tasks.\n\n\t\tCreated by:\n\t   Richard Sterling")
	

	
	

def filterTasks():
	
	def filterItems(item):
		#create two lists, empty and full of boolean values of the check boxes
		name = item['tName'] +(20- len(item['tName']))*" "
		itemHasList =[]
		
		checkBoxList = [chk_Priority.get(), chk_TimeEst.get(), chk_CostEst.get(),chk_Status.get()]
		if chk_Priority.get() and item['tPriority'] == priority.get():
			retPriority = priority.get()
			itemHasList.append(chk_Priority.get())
			retPriority = retPriority+(math.ceil(len(retPriority)/(len(retPriority)+1))*(10-len(retPriority)))*" " 
		else:
			retPriority =""
			itemHasList.append(False)
		if chk_TimeEst.get() and item['tTimeEst'] == timeEst.get():
			retTimeEst = timeEst.get()
			itemHasList.append(chk_TimeEst.get())
			retTimeEst = retTimeEst+(math.ceil(len(retTimeEst)/(len(retTimeEst)+1))*(10-len(retTimeEst)))*" "
		else:
			retTimeEst = ""
			itemHasList.append(False)
		if chk_CostEst.get() and item['tCostEst'] == costEst.get():
			retCostEst = costEst.get()
			itemHasList.append(chk_CostEst.get())
			retCostEst = retCostEst+(math.ceil(len(retCostEst)/(len(retCostEst)+1))*(10-len(retCostEst)))*" "
		else:
			retCostEst = ""
			itemHasList.append(False)
		if chk_Status.get() and item['tStatus'] == status.get():
			retStatus = status.get()
			itemHasList.append(chk_Status.get())
			retStatus = retStatus+(math.ceil(len(retStatus)/(len(retStatus)+1))*(10-len(retStatus)))*" "
		else:
			retStatus = ""
			itemHasList.append(False)
		
		if checkBoxList == itemHasList:
			return (True, name + retPriority +  retTimeEst  + retStatus +retCostEst )
		else:
			return(False, "Not in it")
	
	def updateListFilter():
		lb_filterListbox.delete(0, 'end')
		#a little boolean stuff to add to the titles
		if chk_Priority.get():
			printPriority = "\nPriority = " + priority.get()
			headPriority = "Priority  "
		else:
			printPriority = ""
			headPriority = ""
		if chk_TimeEst.get():
			printTimeEst = "\nTime Estimate = " + timeEst.get()
			headTimeEst = "TimeEst   "
		else:
			printTimeEst =""
			headTimeEst =""
		if chk_CostEst.get():
			printCostEst = "\nCost Estimate = " + costEst.get()
			headCostEst = "CostEst   "
		else:
			printCostEst = ""
			headCostEst =""
		if chk_Status.get():
			printStatus = "\nStatus = " + status.get()
			headStatus = "Status    "
		else:
			printStatus = ""
			headStatus =""
	
		lbl_filterResults["text"] = "Filtered Results by:" + printPriority + printTimeEst  + printStatus + printCostEst
		
		#populate the list box
		boolT = False
		stringT =""
		#first line of list box (headers)
		lb_filterListbox.insert("end", "Name"+" "*16 + headPriority + headTimeEst  + headStatus+ headCostEst)
		lb_filterListbox.itemconfig(0, {"fg" :"purple"})
		length = len("Name"+" "*16 + headPriority + headTimeEst  + headStatus+ headCostEst)
		lb_filterListbox.insert("end", "="*length)
		
		for item in tasks:
			boolT, stringT = filterItems(item)
			if boolT:
				lb_filterListbox.insert("end", stringT)
			else:
				continue
		
		#reset drop down boxes/uncheck any boxes
		status.set("Status..")
		priority.set("Priority..")
		timeEst.set("Time Estimate..")
		costEst.set("Cost Estimate..")
		chk_CostEstBox.deselect()
		chk_StatusBox.deselect()
		chk_TimeEstBox.deselect()
		chk_PriorityBox.deselect()
			
	#create pop up window to display details of selected task
	viewFilter_PopUp = tkinter.Toplevel()
	viewFilter_PopUp.title("Filter Tasks")
	viewFilter_PopUp.title("Filter Tasks")
	viewFilter_PopUp.geometry("600x600+575+0")
	
	#Labels across top
	lbl_onOff = tkinter.Label(viewFilter_PopUp, text = "On/Off", bg = "white")
	lbl_onOff.grid(row=0, column =0)
	
	lbl_filter = tkinter.Label(viewFilter_PopUp, text = "Filter", bg = "white")
	lbl_filter.grid(row=0, column =1)
	
	lbl_filterResults = tkinter.Label(viewFilter_PopUp, text = "Filtered Results", bg = "white")
	lbl_filterResults.grid(row=0, column =3)
	
	#priority drop down
	priority = tkinter.StringVar(viewFilter_PopUp)
	priority.set("Priority..")
	drp_Priority = tkinter.OptionMenu(viewFilter_PopUp, priority, "None", "Low", "Med", "High")
	drp_Priority.grid(row = 1, column =1)
	#Priority check box
	chk_Priority=tkinter.BooleanVar(viewFilter_PopUp)
	chk_PriorityBox = tkinter.Checkbutton(viewFilter_PopUp, variable = chk_Priority, onvalue= True, offvalue= False)
	chk_PriorityBox.grid(row=1, column = 0)
	
	#time estimate drop down
	timeEst = tkinter.StringVar(viewFilter_PopUp)
	timeEst.set("Time Estimate..")
	drp_TimeEst = tkinter.OptionMenu(viewFilter_PopUp, timeEst, "None", "Short", "Med", "Long")
	drp_TimeEst.grid(row=2, column = 1)
	#TimeEst check box
	chk_TimeEst=tkinter.BooleanVar()
	chk_TimeEstBox = tkinter.Checkbutton(viewFilter_PopUp, variable = chk_TimeEst, onvalue=True, offvalue=False)
	chk_TimeEstBox.grid(row=2, column = 0)
	
	#cost Estimate drop down
	costEst = tkinter.StringVar(viewFilter_PopUp)
	costEst.set("Cost Estimate..")
	drp_CostEst = tkinter.OptionMenu(viewFilter_PopUp, costEst, "None ($0)", "Low  (<$150)", "Med  ($150-$500)", "High  ($500-$1500)", "Very High  (>$1500)")
	drp_CostEst.grid(row=4, column = 1)
	#cost Est check box
	chk_CostEst=tkinter.BooleanVar()
	chk_CostEstBox = tkinter.Checkbutton(viewFilter_PopUp, variable = chk_CostEst, onvalue=True, offvalue=False)
	chk_CostEstBox.grid(row=4, column = 0)
	
	#status drop down
	status = tkinter.StringVar(viewFilter_PopUp)
	status.set("Status..")
	drp_Status = tkinter.OptionMenu(viewFilter_PopUp, status, "Planned", "Started", "Waiting", "50%", "90%", "Completed!")
	drp_Status.grid(row=3,column=1)
	#status check box
	chk_Status=tkinter.BooleanVar()
	chk_StatusBox = tkinter.Checkbutton(viewFilter_PopUp, variable = chk_Status, onvalue=True, offvalue=False)
	chk_StatusBox.grid(row=3, column = 0)
	
	#listbox
	lb_filterListbox = tkinter.Listbox(viewFilter_PopUp)
	lb_filterListbox.config(width = 40, height = 20, font = "Courier")
	lb_filterListbox.grid(row= 2, column = 3, rowspan = 7, columnspan = 4)
	
	#ok button
	btn_okBtn = tkinter.Button(viewFilter_PopUp, text = "Ok", command = updateListFilter)
	btn_okBtn.grid(row = 15, column = 0)
	
	#Close Button
	btn_closeBtn = tkinter.Button(viewFilter_PopUp, text = "Close", command = viewFilter_PopUp.destroy)
	btn_closeBtn.grid(row = 15, column = 3)

def match(a, b):
	return SequenceMatcher(None, a, b).ratio()

'''FIXME -- continue working on the search function'''
def search():
	found = False
	searchFor = txt_searchTask.get().capitalize()
	for item in tasks:
		if item['tName'] == searchFor:
			index = tasks.index(item)
			tasks[0], tasks[index] = tasks[index], tasks[0]
			update_listbox()
			lb_tasks.select_set(0)
			lb_tasks.activate(0)
			viewTask()
			found = True
		if match(searchFor, item['tName']) > .75:
			print(item['tName'], " %s%% match" %int(match(searchFor, item['tName'])*100))
	
	if not found:
		messagebox.showwarning("Not found!", "%s not found!" %searchFor)
	txt_searchTask.delete(0, 'end')
	"""have a else with message box saying doesn't exsist"""

def materialsList():
	
	
	#function to add materials in from root
	def addMatIn():
		#get active task
		task = lb_tasks.get("active")
		for item in tasks:
			if item['tName'] == task:
				selTask = item
							
		lb_materialListbox.insert('end', "---" + selTask['tName'] +"---")
		for mat in selTask['tMaterials']:
			lb_materialListbox.insert('end', mat)
	
	#function to print the materials list
	def printLB():
		matOut = open('materialsPrint.txt','w')
		matOut.write("Materials List\n")
		matOut.write(datetime.datetime.today().strftime("%m/%d/%y")+'\n')
		matOut.write("="*50+'\n')
		for item in lb_materialListbox.get(0, 'end'):
			matOut.write(item+'\n')
		
		matOut.close()
			
			
	#Create pop up
	materialsList_PopUp = tkinter.Toplevel()
	materialsList_PopUp.title("Materials List")
	materialsList_PopUp.geometry("400x425+575+0")
	
	#create list box
	lb_materialListbox = tkinter.Listbox(materialsList_PopUp)
	lb_materialListbox.config(width = 40, height = 20, font = "Courier")
	lb_materialListbox.grid(row= 1, column = 1, rowspan = 7, columnspan = 4)
	
	#add materials in button
	btn_addMatIn = tkinter.Button(materialsList_PopUp, text = "Add Materials in", fg="green", bg = "white", command = addMatIn)
	btn_addMatIn.grid(row = 1, column =0)
	
	#print button
	btn_printMat = tkinter.Button(materialsList_PopUp, text = "Print this List", fg ="green", bg = "white", command = printLB)
	btn_printMat.grid(row = 8, column = 1)

#PlaceHolder function to test buttons/menus/etc
def hello():
	print("hello")

#open the file and read into list tasks
with open("toDoSave.csv") as f_obj:
	csv_dict_reader(saveFile)
	
	
#create menuBar at top of root
menubar = tkinter.Menu(root)
root.config(menu=menubar)

# create a pulldown menu, and add it to the menu bar
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=saveTasks)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create edit menu
editmenu = tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="Add a new Task", command=add_task)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

#create help menu
helpmenu = tkinter.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)



lbl_title = tkinter.Label(root, text = "To-Do-List", bg = "white")
lbl_title.grid(row=0, column =0)

#lbl_display = tkinter.Label(root, text="Enter a task Here:", bg ="white")
#lbl_display.grid(row=0, column =1)

#txt_input = tkinter.Entry(root, width = 15)
#txt_input.grid(row=1, column = 1)

btn_addTask = tkinter.Button(root, text = "Add Task", fg = "green", bg = "white", command = add_task)
btn_addTask.grid(row=1, column =0)

btn_markComplete = tkinter.Button(root, text = "ok", fg = "green", bg="white", command = markComplete)
btn_markComplete.grid(row=1, column = 1)
markStatus = tkinter.StringVar(root)
markStatus.set("Change Status..")#initial value
drp_markStatus = tkinter.OptionMenu(root, markStatus,"Planned", "Started", "Waiting", "50%", "90%", "Completed!")
drp_markStatus.grid(row =0, column = 1)

btn_delAll = tkinter.Button(root, text = "Delete All", fg = "green", bg = "white", command =delAll )
btn_delAll.grid(row=3, column =0)

btn_delOne = tkinter.Button(root, text = "Delete", fg = "green", bg = "white", command =delOne )
btn_delOne.grid(row=4, column =0)

btn_sortAsc = tkinter.Button(root, text = "Sort Ascending", fg = "green", bg = "white", command = sortAsc )
btn_sortAsc.grid(row=5, column =0)

btn_sortDsc = tkinter.Button(root, text = "Sort Decending", fg = "green", bg = "white", command = sortDsc)
btn_sortDsc.grid(row=6, column =0)

btn_filter = tkinter.Button(root, text = "Filter Tasks", fg = "green", bg = "white", command = filterTasks)
btn_filter.grid(row=7, column =0)

"""FIXME -- previously updated label -- label no longer exists"""
btn_chooRand = tkinter.Button(root, text = "Choose Random", fg = "green", bg = "white", command = chooRand)
btn_chooRand.grid(row=8, column =0)

"""FIXME --Previously updated label --- label no longer exists"""
btn_numOfTasks = tkinter.Button(root, text = "Number of Tasks", fg = "green", bg = "white", command = numOfTasks )
btn_numOfTasks.grid(row=9, column =0)

btn_viewTask = tkinter.Button(root, text = "View Task Details", fg = "green", bg = "white", command = viewTask)
btn_viewTask.grid(row=10, column = 0)

"""FIXME finish search bar!"""

txt_searchTask = tkinter.Entry(root, width = 20)
txt_searchTask.grid(row = 10, column = 1)
btn_searchTask = tkinter.Button(root, text = "Search", fg = "green", bg = "white", command = search)
btn_searchTask.grid(row=11, column =1)

btn_materialsList = tkinter.Button(root, text = "Create Materials List", fg ='green', bg = "white", command = materialsList)
btn_materialsList.grid(row = 11, column = 0)

btn_exit = tkinter.Button(root, text = "Exit", fg = "green", bg = "white", command = exit)
btn_exit.grid(row=12, column =0)

btn_save = tkinter.Button(root, text = "Save", fg = "green", bg = "white", command = saveTasks)
btn_save.grid(row=12, column = 1)

lb_tasks =  tkinter.Listbox(root, activestyle ='dotbox')
lb_tasks.grid(row=3, column =1, rowspan = 7)

update_listbox()








#start the main events loop
root.mainloop()