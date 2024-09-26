import string
import re
import traceback

def custom_trace(e: Exception):
    # Extract the traceback details
    tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
    
    # Format the trace in a custom manner, similar to the example
    trace_output = []
    for line in tb_lines:
        if "File" in line:
            # Extract the file path, line number, and code causing the issue
            trace_output.append(line.strip())
        else:
            # Append the rest of the traceback (error message etc.)
            trace_output.append(line.strip())
    
    # Join the trace lines together for output
    return "\n".join(trace_output)


debug_ = 0
def debug(*args):
    if debug_:
        print(*args)
# Supported operations
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
def find_for(string, search):
    index = 0
    while string[index:index+len(search)] != search and index + len(search) < len(string) + 1:
        index += 1
    if string[index:index+len(search)] != search:
        return -1
    else:
        return index
def run_function(functions, function_name, args: str, vars):
    func_name = function_name
    #print(args)
    args = args[1:-1]
    args += ","
    args = "(" + args + ")"
    args = eval_vars(functions, args, vars)  # Evaluate the arguments
    #print(args)
    funcdata = functions[func_name]
    req = funcdata[0]
    func_code = funcdata[1]
    merged_vars = merge_dict_with_list(req, args)
    merged_vars.update(vars)
    returnval, a, b = run(func_code, functions, merged_vars)
    del merged_vars
    return returnval  # Fix to pass the merged variables
def detect_and_replace_functions(functions: dict, code: str, vars: dict):
    debug("code3", code)
    code = split(code)
    index = 0
    replace = ""
    while index < len(code):
        if code[index][0] in "[({":
            a = detect_and_replace_functions_args(functions, code[index], vars)
            code[index] = a
        elif code[index] in vars:
            index += 1
            if code[index][0] == "[":
                range_ = code[index]
                range__ = range_[1:-1].split(":")
                for i, j in enumerate(range_):
                    range__[i] = int(eval_vars(functions, range_[i], vars))
                value = eval_vars(functions, code[index - 1], vars)
                if len(range__) == 1:
                    value = value[range__[0]]
                elif len(range__) == 2:
                    value = value[range__[0]:range__[1]]
                elif len(range__) == 3:
                    value = value[range__[0]:range__[1]:range__[2]]
                code = "".join(code)
                code = code.replace(code[index - 1] + range_, str(value))
            else:
                index -= 1
        elif code[index] in functions:
            func_name = code[index]
            index += 1
            args = code[index]
            replace = func_name + args
            value = run_function(functions, func_name, args, vars)
            code = "".join(code)
            debug("replace", replace)
            debug("replace2", str(value))
            code = code.replace(replace, str(value))
            debug("replace3", code)
            code = split(code)
        elif code[index] == "evalp":
            index += 1
            args = code[index]
            replace = "evalp" + args
            #print(args)
            value = eval(args[1:-1])
            if type(value) == str:
                value = f"str(\'{value}\')"
            code = "".join(code).replace(replace, str(value))
            code = split(code)
            index += 1
        index += 1
    if isinstance(code, list):
        code = "".join(code)
    debug("code4", code)
    return code
def detect_and_replace_functions_args(functions, args, vars):
    a = ""
    if args.startswith("("):
        a = "(" + detect_and_replace_functions(functions, args[1:-1], vars) + ")"
    if args.startswith("["):
        a = "[" + detect_and_replace_functions(functions, args[1:-1], vars) + "]"
    if args.startswith("{"):
        a = "{" + detect_and_replace_functions(functions, args[1:-1], vars) + "}"
    #print(a)
    return a
def parseExpr(functions: dict, code: str, vars: dict):
    #raise Exception()
    #debug("a" + code)
    for var in vars:
        # Using \b for word boundaries to match whole words only
        code = re.sub(rf'\b{re.escape(var)}\b', str(vars[var]), code)
    code = detect_and_replace_functions(functions, code, vars)
    return code

def eval_vars(functions: dict, stmt: str, vars: dict):
    stmt = parseExpr(functions, stmt, vars)
    debug(stmt)
    return eval(stmt)


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

def merge_dict_with_list(struct, values):
    # Prepare the output dictionary
    result = {}
    
    # Extract required fields
    required_fields = [key for key, (status, _) in struct.items() if status == "required"]

    # Check if there are enough values for required fields
    if len(values) < len(required_fields):
        raise ValueError("Error: Not enough args for required fields")

    # Iterate through the struct and merge with values
    index = 0
    for key, (status, default_value) in struct.items():
        if status == "required":
            if len(values) >= index + 1:
                result[key] = values[index]
            else:
                debug("Error: Not enough args")
                raise ValueError
        else:
            if len(values) < index + 1:
                result[key] = default_value
            else:
                result[key] = values[index]
        index += 1
    return result

def find_until(tokens, index, end_token):
    result = []
    while index < len(tokens) and tokens[index] != end_token:
        result.append(tokens[index])
        index += 1
    return result, index
