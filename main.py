import string, ast
import operator
import re
# Supported operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg,
}

def split(text):
    # Remove comments and join the text
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "#" in line:
            lines[i] = line.split("#")[0]
    text = "".join(lines)

    res = []
    a = ""
    type_ = "str"
    layer = 0
    openm = "([{"
    closem = ")]}"
    escape = False
    in_string = False
    string_char = ""

    for i in text:
        if escape:
            a += "\\" + i  # Add the escaped character with backslash
            escape = False
            continue

        if i == "\\":
            escape = True  # Next character is escaped
            continue

        if layer == 0:  # We're not inside a container
            if in_string:
                a += i  # Add characters to the string until it closes
                if i == string_char:  # Closing quote matches the opening quote
                    res.append(a)  # End of the string, add the full quoted string
                    a = ""
                    in_string = False
                continue

            if i in "'\"":  # Start of a string
                if layer == 0:  # Only start a string if not inside a container
                    if a:
                        res.append(a)  # Add whatever is before the string (if any)
                    a = i  # Start collecting the string, including the opening quote
                    in_string = True
                    string_char = i
            if i in openm:  # Start of a container (parentheses, brackets, braces)
                if a:
                    res.append(a)  # Add the previous token before the container
                a = i
                layer += 1
            elif i in string.ascii_letters + string.digits:  # Handle alphanumeric (strings)
                if type_ == "str":
                    a += i
                else:
                    if a:
                        res.append(a)
                    a = i
                    type_ = "str"
            elif i in r"""!#$%&()*+,-./:;<=>?@[\]^_`{|}~""" and i not in openm:  # Handle punctuation
                if type_ == "punc":
                    a += i
                else:
                    if a:
                        res.append(a)
                    a = i
                    type_ = "punc"
            elif i == " ":  # Handle spaces (reset current token)
                if a:
                    res.append(a)
                a = ""
            elif i in closem:  # Handle closing a container (shouldn't happen at layer 0)
                raise ValueError(f"Unexpected closing delimiter '{i}'")
        else:  # We are inside a container
            a += i
            if i in openm:  # Nested container
                layer += 1
            elif i in closem:  # Closing a container
                layer -= 1
                if layer == 0:  # Closed the container
                    res.append(a)
                    a = ""
                    type_ = "str"

    if a:
        res.append(a)

    # Remove empty strings from the result
    res = [x for x in res if x]

    return res


def toParams(val: str):
    val = val[1:-1].split(",")
    res = {}
    for i in val:
        i = i.strip()
        if "=" not in i:
            res[i] = ("required", "")
        else:
            i = i.split("=")
            res[i[0]] = ("optional", i[1])
    return res
def eval_function(function_name: str, args: dict, functions: dict, vars: dict):
    # Assuming eval_vars processes args and vars
    args = eval_vars(functions, args, vars)
    func_data = functions[function_name]
    req = func_data[0]  # Function arguments
    func_code = func_data[1][1:-1].strip()  # Function body

    # Assuming merge_dict_with_list merges the function signature with args
    merged_vars = merge_dict_with_list(req, args, vars)
    merged_vars.update(vars)  # Ensure merged vars include all current vars

    # Assuming run executes the function code and updates vars
    returnval, functions, vars = run(func_code, functions, merged_vars)
    return returnval, functions, vars

def detect_and_replace_functions(functions: dict, code: str, vars: dict):
    # Regex to match function calls
    pattern = re.compile(r'(\w+)\s*\(([^)]*)\)')

    def replace_function(match):
        func_name = match.group(1)
        args_str = match.group(2).strip()
        args_list = [arg.strip() for arg in args_str.split(',')] if args_str else []

        if func_name in functions:
            func_signature = functions[func_name][0]  # Argument dictionary
            required_args = list(func_signature.keys())

            # Ensure the number of arguments provided matches the function signature
            if len(args_list) == len(required_args):
                args = dict(zip(required_args, args_list))  # Map argument names to values

                # Call eval_function to get the return value of the function
                returnval, functions, vars = eval_function(func_name, args, functions, vars)
                return str(returnval)  # Replace function call with its return value
            else:
                raise ValueError(f"Error: Function {func_name} requires {len(required_args)} arguments, but {len(args_list)} were provided.")
        else:
            raise ValueError(f"Error: Function {func_name} not found.")

    # Replace all function calls with their evaluated values
    code_with_replaced_functions = pattern.sub(replace_function, code)
    
    return code_with_replaced_functions, functions, vars

def parseExpr(functions: dict, code: str, vars: dict):
    for var in vars:
        # Using \b for word boundaries to match whole words only
        code = re.sub(rf'\b{re.escape(var)}\b', str(vars[var]), code)
    code, functions, vars = detect_and_replace_functions(functions, code, vars)
    return code

def eval_vars(functions: dict, stmt: str, vars: dict):
    stmt, functions, vars = parseExpr(functions, stmt, vars)
    stmt, functions, vars = parseExpr(functions, stmt, vars)
    try:
        return eval(stmt)
    except:
        return str(stmt)

