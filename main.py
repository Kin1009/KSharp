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
                a += i  # Add characters to the f until it closes
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
            elif i in string.ascii_letters + string.digits + "_:.":  # Handle alphanumeric (strings)
                if type_ == "str":
                    a += i
                else:
                    if a:
                        res.append(a)
                    a = i
                    type_ = "str"
            elif i in r"""!#$%&()*+,-/;<=>?@[\]^`{|}~""" and i not in openm:  # Handle punctuation
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
def splitline(text):
    # Remove comments and join the text
    a = split(text)
    idx = 0
    c = 0
    b = 0
    res = {}
    for i in a:
        if i == ";":
            res.update({c: list(range(idx, idx+b))}) # type: ignore
            idx += b
            b = 0
            c += 1
        elif i.endswith("}"):
            res.update({c: list(range(idx, idx+b))}) # type: ignore
            idx += b
            b = 0
            c += 1
        else:
            b += 1
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
    if args != "": 
        args += ","
    args = "(" + args + ")"
    args = eval_vars(functions, args, vars)  # Evaluate the arguments
    #print(args)
    funcdata = functions[func_name]
    req = funcdata[0]
    func_code = funcdata[1]
    merged_vars = merge_dict_with_list(req, args)
    merged_vars.update(vars)
    returnval, a, b, returned = run(func_code, functions, merged_vars)
    del merged_vars
    return returnval  # Fix to pass the merged variables
def detect_and_replace_functions(functions: dict, code: str, vars: dict):
    debug("code3", code)
    code = split(code)
    index = 0
    replace = ""
    while index < len(code):
        try:
            if code[index][0] in "[({":
                if code[index] not in ["()", "[]", "{}"]:
                    a = detect_and_replace_functions_args(functions, code[index], vars)
                    code[index] = a
        except:
            pass
        if code[index] in vars:
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
        code = re.sub(rf'\b{re.escape(var)}\b', (str(vars[var]) if (type(vars[var]) != str) else ("\"" + re.escape(vars[var].replace("\"", "\\\"")) + "\"")), code)
    code = detect_and_replace_functions(functions, code, vars)
    return code

def eval_vars(functions: dict, stmt: str, vars: dict):
    stmt = parseExpr(functions, stmt, vars)
    debug(stmt)
    #print(stmt)
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

