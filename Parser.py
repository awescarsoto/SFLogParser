__author__ = 'oxsc'

from Tkinter import *
import tkFileDialog
import ttk
import DebugTypeInfo


########################################################################################################################
def choosefile():
    # Remove other widgets
    fileButton.grid_remove()
    pasteButton.grid_remove()

    # Prompt for the file
    f = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')
    while f is None:
        f = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')

    # Format the tree with columns and scrollbars that resize
    treeStructure.column("#0", stretch=TRUE)
    ysb = ttk.Scrollbar(root, orient='vertical', command=treeStructure.yview)
    xsb = ttk.Scrollbar(root, orient='horizontal', command=treeStructure.xview)
    treeStructure.configure(yscroll=ysb.set, xscroll=xsb.set)
    treeStructure.heading('#0', text="Methods Tree", anchor='w')
    treeStructure.grid(row=0, column=0, sticky='nsew')
    treeStructure.columnconfigure(0, weight=1)
    ysb.grid(row=0, column=1, sticky='nse')
    xsb.grid(row=1, column=0, sticky='sew')
    treeStructure.grid(sticky="nesw")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    treeStructure.columnconfigure(0, weight=1)
    treeStructure.rowconfigure(0, weight=1)

    # Variables
    hierarchicalLevel = 0
    stack = []

    for line in f:   # Iterate over the rest of lines in the file
        if "|" in line:  # Separate lines by the pipe and remove newline characters
            line = line.rstrip('\n')  # Remove the newline characters
            splitLine = line.split("|")  # Split into array by pipes
            if splitLine[1] in startingKeywords:  # Check if the name is
                hierarchicalLevel += 1
                if len(stack) == 0:
                    stack.append(treeStructure.insert('', 'end', text=DebugTypeInfo.getInfo(splitLine), image=images[splitLine[1]]))
                else:
                    stack.append(treeStructure.insert(stack[len(stack)-1], 'end', text=DebugTypeInfo.getInfo(splitLine), image=images[splitLine[1]]))
            elif splitLine[1] in endingKeywords:
                hierarchicalLevel -= 1
                stack.pop()

    f.close()  # close the file when everything is done
    return


########################################################################################################################
def initialMenu():
    # Remove other widgets
    treeStructure.grid_remove()


    '''
    callout.set('on')
    codeUnit.set('on')
    cumulativeProfiling.set('on')
    dml.set('on')
    method.set('on')
    soql.set('on')
    sosl.set('on')
    systemMode.set('on')
    validationRule.set('on')
    visualforceDeserialize.set('on')
    visualforceEvaluate.set('on')
    visualforceSerialize.set('on')
    workflow.set('on')
    '''

    # Put widgets on the frame
    fileButton.grid(row=0, column=0, sticky='nesw')
    pasteButton.grid(row=0, column=1, sticky='nesw')

    # Put widgets on the frame and set default values for buttons
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.invoke()

    '''
    calloutCheck.grid(sticky='w')
    codeUnitCheck.grid(sticky='w')
    cumulativeProfilingCheck.grid(sticky='w')
    dmlCheck.grid(sticky='w')
    methodCheck.grid(sticky='w')
    soqlCheck.grid(sticky='w')
    soslCheck.grid(sticky='w')
    systemModeCheck.grid(sticky='w')
    validationRuleCheck.grid(sticky='w')
    visualforceDeserializCheck.grid(sticky='w')
    visualforceEvaluateCheck.grid(sticky='w')
    visualforceSerializeCheck.grid(sticky='w')
    workflowCheck.grid(sticky='w')
    '''


########################################################################################################################
# Global variables for things that increase, decrease, and the level of hierarchy currently at
startingKeywords = ['CALLOUT_REQUEST', 'CODE_UNIT_STARTED',
              'CUMULATIVE_PROFILING_BEGIN', 'DML_BEGIN', 'METHOD_ENTRY', 'SOQL_EXECUTE_BEGIN',
              'SOSL_EXECUTE_BEGIN', 'SYSTEM_MODE_ENTER', 'VALIDATION_RULE',
              'VF_DESERIALIZE_VIEWSTATE_BEGIN', 'VF_EVALUATE_FORMULA_BEGIN',
              'VF_SERIALIZE_VIEWSTATE_BEGIN', 'WF_CRITERIA_BEGIN']

endingKeywords = ['CALLOUT_RESPONSE', 'CODE_UNIT_FINISHED',
              'CUMULATIVE_PROFILING_END', 'DML_END', 'METHOD_EXIT', 'SOQL_EXECUTE_END',
              'SOSL_EXECUTE_END', 'SYSTEM_MODE_EXIT', 'VALIDATION_PASS', 'VALIDATION_FAIL',
              'VF_DESERIALIZE_VIEWSTATE_END', 'VF_EVALUATE_FORMULA_END',
              'VF_SERIALIZE_VIEWSTATE_END', 'WF_CRITERIA_END']

