"""validator logic"""

import re


def is_valid_expression(
    expression: str, rows: dict, missing_data_values: dict, passing_data_values: dict
):
    """is valid expression."""
    pattern = r"\b(?!\d+$)[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*)?\b"

    valid_strings = re.findall(pattern, expression)

    for valid_string in valid_strings:
        if rows.get(valid_string) is None:
            missing_data_values[valid_string] = valid_string
            return False, valid_string

        passing_data_values[valid_string] = valid_string
        expression = expression.replace(
            valid_string, rows.get(valid_string).get("value")
        )

    return True, expression


def validate_expression(expression: str):
    """validate expression."""
    expression = expression.replace("=", "==").replace("<>", "!=").replace("&", " and ")

    if not re.match(r"^[\d\+\-\*/\(\)\.\s<>=!&and]+$", expression):
        return "Invalid expression"

    try:
        result = eval(expression)
    except Exception:
        return "Error evaluating expression"

    return result


def expression_validator(
    value: dict, rows: dict, missing_data_values: dict, passing_data_values: dict
):
    """expression validator."""
    record = []

    record.append(value["validation"])

    print("evaluating", value["validation"])
    is_valid, result = is_valid_expression(
        expression=value["validation"],
        rows=rows,
        missing_data_values=missing_data_values,
        passing_data_values=passing_data_values,
    )

    if not is_valid:
        print(f"id with value {result} not found")
        record.extend([None, f"{result} not found"])
        missing_data_values[result] = result
        return record

    print("expression", result)
    result = validate_expression(expression=result)
    print("validated expression", result)

    if result in ["Invalid expression", "Error evaluating expression"]:
        record.extend(["Fail", result])
        return record

    if result:
        record.extend(["Pass", ""])
        return record

    record.extend(["Fail", value["fail_statement"]])
    return record
