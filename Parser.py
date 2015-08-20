__author__ = 'oxsc'

from Tkinter import *  # Used for ttk and basic GUI
import tkFileDialog  # Used for the file dialog for choosing file
import ttk  # Used for some other GUIs based on Tkinter


########################################################################################################################
def rClicker(e):  # Right-click menu in log entry for copy, cut, paste

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        def rClick_Select(e):
            e.widget.event_generate('<Control-/>')

        e.widget.focus()

        nclst=[
            (' Cut', lambda e=e: rClick_Cut(e)),
            (' Copy', lambda e=e: rClick_Copy(e)),
            (' Paste', lambda e=e: rClick_Paste(e)),
            (' Select All', lambda e=e: rClick_Select(e)),
        ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"


########################################################################################################################
def get_info(log_lines, index):  # Used to return text, image, and code line info based on keyword
    current_line = log_lines[index]  # The line that was currently sent to the function
    split_current_line = current_line.rstrip('\n').split("|")  # Remove the newline character and split it by the pipes
    debug_type = split_current_line[1]  # This is our debug identifier at index 1

    # Defaults to be overwritten
    displayed_text = 'undefined text'
    displayed_image = blank_image
    displayed_code_line = ''

    # Starting to define things specific to keywords
    if debug_type == 'CALLOUT_REQUEST':
        displayed_text = split_current_line[1]
    elif debug_type == 'CODE_UNIT_STARTED':
        displayed_text = "Code Unit: " + split_current_line[len(split_current_line)-1]
    elif debug_type == 'CONSTRUCTOR_ENTRY':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[1]
    elif debug_type == 'CUMULATIVE_LIMIT_USAGE':
        displayed_text = split_current_line[1]
    elif debug_type == 'CUMULATIVE_PROFILING_BEGIN':
        displayed_text = split_current_line[1]
    elif debug_type == 'DML_BEGIN':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[3][3:] + " " + split_current_line[4][5:]
        displayed_image = dml_image
    elif debug_type == 'EXCEPTION_THROWN':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = "Exception: " + split_current_line[3]
        displayed_image = warning_image
    elif debug_type == 'EXECUTION_STARTED':
        displayed_text = split_current_line[1]
    elif debug_type == 'FATAL_ERROR':
        displayed_text = split_current_line[2]
        displayed_image = warning_image
    elif debug_type == 'METHOD_ENTRY':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = "Method: " + split_current_line[len(split_current_line)-1]
    elif debug_type == 'SOQL_EXECUTE_BEGIN':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[len(split_current_line)-1]
        displayed_image = soql_image
    elif debug_type == 'SOSL_EXECUTE_BEGIN':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[1]
        displayed_image = sosl_image
    elif debug_type == 'SYSTEM_CONSTRUCTOR_ENTRY':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[1]
    elif debug_type == 'SYSTEM_METHOD_ENTRY':
        displayed_code_line = split_current_line[2].strip('[]')
        displayed_text = split_current_line[1]
    elif debug_type == 'SYSTEM_MODE_ENTER':
        displayed_text = split_current_line[1]
    elif debug_type == 'USER_DEBUG':
        displayed_text = 'User Debug: ' + split_current_line[4]
    elif debug_type == 'VALIDATION_RULE':
        displayed_text = split_current_line[len(split_current_line)-1]
        for x in range(index, len(log_lines)):  # Look at the next few lines until the validation pass or fail
            current_line = log_lines[x]
            if "VALIDATION_PASS" in current_line:
                displayed_image = pass_image
                break
            if "VALIDATION_FAIL" in current_line:
                displayed_image = fail_image
                break
            if "VALIDATION_ERROR" in current_line:
                displayed_image = fail_image
                break
            else:
                displayed_image = fail_image  # In case something wasn't picked up
    elif debug_type == 'VARIABLE_SCOPE_BEGIN':
        displayed_text = split_current_line[1]
        displayed_code_line = split_current_line[2].strip('[]')
    elif debug_type == 'VF_APEX_CALL':
        displayed_text = 'VF Apex Call' + split_current_line[3].strip('{}')
    elif debug_type == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        displayed_text = split_current_line[1]
        displayed_image = visualforce_image
    elif debug_type == 'VF_EVALUATE_FORMULA_BEGIN':
        displayed_text = split_current_line[1]
        displayed_image = visualforce_image
    elif debug_type == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        displayed_text = split_current_line[1]
        displayed_image = visualforce_image
    elif debug_type == 'WF_CRITERIA_BEGIN':
        displayed_image = workflow_image
        for x in range(index, len(log_lines)):  # Look at the next few lines until the workflow pass or fail
            current_line = log_lines[x]
            if "WF_CRITERIA_END" in current_line:
                if 'false' in current_line:
                    displayed_text = ' Criteria Not Met: ' + split_current_line[3]
                if 'true' in current_line:
                    displayed_text = ' Criteria Met: ' + split_current_line[3]
    elif debug_type == 'WF_RULE_EVAL_BEGIN':
        displayed_text = split_current_line[1]
        displayed_image = workflow_image

    return displayed_text, displayed_image, displayed_code_line


########################################################################################################################
def get_tree_ready():  # Sets up the treeview structure
    # Clear the tree
    tree_structure.delete(*tree_structure.get_children())

    # Remove other widgets from view
    file_button.grid_remove()
    paste_button.grid_remove()
    reset_button.grid_remove()
    select_button.grid_remove()
    deselect_button.grid_remove()
    log_entry.grid_remove()
    continue_button.grid_remove()
    logYScrolling.grid_remove()
    for button in checkbutton_array:
        button.grid_remove()

    # Add in tree structure settings to expand to fit frame (resizable)
    tree_structure.column('logLine', stretch=FALSE, width=65)
    tree_structure.heading('logLine', text='Log Line#', anchor='w')
    tree_structure.column('codeLine', stretch=FALSE, width=70)
    tree_structure.heading('codeLine', text='Code Line#', anchor='w')
    tree_structure.grid(row=0, column=0, sticky='nsew')
    tree_structure.columnconfigure(0, weight=1)
    treeYScrolling.grid(row=0, column=1, sticky='nse')
    treeXScrolling.grid(row=1, column=0, sticky='sew')
    tree_structure.grid(sticky="nesw")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    tree_structure.columnconfigure(0, weight=1)
    tree_structure.rowconfigure(0, weight=1)

    return


########################################################################################################################
def check_selected_keywords():  # Used to check what checkboxes were chosen
    # Clear the keywords list in case of previous
    keywords_chosen[:] = []
    endings_chosen[:] = []

    # check if a button was selected and use the onvalue to add it to the list of keywords chosen
    for button in checkbutton_array:
        if button.instate(['selected']):
            onvalue = button['onvalue']
            if onvalue in keywords_with_endings:
                keywords_chosen.append(onvalue)
                endings_chosen.append(keywords_with_endings[onvalue])
            elif onvalue in neutral_keywords:
                keywords_chosen.append(onvalue)

    return


########################################################################################################################
def process_log_file(log_file):  # Used to process log files and closes the file.
    # Add the keywords to be looked for
    check_selected_keywords()

    # Get the tree ready
    get_tree_ready()

    # Variables
    stack = []
    lines = []
    debug_line_number = 0

    # Add lines to array as a buffer
    for line in log_file:
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        debug_line_number += 1
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            split_line = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if split_line[1] in neutral_keywords and split_line[1] in keywords_chosen:  # Neutral so it can't be a parent and append to stack
                text_info, image_info, code_line_info = get_info(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    tree_structure.insert('', 'end', text=text_info,
                                          image=image_info, values=(debug_line_number, code_line_info))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    tree_structure.insert(stack[len(stack)-1], 'end', text=text_info,
                                          image=image_info, values=(debug_line_number, code_line_info))
            elif split_line[1] in keywords_with_endings and split_line[1] in keywords_chosen:  # Check if the name is the beginning of a new hierarchy
                text_info, image_info, code_line_info = get_info(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    stack.append(tree_structure.insert('', 'end', text=text_info,
                                                       image=image_info, values=(debug_line_number, code_line_info)))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    stack.append(tree_structure.insert(stack[len(stack)-1], 'end', text=text_info,
                                                       image=image_info, values=(debug_line_number, code_line_info)))
            elif split_line[1] in endings_chosen:  # Check if the keyword ends a hierarchy and remove the last branch
                stack.pop()

    log_file.close()  # close the file when everything is done
    reset_button.grid()  # add the reset button onto the side
    root.mainloop()  # Keeps the window looping until a button is pressed to move it to another function


########################################################################################################################
def process_pasted_log(log):  # Used to process pasted logs. Only difference is that no file is closed.
    # Add the keywords to be looked for
    check_selected_keywords()

    # Get the tree ready
    get_tree_ready()

    # Variables
    stack = []  # Holds the branches of the treeview
    lines = []  # holds all the lines of the log file
    debug_line_number = 0

    # Determine amount of lines to create a for loop
    num_lines = int(log.index('end-1c').split('.')[0])

    # Go through and grab each line and add it to the lines array
    for x in range(1, num_lines):
        line = log.get(float(x), float(x+1))
        lines.append(line)

    for x in range(0, len(lines)):   # Iterate over the rest of lines in the file
        debug_line_number += 1
        if "|" in lines[x]:  # Separate lines by the pipe and remove newline characters
            split_line = lines[x].rstrip('\n').split("|")  # Split into array by pipes
            if split_line[1] in neutral_keywords and split_line[1] in keywords_chosen:  # Neutral so it can't be a parent and append to stack
                text_info, image_info, code_line_info = get_info(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    tree_structure.insert('', 'end', text=text_info,
                                          image=image_info, values=(debug_line_number, code_line_info))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    tree_structure.insert(stack[len(stack)-1], 'end', text=text_info,
                                          image=image_info, values=(debug_line_number, code_line_info))
            elif split_line[1] in keywords_with_endings and split_line[1] in keywords_chosen:  # Check if the name is the beginning of a new hierarchy
                text_info, image_info, code_line_info = get_info(lines, x)
                if len(stack) == 0:  # Insert a new branch to the root of the tree and add that to our list of branches
                    stack.append(tree_structure.insert('', 'end', text=text_info,
                                                       image=image_info, values=(debug_line_number, code_line_info)))
                else:  # Insert a new branch under the last branch and add it to our known list of branches
                    stack.append(tree_structure.insert(stack[len(stack)-1], 'end', text=text_info,
                                                       image=image_info, values=(debug_line_number, code_line_info)))
            elif split_line[1] in endings_chosen:  # Check if the keyword ends a hierarchy and remove the last branch
                stack.pop()

    reset_button.grid()  # add the reset button onto the side
    root.mainloop()  # Keep the window looping until button forces it out to other function


########################################################################################################################
def select_all():  # Select all the checkbuttons
    for button in checkbutton_array:
        button.grid(sticky='w')
        button.state(['selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def deselect_all():  # Deselect all the checkbuttons
    for button in checkbutton_array:
        button.grid(sticky='w')
        button.state(['!selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()
    return


########################################################################################################################
def initial_menu():  # The initial menu
    # Remove other widgets
    tree_structure.grid_remove()
    treeXScrolling.grid_remove()
    treeYScrolling.grid_remove()
    logYScrolling.grid_remove()
    log_entry.grid_remove()
    continue_button.grid_remove()
    root.columnconfigure(0, weight=0)
    root.rowconfigure(0, weight=0)

    # Put initial widgets on the frame
    file_button.grid(row=0, column=0, sticky='nesw')
    paste_button.grid(row=0, column=1, sticky='nesw')
    reset_button.grid(row=0, column=2, sticky='nesw')
    select_button.grid(row=1, column=0, sticky='nesw')
    deselect_button.grid(row=1, column=1, sticky='nesw')

    # Put checkbuttons on the frame and set default values for buttons as checkmarked
    for button in checkbutton_array:
        button.grid(sticky='w')
        button.state(['selected'])  # Sets the internal state as having been selected
        button.invoke()  # invoked twice to make the checkmarks appear correctly
        button.invoke()

    root.mainloop()  # Keep the frame looping until a button forces it out


########################################################################################################################
def choose_file():  # Function for choosing a log file
    # Prompt for the file
    log_file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')

    # Go back to menu if a file wasn't chosen such as cancel or close
    if log_file is None:
        initial_menu()
    else:
        process_log_file(log_file)

    return


########################################################################################################################
def paste_log():  # Used for the pasting of the log file.
    # Remove other widgets
    tree_structure.grid_remove()
    treeXScrolling.grid_remove()
    treeYScrolling.grid_remove()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    file_button.grid_remove()
    paste_button.grid_remove()
    reset_button.grid_remove()
    select_button.grid_remove()
    deselect_button.grid_remove()
    for button in checkbutton_array:
        button.grid_remove()

    # Clear the text box
    log_entry.delete(1.0, END)

    # Add the paste widget
    logYScrolling.grid(row=0, column=1, sticky='nse')
    log_entry.grid(row=0, column=0, sticky="nesw")
    continue_button.grid(row=1, column=0, sticky='nesw')
    reset_button.grid(row=2, column=0)

    root.mainloop()  # Keep the frame looping until a button forces it out

########################################################################################################################
''' This is the main function that gets started and calls the initial menu after setting up.'''

# Keywords that have no specific ending keyword
neutral_keywords = ['EXCEPTION_THROWN', 'FATAL_ERROR', 'VALIDATION_RULE', 'USER_DEBUG', 'VF_APEX_CALL']

# Keywords that have a close
keywords_with_endings = {'CALLOUT_REQUEST': 'CALLOUT_RESPONSE', 'CODE_UNIT_STARTED': 'CODE_UNIT_FINISHED',
                         'CUMULATIVE_PROFILING_BEGIN': 'CUMULATIVE_PROFILING_END', 'DML_BEGIN': 'DML_END',
                         'METHOD_ENTRY': 'METHOD_EXIT', 'SOQL_EXECUTE_BEGIN': 'SOQL_EXECUTE_END',
                         'SOSL_EXECUTE_BEGIN': 'SOSL_EXECUTE_END', 'SYSTEM_MODE_ENTER': 'SYSTEM_MODE_EXIT',
                         'VF_DESERIALIZE_VIEWSTATE_BEGIN': 'VF_DESERIALIZE_VIEWSTATE_END',
                         'VF_EVALUATE_FORMULA_BEGIN': 'VF_EVALUATE_FORMULA_END',
                         'VF_SERIALIZE_VIEWSTATE_BEGIN': 'VF_SERIALIZE_VIEWSTATE_END',
                         'WF_CRITERIA_BEGIN': 'WF_CRITERIA_END'}

# Translation to a friendlier output for the checkbuttons
keyword_translations = {'CALLOUT_REQUEST': 'Callout Requests',
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
                        'USER_DEBUG': 'User Debugging',
                        'VARIABLE_SCOPE_BEGIN': 'Variable Scopes',
                        'VALIDATION_RULE': 'Validation Rules',
                        'VF_APEX_CALL': 'Visualforce Apex Calls',
                        'VF_DESERIALIZE_VIEWSTATE_BEGIN': 'Visualforce Deserialize',
                        'VF_EVALUATE_FORMULA_BEGIN': 'Visualforce Evaluate',
                        'VF_SERIALIZE_VIEWSTATE_BEGIN': 'Visualforce Serialize',
                        'WF_CRITERIA_BEGIN': 'Workflow Rules',
                        'WF_RULE_EVAL_BEGIN': 'Workflow Evaluations'}

keywords_chosen = []  # empty list to hold keywords that will be selected
endings_chosen = []  # empty list to hold the ending keywords of the selected
checkbutton_array = []  # empty list to hold checkbuttons that will be created


# Initiate the window
root = Tk()
root.title("Salesforce Debug Methods Tree")
root.geometry("800x600")

# Create buttons
file_button = ttk.Button(root, text="Choose File", command=lambda: choose_file())
paste_button = ttk.Button(root, text="Paste Log", command=lambda: paste_log())
reset_button = ttk.Button(root, text="Reset", command=lambda: initial_menu())
continue_button = ttk.Button(root, text="Continue", command=lambda: process_pasted_log(log_entry))
select_button = ttk.Button(root, text="Select All", command=lambda: select_all())
deselect_button = ttk.Button(root, text="Deselect All", command=lambda: deselect_all())

# Create checkbuttons automatically
for keyword in neutral_keywords:
    new_checkbutton = ttk.Checkbutton(root, text=keyword_translations[keyword], onvalue=keyword, offvalue='off')
    checkbutton_array.append(new_checkbutton)
for keyword in keywords_with_endings:
    new_checkbutton = ttk.Checkbutton(root, text=keyword_translations[keyword], onvalue=keyword, offvalue='off')
    checkbutton_array.append(new_checkbutton)

# Create the images
blank_image = PhotoImage(file='blank.gif')
workflow_image = PhotoImage(file='gear_happy2.gif')
validation_rule_image = PhotoImage(file='VR.gif')
visualforce_image = PhotoImage(file='VF.gif')
dml_image = PhotoImage(file='DML.gif')
sosl_image = PhotoImage(file='SOSL.gif')
soql_image = PhotoImage(file='SOQL.gif')
pass_image = PhotoImage(file='pass.gif')
fail_image = PhotoImage(file='fail.gif')
warning_image = PhotoImage(file='warning.gif')

# Create the Treeview
tree_structure = ttk.Treeview(root, selectmode="extended", columns=('logLine', 'codeLine'))

# Create scrollbars to be added to tree structure later
treeYScrolling = ttk.Scrollbar(root, orient='vertical', command=tree_structure.yview)
treeXScrolling = ttk.Scrollbar(root, orient='horizontal', command=tree_structure.xview)
tree_structure.configure(yscroll=treeYScrolling.set, xscroll=treeXScrolling.set)

# Create place to paste logs
log_entry = Text(root)
log_entry.bind('<Button-3>',rClicker, add='')
logYScrolling = ttk.Scrollbar(root, orient='vertical', command=log_entry.yview)
log_entry.configure(yscroll=logYScrolling.set)

# Startup
initial_menu()
root.mainloop()






