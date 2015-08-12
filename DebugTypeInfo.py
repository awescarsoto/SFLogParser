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
        return infoArray[3][3:] + " " + infoArray[4][5:]
    elif debugType == 'EXECUTION_STARTED':
        return infoArray[1]
    elif debugType == 'METHOD_ENTRY':
        return "Method: " + infoArray[len(infoArray)-1]
    elif debugType == 'SOQL_EXECUTE_BEGIN':
        return infoArray[len(infoArray)-1]
    elif debugType == 'SOSL_EXECUTE_BEGIN':
        return infoArray[1]
    elif debugType == 'SYSTEM_CONSTRUCTOR_ENTRY':
        return infoArray[1]
    elif debugType == 'SYSTEM_METHOD_ENTRY':
        return infoArray[1]
    elif debugType == 'SYSTEM_MODE_ENTER':
        return infoArray[1]
    elif debugType == 'VALIDATION_RULE':
        return infoArray[len(infoArray)-1]
    elif debugType == 'VARIABLE_SCOPE_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_DESERIALIZE_VIEWSTATE_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_EVALUATE_FORMULA_BEGIN':
        return infoArray[1]
    elif debugType == 'VF_SERIALIZE_VIEWSTATE_BEGIN':
        return infoArray[1]
    elif debugType == 'WF_CRITERIA_BEGIN':
        return infoArray[3]
    elif debugType == 'WF_RULE_EVAL_BEGIN':
        return infoArray[1]
