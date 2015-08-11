__author__ = 'oxsc'


def getInfo(infoArray):
    infoArray = infoArray
    debugType = infoArray[1]

    if debugType == 'CALLOUT_REQUEST':
        return infoArray[1]
    elif debugType == 'CODE_UNIT_STARTED':
        return "Code Unit: " + infoArray[len(infoArray)-1]
    elif debugType == 'CONSTRUCTOR_ENTRY':
        return infoArray[1]
    elif debugType == 'CUMULATIVE_LIMIT_USAGE':
        return infoArray[1]
    elif debugType == 'CUMULATIVE_PROFILING_BEGIN':
        return infoArray[1]
    elif debugType == 'DML_BEGIN':
        return "DML: " + infoArray[3][3:] + " " + infoArray[4][5:]
    elif debugType == 'EXECUTION_STARTED':
        return infoArray[1]
    elif debugType == 'METHOD_ENTRY':
        return "Method: " + infoArray[len(infoArray)-1]
    elif debugType == 'SOQL_EXECUTE_BEGIN':
        return "SOQL: " + infoArray[len(infoArray)-1]
    elif debugType == 'SOSL_EXECUTE_BEGIN':
        return infoArray[1]
    elif debugType == 'SYSTEM_CONSTRUCTOR_ENTRY':
        return infoArray[1]
    elif debugType == 'SYSTEM_METHOD_ENTRY':
        return infoArray[1]
    elif debugType == 'SYSTEM_MODE_ENTER':
        return infoArray[1]
    elif debugType == 'VALIDATION_RULE':
        return "Validation Rule: " + infoArray[len(infoArray)-1]
    elif debugType == 'VARIABLE_SCOPE_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_EVALUATE_FORMULA_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        return infoArray[1]
    elif debugType == 'WF_CRITERIA_BEGIN':
        return "Workflow Rule: " + infoArray[3]
    elif debugType == 'WF_RULE_EVAL_BEGIN':
        return infoArray[1]


def convertName(debugType):

    if debugType == 'CALLOUT_REQUEST':
        return 'Callout Requests'
    elif debugType == 'CODE_UNIT_STARTED':
        return 'Code Units'
    elif debugType == 'CONSTRUCTOR_ENTRY':
        return 'Constructors'
    elif debugType == 'CUMULATIVE_LIMIT_USAGE':
        return 'Cumulative Limits'
    elif debugType == 'CUMULATIVE_PROFILING_BEGIN':
        return 'Cumulative Profilings'
    elif debugType == 'DML_BEGIN':
        return 'DML Operations'
    elif debugType == 'EXECUTION_STARTED':
        return 'Executions'
    elif debugType == 'METHOD_ENTRY':
        return 'Methods'
    elif debugType == 'SOQL_EXECUTE_BEGIN':
        return 'SOQL Queries'
    elif debugType == 'SOSL_EXECUTE_BEGIN':
        return 'SOSL Queries'
    elif debugType == 'SYSTEM_CONSTRUCTOR_ENTRY':
        return 'System Constructors'
    elif debugType == 'SYSTEM_METHOD_ENTRY':
        return 'System Methods'
    elif debugType == 'SYSTEM_MODE_ENTER':
        return 'System Modes'
    elif debugType == 'VALIDATION_RULE':
        return 'Validation Rules'
    elif debugType == 'VARIABLE_SCOPE_BEGIN':
        return 'Variable Scopes'
    elif debugType == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        return 'Visualforce Deserialize'
    elif debugType == 'VF_EVALUATE_FORMULA_BEGIN':
        return 'Visualforce Evaluate'
    elif debugType == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        return 'Visualforce Serialize'
    elif debugType == 'WF_CRITERIA_BEGIN':
        return 'Workflow Rules'
    elif debugType == 'WF_RULE_EVAL_BEGIN':
        return 'Workflow Evaluations'
    else:
        return debugType