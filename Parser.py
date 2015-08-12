__author__ = 'oxsc'

from Tkinter import *
import tkFileDialog
import ttk
import DebugTypeInfo


########################################################################################################################
def getImage(logLines, index):

    currentLine = logLines[index]
    splitCurrent = currentLine.rstrip('\n').split("|")
    debugType = splitCurrent[1]

    if debugType == 'CALLOUT_REQUEST':
        return blankImage
    elif debugType == 'CODE_UNIT_STARTED':
        return blankImage
    elif debugType == 'CONSTRUCTOR_ENTRY':
        return blankImage
    elif debugType == 'CUMULATIVE_LIMIT_USAGE':
        return  blankImage
    elif debugType == 'CUMULATIVE_PROFILING_BEGIN':
        return blankImage
    elif debugType == 'DML_BEGIN':
        return dmlImage
    elif debugType == 'EXECUTION_STARTED':
        return blankImage
    elif debugType == 'METHOD_ENTRY':
        return blankImage
    elif debugType == 'SOQL_EXECUTE_BEGIN':
        return soqlImage
    elif debugType == 'SOSL_EXECUTE_BEGIN':
        return soslImage
    elif debugType == 'SYSTEM_CONSTRUCTOR_ENTRY':
        return blankImage
    elif debugType == 'SYSTEM_METHOD_ENTRY':
        return blankImage
    elif debugType == 'SYSTEM_MODE_ENTER':
        return blankImage
    elif debugType == 'VARIABLE_SCOPE_BEGIN':
        return blankImage
    elif debugType == 'VALIDATION_RULE':
        for x in range(index, len(logLines)):
            currentLine = logLines[x]
            if "|" in currentLine:
                passOrFailLine = currentLine.rstrip('\n').split("|")
                passOrFail = passOrFailLine[1]
                if passOrFail == "VALIDATION_PASS":
                    return passImage
                if passOrFail == "VALIDATION_FAIL":
                    return failImage
                if passOrFail == "VALIDATION_ERROR":
                    return failImage
        return failImage
    elif debugType == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        return visualForceImage
    elif debugType == 'VF_EVALUATE_FORMULA_BEGIN':
        return visualForceImage
    elif debugType == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        return visualForceImage
    elif debugType == 'WF_CRITERIA_BEGIN':
        return workflowImage
    elif debugType == 'WF_RULE_EVAL_BEGIN':
        return workflowImage

    return blankImage


########################################################################################################################
def getTreeReady():
    # Clear the tree
    treeStructure.delete(*treeStructure.get_children())

    # Remove other widgets from view
    fileButton.grid_remove()
    pasteButton.grid_remove()
    resetButton.grid_remove()
    selectButton.grid_remove()
    deselectButton.grid_remove()
    logEntry.grid_remove()
    continueButton.grid_remove()
    logYScrolling.grid_remove()
    for button in checkButtonArray:
        button.grid_remove()

    # Add in tree structure settings to expand
    treeStructure.column("#0", stretch=TRUE)
    treeStructure.heading('#0', text="Methods Tree", anchor='w')
    treeStructure.grid(row=0, column=0, sticky='nsew')
    treeStructure.columnconfigure(0, weight=1)
    treeYScrolling.grid(row=0, column=1, sticky='nse')
    treeXScrolling.grid(row=1, column=0, sticky='sew')
    treeStructure.grid(sticky="nesw")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    treeStructure.columnconfigure(0, weight=1)
    treeStructure.rowconfigure(0, weight=1)

    return


########################################################################################################################
def checkSelectedKeywords():
    # Clear the list
    keywordsChosen[:] = []

    # check if a button was selected and use the value to add it to the list of keywords chosen
    for button in checkButtonArray:
        if button.instate(['selected']):
            keywordsChosen.append(button['onvalue'])
    return


