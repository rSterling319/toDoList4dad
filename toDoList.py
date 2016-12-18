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

"""

#Create The GUI Elements
import tkinter
from tkinter import messagebox
import random
#import taskClass
import csv

#create root window
root = tkinter.Tk()

#change root window background color
root.configure(bg="white")

#sets the title bar name
root.title("To-Do-List")

#set the window size
root.geometry("300x300+250+50")

#create empty list
tasks = []
#open save file
saveFile = open("toDoSave.csv",'r')

"""FIXME does not work yet
	-this seems really inefficient.. there has got to be an easier way--also does not work
"""




print(tasks)
#for Testing defalut list
#tasks = ["Pick up Poo", "Do Dishes", "Exercise"]
#functions
def csv_dict_reader(file_obj):
	"""
	Read a CSV file using a csv.DictReader
	"""
	
	reader = csv.DictReader(file_obj, delimiter=',')
	for line in reader:
		tasks.append(line)
	
	
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

def add_task():
	
	def addTaskIn():
		#get the task to add #tName|tDescription|tLocation|tTimeEst|tTimeStart|tTimeFinish|tCostEst|tCostAct|tPriority|tStatus
		newTask = {"tName":txt_addTask.get().capitalize(),"tDescription":txt_addDesc.get(),"tLocation": txt_addLocation.get(), "tTimeEst":addTimeEst.get(), "tTimeStart": 0, "tTimeFinish": 0,"tCostEst":addCostEst.get(),"tCostAct":0,"tPriority":addPriority.get(),"tStatus":addStatus.get()}
		
		duplicate = False
		
		#make sure !empty
		if txt_addTask.get() != "":
			
			#tasks.append(newTask)
			#update_listbox()
			
			for item in tasks:
				if newTask['tName'] == item['tName']:
					confirm = messagebox.askyesno("Duplicate Found", " %s already in To-Do-List!\n Do you want to add anyway?" %newTask["tName"].capitalize())
					if confirm:
						tasks.append(newTask)
						update_listbox()
						duplicate = True
						break
					else:
						break
				else:
					continue
			if not duplicate:
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
	
	#Add the task
	btn_AddTask = tkinter.Button(add_task_PopUp, text = "Add this Task", fg = "green", bg = "white", command =addTaskIn)
	btn_AddTask.grid(row=10, column = 0)
	#Exit popup
	btn_Done = tkinter.Button(add_task_PopUp, text = "Done", fg = "green", bg = "white", command =add_task_PopUp.destroy)
	btn_Done.grid(row=10, column = 1)
	
	

	

def markComplete():
	task=lb_tasks.get("active")
	for item in tasks:
		if item.name == task:
			index = tasks.index(item)
	lb_tasks.itemconfig(index, {"fg" :"red"})
		
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
	tasks.sort()
	#update the list box
	update_listbox()
	
def sortDsc():
	tasks.sort()
	#reverse lists
	tasks.reverse()
	#update the list box
	update_listbox()

def chooRand():
	#choose a random task
	task = random.choice(tasks)
	#update display label
	lbl_display["text"]=task.name
	
def numOfTasks():
	#get number of tasks
	number_of_tasks = len(tasks)
	#create and format message to dispay
	msg = "Number of Tasks: %s" %number_of_tasks
	#display message
	lbl_display["text"] = msg

def saveTasks():
	#create list that contains the fild names
	fieldnames = ["tName","tTimeStart","tLocation","tStatus","tPriority","tDescription","tTimeEst","tTimeFinish","tCostEst","tCostAct"]
	#write to file
	with open("toDoSave.csv", "w", newline='') as out_file:
		writer = csv.DictWriter(out_file,delimiter=',',fieldnames=fieldnames)
		writer.writeheader()
		for row in tasks:
			writer.writerow(row)
	
	messagebox.showinfo("Saved", "Your To-Do-List has been saved!")


#open the file and read into list tasks
with open("toDoSave.csv") as f_obj:
	csv_dict_reader(saveFile)
	
"""	HOW TO Iterate through data
print(tasks)
print('\n')
for item in tasks:
	print('\n')
	for value in item.keys():
		print (item[value])
"""



lbl_title = tkinter.Label(root, text = "To-Do-List", bg = "white")
lbl_title.grid(row=0, column =0)

lbl_display = tkinter.Label(root, text="Enter a task Here:", bg ="white")
lbl_display.grid(row=0, column =1)

txt_input = tkinter.Entry(root, width = 15)
txt_input.grid(row=1, column = 1)

btn_addTask = tkinter.Button(root, text = "Add Task", fg = "green", bg = "white", command = add_task)
btn_addTask.grid(row=1, column =0)

btn_markComplete = tkinter.Button(root, text = "Mark as Complete", fg = "green", bg="white", command = markComplete)
btn_markComplete.grid(row=2, column = 0)

btn_delAll = tkinter.Button(root, text = "Delete All", fg = "green", bg = "white", command =delAll )
btn_delAll.grid(row=3, column =0)

btn_delOne = tkinter.Button(root, text = "Delete", fg = "green", bg = "white", command =delOne )
btn_delOne.grid(row=4, column =0)

btn_sortAsc = tkinter.Button(root, text = "Sort Ascending", fg = "green", bg = "white", command = sortAsc )
btn_sortAsc.grid(row=5, column =0)

btn_sortDsc = tkinter.Button(root, text = "Sort Decending", fg = "green", bg = "white", command = sortDsc)
btn_sortDsc.grid(row=6, column =0)

btn_chooRand = tkinter.Button(root, text = "Choose Random", fg = "green", bg = "white", command = chooRand)
btn_chooRand.grid(row=7, column =0)

btn_numOfTasks = tkinter.Button(root, text = "Number of Tasks", fg = "green", bg = "white", command = numOfTasks )
btn_numOfTasks.grid(row=8, column =0)

btn_exit = tkinter.Button(root, text = "Exit", fg = "green", bg = "white", command = exit)
btn_exit.grid(row=10, column =0)

btn_save = tkinter.Button(root, text = "Save", fg = "green", bg = "white", command = saveTasks)
btn_save.grid(row=10, column = 1)

lb_tasks =  tkinter.Listbox(root)
lb_tasks.grid(row=2, column =1, rowspan = 7)

update_listbox()








#start the main events loop
root.mainloop()