def run(code: str, functions: dict={}, vars: dict={}):
    # Remove the outermost curly braces and split the code
    code = code.strip("{}")
    returnval = None
    code = split(code)
    index = 0
    condeval = False
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
            conditions = conditions.replace("||", " or ")
            conditions = conditions.replace("&&", " and ")
            conditions = conditions.replace("!", " not ") 
            conditions = eval_vars(functions, conditions, vars)
            condeval = conditions
            index += 1
            if conditions:
                if "return" in code[index][1:-1]:
                    returnval, functions_, vars = run(code[index][1:-1], functions, vars)
                else:
                    returnval_, functions_, vars = run(code[index][1:-1], functions, vars)
            #index += 1
        elif code[index] == "else":
            index += 1
            if not condeval:
                if "return" in code[index][1:-1]:
                    returnval, functions_, vars = run(code[index][1:-1], functions, vars)
                else:
                    returnval_, functions_, vars = run(code[index][1:-1], functions, vars)
        elif code[index] == "while":
            index += 1
            conditions = code[index]
            conditions.replace("||", " or ")
            conditions.replace("&&", " and ")
            conditions.replace("!", " not ")  
            index += 1
            condtitions = eval_vars(functions, conditions, vars)
            while condtitions:
                returnval, functions_, vars = run(code[index][1:-1], functions, vars)
                condtitions = eval_vars(functions, conditions, vars)
            index += 1
        elif code[index] == "using":
            index += 1
            data = ""
            filepath = code[index]
            filepath = filepath[1:-1]
            with open(filepath) as file:
                data = file.read()
            _, functions1, vars1 = run(data)
            functions.update(functions1)
            vars.update(vars1)
            index += 1
        elif code[index] == "execp":
            index += 1
            expr, index = find_until(code, index, ";")
            expr = parseExpr(functions, expr[0], wrap_strings_recursively(vars))[1:-1]  # Fix parsing and execution
            #print(expr)
            debug(expr[1:-1])
            #print(expr[1:-1])
            exec(expr)
        elif code[index] == "var":
            index += 1
            var_name = code[index]
            index += 2  # Skip over "="
            expr, index = find_until(code, index, ";")
            a = eval_vars(functions, "".join(expr), vars)
            debug("var", a, type(a))
            vars[var_name] = a
        elif code[index] in vars:
            var_name = code[index]
            index += 1
            op = code[index]
            index += 1
            expr, index = find_until(code, index, ";")
            vars.update({"this": vars[var_name]})
            #print(expr)
            expr = eval_vars(functions, "".join(expr), vars)
            
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
            #print(code[index], code[index + 1], vars)
            run_function(functions, code[index], code[index + 1], vars)
        elif code[index] == "return":
            index += 1
            expr, index = find_until(code, index, ";")
            return eval_vars(functions, "".join(expr), vars), functions, vars
        elif code[index] == "for":
            index += 1
            con = code[index]
            con = con[1:-1].strip().split(",")
            mvar = con[0]
            iterable = con[1]
            iterable = eval_vars(functions, iterable, vars)
            index += 1
            for i in iterable:
                update_vars = vars
                update_vars.update({mvar: i})
                r, functions, vars = run(code[index], functions, vars)
                vars.pop(mvar, "")    
            index += 1
        elif code[index] == "try":
            varsnapshot = vars
            functionsnapshot = functions
            index += 1
            ex = 0
            try:
                returnval_, functions, vars = run(code[index][1:-1], functions, vars)
            except:
                ex = 1
                vars = varsnapshot
                functions = functionsnapshot
                index += 2
                returnval_, functions, vars = run(code[index][1:-1], functions, vars)
            index += 1
            if ex == 0:
                index += 1
        debug(vars)
        index += 1
    #print(vars)
    return returnval, functions, vars
def main(content):
    run(content)
#print(eval_vars({'print': ({'a': ('required', '')}, '{    execp("print("a")");}'), 'input': ({'c': ('required', '')}, '{    var d = evalp("input(\\"c\\")");    return d;}'), 'pow': ({'a': ('required', ''), 'b': ('required', '')}, '{    var c = a ** b;    return c;}'), 'mod': ({'a': ('required', ''), 'b': ('required', '')}, '{    var c = a % b;    return c;}'), 'abs': ({'n': ('required', '')}, '{    if (n >= 0) {        return n;    }    if (n < 0) {        n -= n;        n -= n;        return n;    }}'), 'sqrt': ({'n': ('required', '')}, '{    return pow(n, 0.5);}'), 'min': ({'a': ('required', ''), 'b': ('required', '')}, '{    if (a < b) {        return a;    }    return b;}'), 'max': ({'a': ('required', ''), 'b': ('required', '')}, '{    if (a < b) {        return b;    }    return a;}'), 'floor': ({'n': ('required', '')}, '{    if (mod(n, 1) == 0) {        return n;    }    return n - mod(n, 1);}'), 'ceil': ({'n': ('required', '')}, '{    if (mod(n, 1) == 0) {        return n;    }    return n + 1 - mod(n, 1);}'), 'round': ({'n': ('required', '')}, '{    var decimalPart = mod(n, 1);    if (decimalPart >= 0.5) {        return ceil(n);    }    return floor(n);}'), 'sign': ({'n': ('required', '')}, '{    if (n > 0) {        return 1;    }    if (n < 0) {        return -1;    }    return 0;}'), 'exp': ({'n': ('required', '')}, '{    return pow(E, n);}'), 'log': ({'n': ('required', '')}, '{    var result = 0;    var approx = n - 1;    while (approx > 0) {        approx = approx / E;        result += 1;    }    return result;}'), 'fact': ({'n': ('required', '')}, '{    if (n == 0) {        return 1;    }    if (n > 0) {        var b = fact(n - 1);        b *= n;        return b;    }}'), 'gcd': ({'a': ('required', ''), 'b': ('required', '')}, '{    while (b != 0) {        var temp = b;        b = mod(a, b);        a = temp;    }    return a;'), 'g': ({'a': ('required', ''), 'b': ('required', '')}, '{    if (a < b) {        return "1";    }    return "2";}')}, "(a < b)", {"a": 1, "b": 2}))

main(r"""using "modules/test.ks";
using "modules/io.ks";
var b = input("h");""")