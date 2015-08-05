__author__ = 'oxsc'

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
ImportantInfo = {'CALLOUT_REQUEST': 1, 'CODE_UNIT_STARTED': 1, 'CONSTRUCTOR_ENTRY': 1, 'CUMULATIVE_LIMIT_USAGE': 1,
                 'CUMULATIVE_PROFILING_BEGIN': 1, 'DML_BEGIN': 1, 'EXECUTION_STARTED': 1, 'METHOD_ENTRY': 1,
                 'SOQL_EXECUTE_BEGIN': 1, 'SOSL_EXECUTE_BEGIN': 1, 'SYSTEM_CONSTRUCTOR_ENTRY': 1,
                 'SYSTEM_METHOD_ENTRY': 1, 'SYSTEM_MODE_ENTER': 1,'VARIABLE_SCOPE_BEGIN': 1,
                 'VF_DESERIALIZE_VIEWSTATE_BEGIN': 1, 'VF_EVALUATE_FORMULA_BEGIN': 1,
                 'VF_SERIALIZE_VIEWSTATE_BEGIN': 1, 'WF_CRITERIA_BEGIN': 1, 'WF_RULE_EVAL_BEGIN': 1}

currLevel = 0

# Iterate over the lines in the file
for line in f:

    # Separate lines by the pipe and remove newline characters
    if "|" in line:
        line = line.rstrip('\n')
        splitLine = line.split("|")
        if splitLine[1] in increasers:
            currLevel += 1
            print (currLevel * '\t') + splitLine[ImportantInfo[splitLine[1]]]
        elif splitLine[1] in decreasers:
            currLevel -= 1


f.close()
