__author__ = 'oxsc'

from Tkinter import *
import tkFileDialog
import ttk


########################################################################################################################
def getInfo(logLines, index):
    currentLine = logLines[index]  # The line that was currently sent to the function
    splitCurrentLine = currentLine.rstrip('\n').split("|")  # Remove the newline character and split it by the pipes
    debugType = splitCurrentLine[1]  # This is our debug identifier at index 1

    # Defaults to be overwritten
    textInfo = ''
    imageInfo = blankImage
    currentCodeLine = ''

    if debugType == 'CALLOUT_REQUEST':
        textInfo =  splitCurrentLine[1]
    elif debugType == 'CODE_UNIT_STARTED':
        textInfo =  "Code Unit: " + splitCurrentLine[len(splitCurrentLine)-1]
    elif debugType == 'CONSTRUCTOR_ENTRY':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[1]
    elif debugType == 'CUMULATIVE_LIMIT_USAGE':
        textInfo =  splitCurrentLine[1]
    elif debugType == 'CUMULATIVE_PROFILING_BEGIN':
        textInfo =  splitCurrentLine[1]
    elif debugType == 'DML_BEGIN':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[3][3:] + " " + splitCurrentLine[4][5:]
        imageInfo = dmlImage
    elif debugType == 'EXCEPTION_THROWN':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo = "Exception: " + splitCurrentLine[3]
        imageInfo = warningImage
    elif debugType == 'EXECUTION_STARTED':
        textInfo =  splitCurrentLine[1]
    elif debugType == 'FATAL_ERROR':
        textInfo = splitCurrentLine[2]
        imageInfo = warningImage
    elif debugType == 'METHOD_ENTRY':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo = "Method: " + splitCurrentLine[len(splitCurrentLine)-1]
    elif debugType == 'SOQL_EXECUTE_BEGIN':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[len(splitCurrentLine)-1]
        imageInfo = soqlImage
    elif debugType == 'SOSL_EXECUTE_BEGIN':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[1]
        imageInfo = soslImage
    elif debugType == 'SYSTEM_CONSTRUCTOR_ENTRY':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[1]
    elif debugType == 'SYSTEM_METHOD_ENTRY':
        currentCodeLine = splitCurrentLine[2].strip('[]')
        textInfo =  splitCurrentLine[1]
    elif debugType == 'SYSTEM_MODE_ENTER':
        textInfo =  splitCurrentLine[1]
    elif debugType == 'VALIDATION_RULE':
        textInfo = splitCurrentLine[len(splitCurrentLine)-1]
        for x in range(index, len(logLines)):  # Look at the next few lines until the validation pass or fail
                currentLine = logLines[x]
                if "VALIDATION_PASS" in currentLine:
                    imageInfo = passImage
                    break
                if "VALIDATION_FAIL" in currentLine:
                    imageInfo = failImage
                    break
                if "VALIDATION_ERROR" in currentLine:
                    imageInfo = failImage
                    break
                else:
                    imageInfo = failImage  # In case something wasn't picked up
    elif debugType == 'VARIABLE_SCOPE_BEGIN':
        textInfo =  splitCurrentLine[1]
        currentCodeLine = splitCurrentLine[2].strip('[]')
    elif debugType == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        textInfo =  splitCurrentLine[1]
        imageInfo = visualForceImage
    elif debugType == 'VF_EVALUATE_FORMULA_BEGIN':
        textInfo =  splitCurrentLine[1]
        imageInfo = visualForceImage
    elif debugType == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        textInfo =  splitCurrentLine[1]
        imageInfo = visualForceImage
    elif debugType == 'WF_CRITERIA_BEGIN':
        textInfo =  " " + splitCurrentLine[3]
        imageInfo = workflowImage
    elif debugType == 'WF_RULE_EVAL_BEGIN':
        textInfo =  splitCurrentLine[1]
        imageInfo = workflowImage

    return textInfo, imageInfo, currentCodeLine


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

    # Add in tree structure settings to expand to fit frame (resizable)
    treeStructure.column('logLine', stretch=FALSE, width=65)
    treeStructure.heading('logLine', text='Log Line#', anchor='w')
    treeStructure.column('codeLine', stretch=FALSE, width=70)
    treeStructure.heading('codeLine', text='Code Line#', anchor='w')
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
    # Clear the keywords list in case of previous
    keywordsChosen[:] = []
    endingsChosen[:] = []

    # check if a button was selected and use the onvalue to add it to the list of keywords chosen
    for button in checkButtonArray:
        if button.instate(['selected']):
            onvalue = button['onvalue']
            if onvalue in keywordsWithEndings:
                keywordsChosen.append(onvalue)
                endingsChosen.append(keywordsWithEndings[onvalue])
            elif onvalue in neutralKeywords:
                keywordsChosen.append(onvalue)

    return


########################################################################################################################
def processLogFile(logFile):
    # Add the keywords to be looked for
    checkSelectedKeywords()

    # Get the tree ready
    getTreeReady()

    # Variables
    stack = []
    lines = []
    DebugLineNumber = 0

    # Add lines to array as a buffer
    for line in logFile:
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        DebugLineNumber += 1
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            splitLine = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if splitLine[1] in neutralKeywords and splitLine[1] in keywordsChosen:  # Neutral so it can't be a parent and append to stack
                textInfo, imageInfo, codeLineInfo = getInfo(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    treeStructure.insert('', 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    treeStructure.insert(stack[len(stack)-1], 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo))
            elif splitLine[1] in keywordsWithEndings and splitLine[1] in keywordsChosen:  # Check if the name is the beginning of a new hierarchy
                textInfo, imageInfo, codeLineInfo = getInfo(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    stack.append(treeStructure.insert('', 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo)))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    stack.append(treeStructure.insert(stack[len(stack)-1], 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo)))
            elif splitLine[1] in endingsChosen:  # Check if the keyword ends a hierarchy and remove the last branch
                stack.pop()

    logFile.close()  # close the file when everything is done
    resetButton.grid()  # add the reset button onto the side
    root.mainloop()  # Keeps the window looping until a button is pressed to move it to another function


