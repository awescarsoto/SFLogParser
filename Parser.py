__author__ = 'oxsc'

from Tkinter import *
import ttk

# Create the initial tree
'''
root = Tk()
structure = ttk.Treeview(root)

structure["columns"]=("one","two")
structure.column("one", width=100 )
structure.column("two", width=100)
structure.heading("one", text="coulmn A")
structure.heading("two", text="column B")

structure.insert("" , 0,    text="Line 1", values=("1A","1b"))

id2 = structure.insert("", 1, "dir2", text="Dir 2")
structure.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

##alternatively:
structure.insert("", 3, "dir3", text="Dir 3")
structure.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

structure.pack()
root.mainloop()
'''

# Open the file for reading
f = open("C:\Users\oxsc\Desktop\Log.txt", "r")

# Global variables for things that increase, decrease, and the level of hierarchy currently at
increasers = ['CALLOUT_REQUEST', 'CODE_UNIT_STARTED', 'CONSTRUCTOR_ENTRY', 'CUMULATIVE_LIMIT_USAGE',
              'CUMULATIVE_PROFILING_BEGIN', 'DML_BEGIN', 'EXECUTION_STARTED', 'METHOD_ENTRY', 'SOQL_EXECUTE_BEGIN',
              'SOSL_EXECUTE_BEGIN', 'SYSTEM_CONSTRUCTOR_ENTRY', 'SYSTEM_METHOD_ENTRY', 'SYSTEM_MODE_ENTER',
              'VARIABLE_SCOPE_BEGIN', 'VF_DESERIALIZE_VIEWSTATE_BEGIN', 'VF_EVALUATE_FORMULA_BEGIN',
              'VF_SERIALIZE_VIEWSTATE_BEGIN', 'WF_CRITERIA_BEGIN', 'WF_RULE_EVAL_BEGIN']
decreasers = ['CALLOUT_RESPONSE', 'CODE_UNIT_FINISHED', 'CONSTRUCTOR_EXIT', 'CUMULATIVE_LIMIT_USAGE_END',
              'CUMULATIVE_PROFILING_END', 'DML_END', 'EXECUTION_FINISHED', 'METHOD_EXIT', 'SOQL_EXECUTE_END',
              'SOSL_EXECUTE_END', 'SYSTEM_CONSTRUCTOR_EXIT', 'SYSTEM_METHOD_EXIT', 'SYSTEM_MODE_EXIT',
              'VARIABLE_SCOPE_END', 'VF_DESERIALIZE_VIEWSTATE_END', 'VF_EVALUATE_FORMULA_END',
              'VF_SERIALIZE_VIEWSTATE_END', 'WF_CRITERIA_END', 'WF_RULE_EVAL_END']
importantInfo = {'CALLOUT_REQUEST': 1, 'CODE_UNIT_STARTED': 4, 'CONSTRUCTOR_ENTRY': 1, 'CUMULATIVE_LIMIT_USAGE': 1,
                 'CUMULATIVE_PROFILING_BEGIN': 1, 'DML_BEGIN': 1, 'EXECUTION_STARTED': 1, 'METHOD_ENTRY': 4,
                 'SOQL_EXECUTE_BEGIN': 4, 'SOSL_EXECUTE_BEGIN': 1, 'SYSTEM_CONSTRUCTOR_ENTRY': 1,
                 'SYSTEM_METHOD_ENTRY': 3, 'SYSTEM_MODE_ENTER': 1,'VARIABLE_SCOPE_BEGIN': 1,
                 'VF_DESERIALIZE_VIEWSTATE_BEGIN': 1, 'VF_EVALUATE_FORMULA_BEGIN': 1,
                 'VF_SERIALIZE_VIEWSTATE_BEGIN': 1, 'WF_CRITERIA_BEGIN': 1, 'WF_RULE_EVAL_BEGIN': 1}
formatting = {'CALLOUT_REQUEST': 1,
              'CODE_UNIT_STARTED': 4,
              'CONSTRUCTOR_ENTRY': 1,
              'CUMULATIVE_LIMIT_USAGE': 1,
              'CUMULATIVE_PROFILING_BEGIN': 1,
              'DML_BEGIN': 1,
              'EXECUTION_STARTED': 1,
              'METHOD_ENTRY': 4,
              'SOQL_EXECUTE_BEGIN': 4,
              'SOSL_EXECUTE_BEGIN': 1,
              'SYSTEM_CONSTRUCTOR_ENTRY': 1,
              'SYSTEM_METHOD_ENTRY': 3,
              'SYSTEM_MODE_ENTER': 1,
              'VARIABLE_SCOPE_BEGIN': 1,
              'VF_DESERIALIZE_VIEWSTATE_BEGIN': 1,
              'VF_EVALUATE_FORMULA_BEGIN': 1,
              'VF_SERIALIZE_VIEWSTATE_BEGIN': 1,
              'WF_CRITERIA_BEGIN': 1,
              'WF_RULE_EVAL_BEGIN': 1}

# Initiate the tree
root = Tk()
root.title("Salesforce Debug Methods Tree")
structure = ttk.Treeview(root, selectmode="extended")

# Format the tree with columns and scrollbars that resize
structure.column("#0", stretch=TRUE)
ysb = ttk.Scrollbar(root, orient='vertical', command=structure.yview)
xsb = ttk.Scrollbar(root, orient='horizontal', command=structure.xview)
structure.configure(yscroll=ysb.set, xscroll=xsb.set)
structure.heading('#0', text="Methods Tree", anchor='w')
structure.grid(row=0, column=0, sticky='nsew')
structure.columnconfigure(0, weight=1)
ysb.grid(row=0, column=1, sticky='nse')
xsb.grid(row=1, column=0, sticky='sew')
structure.grid(sticky="nesw")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
structure.columnconfigure(0, weight=1)
structure.rowconfigure(0, weight=1)

# Variables
currLevel = 0
currChild = 0
stack = []

# Create first node
firstLineHit = False
while not firstLineHit:
    initial = f.readline()
    initial = initial.rstrip('\n')
    if "|" in initial:
        splitLine = initial.split("|")
        stack.append(structure.insert('', 'end', text=splitLine[importantInfo[splitLine[1]]]))
        firstLineHit = True

# Iterate over the rest of lines in the file
for line in f:

    # Separate lines by the pipe and remove newline characters
    if "|" in line:
        line = line.rstrip('\n')
        splitLine = line.split("|")
        if splitLine[1] in increasers:
            currLevel += 1
            stack.append(structure.insert(stack[len(stack) - 1], 'end', text=splitLine[importantInfo[splitLine[1]]]))
            print (currLevel * '\t') + splitLine[importantInfo[splitLine[1]]]  # Debugging info
        elif splitLine[1] in decreasers:
            currLevel -= 1
            stack.pop()
            print (currLevel * '\t') + "end"  # debugging info

f.close()  # close the file when everything is done
root.mainloop()  # Keeps the window open and running