keywordsChosen = []
checkButtonArray = []

# Initiate the windows
root = Tk()
root.title("Salesforce Debug Methods Tree")
root.geometry("800x600")

# Variables to store Checkbutton info
callout = StringVar()
codeUnit = StringVar()
cumulativeProfiling = StringVar()
dml = StringVar()
method = StringVar()
soql = StringVar()
sosl = StringVar()
systemMode = StringVar()
validationRule = StringVar()
visualforceDeserialize = StringVar()
visualforceEvaluate = StringVar()
visualforceSerialize = StringVar()
workflow = StringVar()

# Buttons to be created
fileButton = ttk.Button(root, text="Choose File", command=lambda: choosefile())
pasteButton = ttk.Button(root, text="Paste Log")

# Checkbuttons
for keyword in startingKeywords:
    newCheckButton = ttk.Checkbutton(root, text=DebugTypeInfo.convertName(keyword))
    checkButtonArray.append(newCheckButton)

'''
calloutCheck = ttk.Checkbutton(root, text='Callout Requests', variable=callout, onvalue='on', offvalue='off')
codeUnitCheck = ttk.Checkbutton(root, text='Code Units', variable=codeUnit, onvalue='on', offvalue='off')
cumulativeProfilingCheck = ttk.Checkbutton(root, text='Cumulative Profiling', variable=cumulativeProfiling, onvalue='on', offvalue='off')
dmlCheck = ttk.Checkbutton(root, text='DML', variable=dml, onvalue='on', offvalue='off')
methodCheck = ttk.Checkbutton(root, text='Methods', variable=method, onvalue='on', offvalue='off')
soqlCheck = ttk.Checkbutton(root, text='SOQL', variable=soql, onvalue='on', offvalue='off')
soslCheck = ttk.Checkbutton(root, text='SOSL', variable=sosl, onvalue='on', offvalue='off')
systemModeCheck = ttk.Checkbutton(root, text='System Modes', variable=systemMode, onvalue='on', offvalue='off')
validationRuleCheck = ttk.Checkbutton(root, text='Validation Rules', variable=validationRule, onvalue='on', offvalue='off')
visualforceDeserializCheck = ttk.Checkbutton(root, text='Visualforce Deserialize', variable=visualforceDeserialize, onvalue='on', offvalue='off')
visualforceEvaluateCheck = ttk.Checkbutton(root, text='Visualforce Evaluate', variable=visualforceEvaluate, onvalue='on', offvalue='off')
visualforceSerializeCheck = ttk.Checkbutton(root, text='Visualforce Serialize', variable=visualforceSerialize, onvalue='on', offvalue='off')
workflowCheck = ttk.Checkbutton(root, text='Workflows', variable=workflow, onvalue='on', offvalue='off')
'''

# Create the images
blankImage = PhotoImage(file='blank.gif')
workflowImage = PhotoImage(file='gear_happy2.gif')
validationRuleImage = PhotoImage(file='VR.gif')
visualForceImage = PhotoImage(file='VF.gif')
dmlImage = PhotoImage(file='DML.gif')
soslImage = PhotoImage(file='SOSL.gif')
soqlImage = PhotoImage(file='SOQL.gif')

# Associate the images in a dictionary
images = {'CALLOUT_REQUEST': blankImage,
              'CODE_UNIT_STARTED': blankImage,
              'CONSTRUCTOR_ENTRY': blankImage,
              'CUMULATIVE_LIMIT_USAGE': blankImage,
              'CUMULATIVE_PROFILING_BEGIN': blankImage,
              'DML_BEGIN': dmlImage,
              'EXECUTION_STARTED': blankImage,
              'METHOD_ENTRY': blankImage,
              'SOQL_EXECUTE_BEGIN': soqlImage,
              'SOSL_EXECUTE_BEGIN': soslImage,
              'SYSTEM_CONSTRUCTOR_ENTRY': blankImage,
              'SYSTEM_METHOD_ENTRY': blankImage,
              'SYSTEM_MODE_ENTER': blankImage,
              'VARIABLE_SCOPE_BEGIN': blankImage,
              'VALIDATION_RULE': validationRuleImage,
              'VF_DESERIALIZE_VIEWSTATE_BEGIN': visualForceImage,
              'VF_EVALUATE_FORMULA_BEGIN': visualForceImage,
              'VF_SERIALIZE_VIEWSTATE_BEGIN': visualForceImage,
              'WF_CRITERIA_BEGIN': workflowImage,
              'WF_RULE_EVAL_BEGIN': workflowImage}

# Create the Treeview
treeStructure = ttk.Treeview(root, selectmode="extended")

# Startup
initialMenu()
root.mainloop()