########################################################################################################################
def processLogFile(logFile):
    # Add the keywords to be looked for
    checkSelectedKeywords()

    # Get the tree ready
    getTreeReady()

    # Variables
    hierarchicalLevel = 0
    stack = []
    lines = []

    # Add lines to array as a buffer
    for line in logFile:
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            splitLine = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if splitLine[1] in startingKeywords:  # Check if the name is
                hierarchicalLevel += 1
                if len(stack) == 0:
                    stack.append(treeStructure.insert('', 'end', text=DebugTypeInfo.getInfo(splitLine), image=getImage(lines, x)))
                else:
                    stack.append(treeStructure.insert(stack[len(stack)-1], 'end', text=DebugTypeInfo.getInfo(splitLine), image=getImage(lines, x)))
            elif splitLine[1] in endingKeywords:
                hierarchicalLevel -= 1
                stack.pop()

    logFile.close()  # close the file when everything is done
    resetButton.grid()  # add the reset button onto the side
    root.mainloop()

########################################################################################################################
def processPastedLog(log):
    # Add the keywords to be looked for
    checkSelectedKeywords()

    # Get the tree ready
    getTreeReady()

    # Variables
    hierarchicalLevel = 0
    stack = []
    lines = []

    # Determine amount of lines to create a for loop
    numLines = int(log.index('end-1c').split('.')[0])

    # Go through and grab each line
    for x in range(1, numLines):
        line = log.get(float(x), float(x+1))
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            splitLine = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if splitLine[1] in startingKeywords:  # Check if the name is
                hierarchicalLevel += 1
                if len(stack) == 0:
                    stack.append(treeStructure.insert('', 'end', text=DebugTypeInfo.getInfo(splitLine), image=getImage(lines, x)))
                else:
                    stack.append(treeStructure.insert(stack[len(stack)-1], 'end', text=DebugTypeInfo.getInfo(splitLine), image=getImage(lines, x)))
            elif splitLine[1] in endingKeywords:
                hierarchicalLevel -= 1
                stack.pop()

    resetButton.grid()  # add the reset button onto the side
    root.mainloop()