def merge_dict_with_list(struct=dict, values=dict):
    # Prepare the output dictionary
    result = {}
    if "" in struct:
        del struct[''] # type: ignore
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
import math
def run(code: str, functions: dict={}, vars: dict={"PI": math.pi, "E": math.e, "true": True, "false": False}):
    # Remove the outermost curly braces and split the code
    code = code.strip("{}")
    returnval = None
    code.replace("\\\n", re.escape("\n"))
    code_ = split(code)
    exceptiontable = splitline(code)
    lines = code.split("\n")
    code = code_
    index = 0
    condeval = False
    jumps = {}
    while index < len(code):
        try:
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
                        returnval, functions_, vars, returned = run(code[index][1:-1], functions, vars)
                        return returnval, functions, vars, 1
                    else:
                        returnval_, functions_, vars, returned = run(code[index][1:-1], functions, vars)
                #index += 1
            elif code[index] == "else":
                index += 1
                if not condeval:
                    if "return" in code[index][1:-1]:
                        returnval, functions_, vars, returned = run(code[index][1:-1], functions, vars)
                        return returnval, functions, vars, 1
                    else:
                        returnval_, functions_, vars, returned = run(code[index][1:-1], functions, vars)
            elif code[index] == "while":
                index += 1
                conditions = code[index]
                conditions.replace("||", " or ")
                conditions.replace("&&", " and ")
                conditions.replace("!", " not ")  
                index += 1
                condtitions = eval_vars(functions, conditions, vars)
                r = 1
                while condtitions and r:
                    returnval, functions_, vars, returned = run(code[index][1:-1], functions, vars)
                    if returned == 1: return returnval, functions, vars, 1
                    if returned == 2:
                        r = 0
                    condtitions = eval_vars(functions, conditions, vars)
                index += 1
            elif code[index] == "until":
                index += 1
                conditions = code[index]
                conditions.replace("||", " or ")
                conditions.replace("&&", " and ")
                conditions.replace("!", " not ")  
                index += 1
                condtitions = eval_vars(functions, conditions, vars)
                r = 1
                while not condtitions and r:
                    returnval, functions_, vars, returned = run(code[index][1:-1], functions, vars)
                    if returned == 1: return returnval, functions, vars, 1
                    if returned == 2:
                        r = 0
                    condtitions = eval_vars(functions, conditions, vars)
                index += 1
            elif code[index] == "using":
                index += 1
                data = ""
                filepath = code[index]
                filepath = filepath[1:-1]
                with open(filepath + ".kshp") as file:
                    data = file.read()
                _, functions1, vars1, returned = run(data)
                if returned == 1: return returnval, functions, vars, 1
                functions.update(functions1)
                vars.update(vars1)
                index += 1
            elif code[index] == "execp":
                index += 1
                expr = code[index]
                expr = expr.strip("\"")
                for i in vars:
                    expr = expr.replace(i, str(vars[i]))
                exec(expr)
            elif code[index] == "var":
                index += 1
                var_name = code[index]
                index += 2  # Skip over "="
                expr, index = find_until(code, index, ";")
                a = eval_vars(functions, "".join(expr), vars)
                debug("var", a, type(a))
                vars[var_name] = a
            elif code[index] == "println":
                index += 1
                expr = code[index]
                expr = eval_vars(functions, expr, vars)
                print(expr)
                index += 1
            elif code[index] == "print":
                index += 1
                expr = code[index]
                expr = eval_vars(functions, expr, vars)
                print(expr, end="")
                index += 1
            elif code[index] in vars:
                var_name = code[index]
                index += 1
                op = code[index]
                index += 1
                expr, index = find_until(code, index, ";")
                vars.update({"this": vars[var_name]})
                #print(expr)
                if expr != "":
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
                elif op == "append":
                    vars[var_name].append(expr)
                elif op == "extend":
                    vars[var_name].extend(expr)
                elif op == "remove":
                    vars[var_name].remove(expr)
                elif op == "sort":
                    vars[var_name].sort()
                elif op == "reverse":
                    vars[var_name].reverse()
                elif op == "insert":
                    vars[var_name].insert(expr[0], expr[1])
                elif op == "clear":
                    vars[var_name].clear()
                elif op == "add":
                    vars[var_name].add(expr)
                elif op == "update":
                    vars[var_name].update(expr)
                elif op == "discard":
                    vars[var_name].discard(expr)
                elif op == "intersection_update":
                    vars[var_name].intersection_update(expr)
            elif code[index] in functions:
                #print(code[index], code[index + 1], vars)
                run_function(functions, code[index], code[index + 1], vars)
            elif code[index] == "return":
                index += 1
                if code[index] != ";":
                    expr, index = find_until(code, index, ";")
                    return eval_vars(functions, "".join(expr), vars), functions, vars, 1
                else:
                    return None, functions, vars, 1
            elif code[index] == "break":
                index += 1
                return None, functions, vars, 2
            elif code[index] == "define":
                index += 1
                replace = code[index].strip("\"")
                index += 1
                change = code[index].strip("\"")
                code = " ".join(code)
                code = code.replace("define" + replace + change, "")
                code = code.replace(replace, change)
                code = split(code)
            elif code[index] == "label":
                index += 1
                name = code[index]
                jumps[name] = index
            elif code[index] == "jump":
                index += 1
                name = code[index]
                #print(jumps)
                index = jumps[name]
            elif code[index] == "exit":
                sys.exit()
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
                    r, functions, vars, returned = run(code[index], functions, vars)
                    if returned == 1: return returnval, functions, vars, 1
                    if returned == 2: return returnval, functions, vars, 0
                    vars.pop(mvar, "")    
                index += 1
            elif code[index] == "try":
                varsnapshot = vars
                functionsnapshot = functions
                index += 1
                ex = 0
                try:
                    returnval_, functions, vars, returned = run(code[index][1:-1], functions, vars)
                    if returned == 1: return returnval, functions, vars, 1
                except:
                    ex = 1
                    vars = varsnapshot
                    functions = functionsnapshot
                    index += 2
                    returnval_, functions, vars, returned = run(code[index][1:-1], functions, vars)
                    if returned == 1: return returnval, functions, vars, 1
                index += 1
                if ex == 0:
                    index += 1
            elif code[index] == "cmd":
                index += 1
                os.system(code[index][1:-1])
                index += 1
            debug(vars)
            index += 1
        except Exception as e:
            print("Error: " + custom_trace(e) + " at index " + str(index) + ", name \"" + code[index] + "\".")
    #print(vars)
    return returnval, functions, vars, 0
import sys
import math
import random
import time
import datetime
import os
import json
import requests
import re
import collections
import tkinter as tk
import tkinter.ttk as ttk
import PySide6.QtCore as qtcore
import PySide6.QtWidgets as qtwidget
import PySide6.QtGui as qtgui
import pygame
from sys import *
from math import *
from random import *
from time import *
from datetime import *
from json import *
from requests import *
from collections import *
from csv import *
from pygame import *
if len(sys.argv) == 2:
    run(open(sys.argv[1]).read())
    sys.exit()
print("K# IDLE version 1.3.2")
print("Type \"help\" to get help.")
print("Offical home for Kin: https://kin1009.github.io")
code = ""
while True:
    inp = input(">>> ")
    if inp == "help":
        print("""K# help:
while (a) {...}    a while loop
until (a) {...}    an until loop (while (!a))
if (a) {...}       an if statement
else {...}         if (!a)
using "path"       import a module
var a = ...        a = ...
a <tfunc> b        type function (all functions return None in py!)
print('a')         print a variable (string)
'a'                ref a var thats a string
print(a)           prints a variable not a string
a                  ref a var not a string
print("a")         print a string literal
"a"                string literal
And more
For documentation, see https://kin1009.github.io/ksharp

IDLE help:
exit               exit
run                run program
clear              clear program data""")
    elif inp == "exit":
        exit()
    elif inp == "run":
        try:
            run(code)
        except Exception as e:
            raise e
            print("Error: " + str(e))
        print()
    elif inp == "clear":
        code = ""
    else:
        code += inp + "\n"