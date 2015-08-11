__author__ = 'oxsc'

from Tkinter import *
import tkFileDialog
import ttk
import DebugTypeInfo


def choosefile():
    f = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    while f is None:
        f = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')

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
    stack = []

    # Iterate over the rest of lines in the file
    for line in f:
        # Separate lines by the pipe and remove newline characters
        if "|" in line:
            line = line.rstrip('\n')
            splitLine = line.split("|")
            if splitLine[1] in increasers:
                currLevel += 1
                if len(stack) == 0:
                    stack.append(structure.insert('', 'end', text=DebugTypeInfo.getInfo(splitLine), image=images[splitLine[1]]))
                else:
                    stack.append(structure.insert(stack[len(stack)-1], 'end', text=DebugTypeInfo.getInfo(splitLine), image=images[splitLine[1]]))
            elif splitLine[1] in decreasers:
                currLevel -= 1
                stack.pop()

    f.close()  # close the file when everything is done

def initialMenu():
    fileButton = ttk.Button(root, text="Choose File", command=lambda: choosefile())
    pasteButton = ttk.Button(root, text="Paste Log")
    fileButton.grid()
    pasteButton.grid()



# Global variables for things that increase, decrease, and the level of hierarchy currently at
increasers = ['CALLOUT_REQUEST', 'CODE_UNIT_STARTED',
              'CUMULATIVE_PROFILING_BEGIN', 'DML_BEGIN', 'METHOD_ENTRY', 'SOQL_EXECUTE_BEGIN',
              'SOSL_EXECUTE_BEGIN', 'SYSTEM_MODE_ENTER', 'VALIDATION_RULE',
              'VF_DESERIALIZE_VIEWSTATE_BEGIN', 'VF_EVALUATE_FORMULA_BEGIN',
              'VF_SERIALIZE_VIEWSTATE_BEGIN', 'WF_CRITERIA_BEGIN']

decreasers = ['CALLOUT_RESPONSE', 'CODE_UNIT_FINISHED',
              'CUMULATIVE_PROFILING_END', 'DML_END', 'METHOD_EXIT', 'SOQL_EXECUTE_END',
              'SOSL_EXECUTE_END', 'SYSTEM_MODE_EXIT', 'VALIDATION_PASS', 'VALIDATION_FAIL',
              'VF_DESERIALIZE_VIEWSTATE_END', 'VF_EVALUATE_FORMULA_END',
              'VF_SERIALIZE_VIEWSTATE_END', 'WF_CRITERIA_END']

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
root.geometry("800x600")
blank = PhotoImage(file='blank.gif')
gear = PhotoImage(file='gear_happy2.gif')
validation = PhotoImage(file='VR.gif')
vf = PhotoImage(file='VF.gif')
dml = PhotoImage(file='DML.gif')
sosl = PhotoImage(file='SOSL.gif')
soql = PhotoImage(file='SOQL.gif')

images = {'CALLOUT_REQUEST': blank,
              'CODE_UNIT_STARTED': blank,
              'CONSTRUCTOR_ENTRY': blank,
              'CUMULATIVE_LIMIT_USAGE': blank,
              'CUMULATIVE_PROFILING_BEGIN': blank,
              'DML_BEGIN': dml,
              'EXECUTION_STARTED': blank,
              'METHOD_ENTRY': blank,
              'SOQL_EXECUTE_BEGIN': soql,
              'SOSL_EXECUTE_BEGIN': sosl,
              'SYSTEM_CONSTRUCTOR_ENTRY': blank,
              'SYSTEM_METHOD_ENTRY': blank,
              'SYSTEM_MODE_ENTER': blank,
              'VARIABLE_SCOPE_BEGIN': blank,
              'VALIDATION_RULE': validation,
              'VF_DESERIALIZE_VIEWSTATE_BEGIN': vf,
              'VF_EVALUATE_FORMULA_BEGIN': vf,
              'VF_SERIALIZE_VIEWSTATE_BEGIN': vf,
              'WF_CRITERIA_BEGIN': gear,
              'WF_RULE_EVAL_BEGIN': gear}


initialMenu()
root.mainloop()