def wrap_strings_recursively(data):
    if isinstance(data, str):
        # Check if the data is a string and wrap it with double quotes
        return f'"{data}"'
    elif isinstance(data, list):
        # Recursively process each item in the list
        return [wrap_strings_recursively(item) for item in data]
    else:
        # If it's neither a string nor a list, return it as is
        return data

def merge_dict_with_list(struct, values, vars):
    # Prepare the output dictionary
    result = {}
    
    # Extract required fields
    required_fields = [key for key, (status, _) in struct.items() if status == "required"]

    # Check if there are enough values for required fields
    if len(values) < len(required_fields):
        raise ValueError("Error: Not enough args for required fields")
    if values == "(,)":
        values = ()
    # Iterate through the struct and merge with values
    index = 0
    for key, (status, default_value) in struct.items():
        if status == "required":
            if len(values) >= index + 1:
                result[key] = values[index]
            else:
                print("Error: Not enough args")
                raise ValueError
        else:
            if len(values) < index + 1:
                result[key] = default_value
            else:
                result[key] = values[index]
        index += 1
    return result

def run(code: str, functions: dict={}, vars: dict={}):
    def find_until(tokens, index, end_token):
        result = []
        while index < len(tokens) and tokens[index] != end_token:
            result.append(tokens[index])
            index += 1
        return result, index

    # Remove the outermost curly braces and split the code
    code = code.strip("{}")
    returnval = None
    code = split(code)
    index = 0
    while index < len(code):
        if code[index] == "func":
            index += 1
            func_name = code[index]
            index += 1
            params = toParams(code[index])
            index += 1
            func_body = code[index]
            functions[func_name] = (params, func_body)
        elif code[index] == "if":
            index += 1
            conditions = code[index]
            conditions.replace("||", " or ")
            conditions.replace("&&", " and ")
            conditions.replace("!", " not ")  
            condtitions = eval_vars(functions, conditions, vars)
            index += 1
            if condtitions:
                returnval_, functions, vars = run(code[index][1:-1], functions, vars)
            index += 1
        elif code[index] == "while":
            index += 1
            conditions = code[index]
            conditions.replace("||", " or ")
            conditions.replace("&&", " and ")
            conditions.replace("!", " not ")  
            index += 1
            condtitions = eval_vars(functions, conditions, vars)
            while condtitions:
                returnval_, functions, vars = run(code[index][1:-1], functions, vars)
                condtitions = eval_vars(functions, conditions, vars)
            index += 1
        elif code[index] == "python":
            index += 1
            expr, index = find_until(code, index, ";")
            #print(parseExpr(functions, expr[0][1:-1], wrap_strings_recursively(vars)))
            exec(parseExpr({}, expr[0][1:-1], wrap_strings_recursively(vars))[1:-1])
        elif code[index] == "var":
            index += 1
            var_name = code[index]
            index += 2  # Skip over "="
            expr, index = find_until(code, index, ";")
            vars[var_name] = eval_vars(functions, " ".join(expr), vars)
        elif code[index] in vars:
            var_name = code[index]
            index += 1
            op = code[index]
            index += 1
            expr, index = find_until(code, index, ";")
            expr = eval_vars(functions, " ".join(expr), vars)
            
            if op == "+=":
                vars[var_name] += expr
            elif op == "-=":
                vars[var_name] -= expr
            elif op == "*=":
                vars[var_name] *= expr
            elif op == "/=":
                vars[var_name] /= expr
            elif op == "//=":
                vars[var_name] //= expr
            elif op == "**=":
                vars[var_name] **= expr
            elif op == "%=":
                vars[var_name] %= expr
            elif op == "&=":
                vars[var_name] &= expr
            elif op == "|=":
                vars[var_name] |= expr
            elif op == "^=":
                vars[var_name] ^= expr
            elif op == ">>=":
                vars[var_name] >>= expr
            elif op == "<<=":
                vars[var_name] <<= expr
            elif op == "=":
                vars[var_name] = expr
        elif code[index] in functions:
            func_name = code[index]
            index += 1
            args, index = find_until(code, index, ")")
            args = args[0]  # remove the last empty element due to split by comma
            args = args[:-1] + ",)"
            args = eval_vars(functions, args, vars)
            funcdata = functions[func_name]
            req = funcdata[0]
            func_code = funcdata[1][1:-1].strip("{")
            meet = merge_dict_with_list(req, args, vars)
            meet.update(vars)
            returnval_, functions, vars = run(func_code, functions, meet)
        elif code[index] == "return":
            index += 1
            expr, index = find_until(code, index, ";")
            return eval_vars(functions, " ".join(expr), vars), functions, vars

        index += 1
    return returnval, functions, vars

run("""
func a() {
    var d = 1;
    return d;
}
var b = a();
python("print(\"b\")");
""")