########################################################################################################################
def selectAll():
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.state(['selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def deselectAll():
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.state(['!selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def initialMenu():
    # Remove other widgets
    treeStructure.grid_remove()
    treeXScrolling.grid_remove()
    treeYScrolling.grid_remove()
    logYScrolling.grid_remove()
    logEntry.grid_remove()
    continueButton.grid_remove()
    root.columnconfigure(0, weight=0)
    root.rowconfigure(0, weight=0)

    # Put initial widgets on the frame
    fileButton.grid(row=0, column=0, sticky='nesw')
    pasteButton.grid(row=0, column=1, sticky='nesw')
    resetButton.grid(row=0, column=2, sticky='nesw')
    selectButton.grid(row=1, column=0, sticky='nesw')
    deselectButton.grid(row=1, column=1, sticky='nesw')

    # Put checkbuttons on the frame and set default values for buttons as checkmarked
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.state(['selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()

    root.mainloop()


########################################################################################################################
def chooseFile():
    # Prompt for the file
    logFile = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')

    # Go back to menu if a file wasn't chosen such as cancel or close
    if logFile is None:
        initialMenu()
    else:
        processLogFile(logFile)


########################################################################################################################
def pasteLog():
    # Remove other widgets
    treeStructure.grid_remove()
    treeXScrolling.grid_remove()
    treeYScrolling.grid_remove()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    fileButton.grid_remove()
    pasteButton.grid_remove()
    resetButton.grid_remove()
    for button in checkButtonArray:
        button.grid_remove()

    # Clear the log
    logEntry.delete(1.0, END)

    # Add the paste widget
    logYScrolling.grid(row=0, column=1, sticky='nse')
    logEntry.grid(row=0, column=0, sticky="nesw")
    continueButton.grid(row=1, column=0, sticky='nesw')
    resetButton.grid(row=2, column=0)

    return

########################################################################################################################
# Global variables for things that increase and decrease the level of hierarchy currently at
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

# Translation to a friendlier output for the checkbuttons
keywordTranslations = {'CALLOUT_REQUEST': 'Callout Requests',
              'CODE_UNIT_STARTED': 'Code Units',
              'CONSTRUCTOR_ENTRY': 'Constructors',
              'CUMULATIVE_LIMIT_USAGE': 'Cumulative Limits',
              'CUMULATIVE_PROFILING_BEGIN': 'Cumulative Profilings',
              'DML_BEGIN': 'DML Operations',
              'EXECUTION_STARTED': 'Executions',
              'METHOD_ENTRY': 'Methods',
              'SOQL_EXECUTE_BEGIN': 'SOQL Queries',
              'SOSL_EXECUTE_BEGIN': 'SOSL Queries',
              'SYSTEM_CONSTRUCTOR_ENTRY': 'System Constructors',
              'SYSTEM_METHOD_ENTRY': 'System Methods',
              'SYSTEM_MODE_ENTER': 'System Modes',
              'VARIABLE_SCOPE_BEGIN': 'Variable Scopes',
              'VALIDATION_RULE': 'Validation Rules',
              'VF_DESERIALIZE_VIEWSTATE_BEGIN': 'Visualforce Deserialize',
              'VF_EVALUATE_FORMULA_BEGIN': 'Visualforce Evaluate',
              'VF_SERIALIZE_VIEWSTATE_BEGIN': 'Visualforce Serialize',
              'WF_CRITERIA_BEGIN': 'Workflow Rules',
              'WF_RULE_EVAL_BEGIN': 'Workflow Evaluations'}

keywordsChosen = []  # empty list to hold keywords that will be selected
checkButtonArray = []  # empty list to hold checkbuttons that will be created

# Initiate the window
root = Tk()
root.title("Salesforce Debug Methods Tree")
root.geometry("800x600")

# Create buttons
fileButton = ttk.Button(root, text="Choose File", command=lambda: chooseFile())
pasteButton = ttk.Button(root, text="Paste Log", command=lambda: pasteLog())
resetButton = ttk.Button(root, text="Reset", command=lambda: initialMenu())
continueButton = ttk.Button(root, text="Continue", command=lambda: processPastedLog(logEntry))
selectButton = ttk.Button(root, text="Select All", command=lambda: selectAll())
deselectButton = ttk.Button(root, text="Deselect All", command=lambda: deselectAll())

# Create checkbuttons automatically
for keyword in startingKeywords:
    newCheckButton = ttk.Checkbutton(root, text=keywordTranslations[keyword], onvalue=keyword, offvalue='off')
    checkButtonArray.append(newCheckButton)

# Create the images
blankImage = PhotoImage(file='blank.gif')
workflowImage = PhotoImage(file='gear_happy2.gif')
validationRuleImage = PhotoImage(file='VR.gif')
visualForceImage = PhotoImage(file='VF.gif')
dmlImage = PhotoImage(file='DML.gif')
soslImage = PhotoImage(file='SOSL.gif')
soqlImage = PhotoImage(file='SOQL.gif')
passImage = PhotoImage(file='pass.gif')
failImage = PhotoImage(file='fail.gif')

# Create the Treeview
treeStructure = ttk.Treeview(root, selectmode="extended")

# Create scrollbars to be added to tree structure later
treeYScrolling = ttk.Scrollbar(root, orient='vertical', command=treeStructure.yview)
treeXScrolling = ttk.Scrollbar(root, orient='horizontal', command=treeStructure.xview)
treeStructure.configure(yscroll=treeYScrolling.set, xscroll=treeXScrolling.set)

# Create place to paste logs
logEntry = Text(root)
logYScrolling = ttk.Scrollbar(root, orient='vertical', command=logEntry.yview)
logEntry.configure(yscroll=logYScrolling.set)

# Startup
initialMenu()
root.mainloop()