########################################################################################################################
def processPastedLog(log):
    # Add the keywords to be looked for
    checkSelectedKeywords()

    # Get the tree ready
    getTreeReady()

    # Variables
    stack = []  # Holds the branches of the treeview
    lines = []  # holds all the lines of the log file
    DebugLineNumber = 0

    # Determine amount of lines to create a for loop
    numLines = int(log.index('end-1c').split('.')[0])

    # Go through and grab each line and add it to the lines array
    for x in range(1, numLines):
        line = log.get(float(x), float(x+1))
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        DebugLineNumber += 1
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            splitLine = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if splitLine[1] in neutralKeywords and splitLine[1] in keywordsChosen:  # Neutral so it can't be a parent and append to stack
                textInfo, imageInfo, codeLineInfo = getInfo(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    treeStructure.insert('', 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    treeStructure.insert(stack[len(stack)-1], 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo))
            elif splitLine[1] in keywordsWithEndings and splitLine[1] in keywordsChosen:  # Check if the name is the beginning of a new hierarchy
                textInfo, imageInfo, codeLineInfo = getInfo(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    stack.append(treeStructure.insert('', 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo)))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    stack.append(treeStructure.insert(stack[len(stack)-1], 'end', text=textInfo,
                                                      image=imageInfo, values=(DebugLineNumber, codeLineInfo)))
            elif splitLine[1] in endingsChosen:  # Check if the keyword ends a hierarchy and remove the last branch
                stack.pop()

    resetButton.grid()  # add the reset button onto the side
    root.mainloop()  # Keep the window looping until button forces it out to other function


########################################################################################################################
def selectAll():  # Select all the buttons
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.state(['selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def deselectAll():  # Deselect all the buttons
    for button in checkButtonArray:
        button.grid(sticky='w')
        button.state(['!selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def initialMenu():  # The initial menu
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

    root.mainloop()  # Keep the frame looping until a button forces it out


########################################################################################################################
def chooseFile():  # Function for choosing a log file
    # Prompt for the file
    logFile = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')

    # Go back to menu if a file wasn't chosen such as cancel or close
    if logFile is None:
        initialMenu()
    else:
        processLogFile(logFile)

    return


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
    selectButton.grid_remove()
    deselectButton.grid_remove()
    for button in checkButtonArray:
        button.grid_remove()

    # Clear the text box
    logEntry.delete(1.0, END)

    # Add the paste widget
    logYScrolling.grid(row=0, column=1, sticky='nse')
    logEntry.grid(row=0, column=0, sticky="nesw")
    continueButton.grid(row=1, column=0, sticky='nesw')
    resetButton.grid(row=2, column=0)

    root.mainloop()

########################################################################################################################
# Global variables for things that increase and decrease the level of hierarchy currently at
neutralKeywords = ['EXCEPTION_THROWN', 'FATAL_ERROR', 'VALIDATION_RULE']
keywordsWithEndings = {'CALLOUT_REQUEST': 'CALLOUT_RESPONSE', 'CODE_UNIT_STARTED': 'CODE_UNIT_FINISHED',
              'CUMULATIVE_PROFILING_BEGIN': 'CUMULATIVE_PROFILING_END', 'DML_BEGIN': 'DML_END',
                'METHOD_ENTRY': 'METHOD_EXIT', 'SOQL_EXECUTE_BEGIN': 'SOQL_EXECUTE_END',
              'SOSL_EXECUTE_BEGIN': 'SOSL_EXECUTE_END', 'SYSTEM_MODE_ENTER': 'SYSTEM_MODE_EXIT',
              'VF_DESERIALIZE_VIEWSTATE_BEGIN': 'VF_DESERIALIZE_VIEWSTATE_END',
                       'VF_EVALUATE_FORMULA_BEGIN': 'VF_EVALUATE_FORMULA_END',
              'VF_SERIALIZE_VIEWSTATE_BEGIN': 'VF_SERIALIZE_VIEWSTATE_END', 'WF_CRITERIA_BEGIN': 'WF_CRITERIA_END'}

# Translation to a friendlier output for the checkbuttons
keywordTranslations = {'CALLOUT_REQUEST': 'Callout Requests',
              'CODE_UNIT_STARTED': 'Code Units',
              'CONSTRUCTOR_ENTRY': 'Constructors',
              'CUMULATIVE_LIMIT_USAGE': 'Cumulative Limits',
              'CUMULATIVE_PROFILING_BEGIN': 'Cumulative Profilings',
              'DML_BEGIN': 'DML Operations',
                'EXCEPTION_THROWN': 'Exceptions',
              'EXECUTION_STARTED': 'Executions',
                'FATAL_ERROR': 'Fatal Errors',
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
endingsChosen = []
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
for keyword in neutralKeywords:
    newCheckButton = ttk.Checkbutton(root, text=keywordTranslations[keyword], onvalue=keyword, offvalue='off')
    checkButtonArray.append(newCheckButton)
for keyword in keywordsWithEndings:
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
warningImage = PhotoImage(file='warning.gif')

# Create the Treeview
treeStructure = ttk.Treeview(root, selectmode="extended", columns=('logLine', 'codeLine'))

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






