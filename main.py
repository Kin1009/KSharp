import string
import re
import traceback
import ctypes
import warnings
import copy
from ctypes import wintypes
import sys
import math
import random
import time
import datetime
import os
import json
import requests # type: ignore
import re
import collections
import tkinter as tk
import tkinter.ttk as ttk
import PySide6.QtCore as qtcore # type: ignore
import PySide6.QtWidgets as qtwidget # type: ignore
import PySide6.QtGui as qtgui # type: ignore
import pygame # type: ignore
from sys import *
from math import *
from random import *
from time import *
from datetime import *
from json import *
from requests import * # type: ignore
from collections import *
from csv import *
from pygame import * # type: ignore
import zipfile
import io
import shutil

# Importing and creating type aliases from ctypes.wintypes for convenience
from ctypes.wintypes import (
    BOOL as cbool,         # Boolean (0 or non-zero)
    BYTE as byte,          # 8-bit unsigned integer
    WORD as word,          # 16-bit unsigned integer
    DWORD as dword,        # 32-bit unsigned integer
    INT as cint,           # 32-bit signed integer
    UINT as cuint,         # 32-bit unsigned integer
    LONG as clong,         # 32-bit signed integer
    ULONG as culong,       # 32-bit unsigned integer
    HANDLE as handle,      # Generic handle to an object
    HWND as hwnd,          # Handle to a window
    HMODULE as hmodule,    # Handle to a module (DLL/EXE)
    HINSTANCE as hinstance, # Handle to an instance (similar to HMODULE)
    LPCSTR as lpcstr,    # Pointer to a constant ANSI string
    LPCWSTR as lpcwstr,  # Pointer to a constant wide Unicode string
    LPSTR as lpstr,      # Pointer to a mutable ANSI string
    LPWSTR as lpwstr,    # Pointer to a mutable wide Unicode string
    LPVOID as lpvoid,      # Generic pointer (void *)
    FLOAT as cfloat,       # Single-precision floating-point number
    DOUBLE as cdouble,     # Double-precision floating-point number
    FILETIME as filetime,  # Structure for file times
    WPARAM as wparam,      # Message parameter (typically 32-bit or 64-bit)
    LPARAM as lparam,      # Message parameter (used in message handling)
    ATOM as atom,          # 16-bit identifier
    COLORREF as colorref,  # 32-bit value to define RGB colors
)
# Importing and creating type aliases from ctypes for convenience
from ctypes import (
    c_char as char,              # 8-bit character (signed)
    c_byte as cbyte,             # 8-bit signed integer
    c_ubyte as ubyte,            # 8-bit unsigned integer
    c_short as short,            # 16-bit signed integer
    c_ushort as ushort,          # 16-bit unsigned integer
    c_int as cint,               # 32-bit signed integer
    c_uint as uint,              # 32-bit unsigned integer
    c_long as long,              # 32-bit signed integer (same as cint)
    c_ulong as ulong,            # 32-bit unsigned integer
    c_longlong as longlong,      # 64-bit signed integer
    c_ulonglong as ulonglong,    # 64-bit unsigned integer
    c_float as cfloat,           # Single-precision floating-point number
    c_double as double,          # Double-precision floating-point number
    c_longdouble as longdouble,  # Extended precision floating-point number
    c_void_p as voidp,           # Pointer to void (generic pointer)
    c_char_p as charp,           # Pointer to a C-style string (char *)
    c_wchar_p as wcharp,         # Pointer to a wide-character string (wchar_t *)
    c_bool as cbool,             # Boolean (True or False)
    c_int8 as int8,              # 8-bit signed integer
    c_int16 as int16,            # 16-bit signed integer
    c_int32 as int32,            # 32-bit signed integer
    c_int64 as int64,            # 64-bit signed integer
    c_uint8 as uint8,            # 8-bit unsigned integer
    c_uint16 as uint16,          # 16-bit unsigned integer
    c_uint32 as uint32,          # 32-bit unsigned integer
    c_uint64 as uint64           # 64-bit unsigned integer
)
class WIN32_FIND_DATAW(ctypes.Structure):
    _fields_ = [
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", wintypes.FILETIME),
        ("ftLastAccessTime", wintypes.FILETIME),
        ("ftLastWriteTime", wintypes.FILETIME),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("dwReserved0", wintypes.DWORD),
        ("dwReserved1", wintypes.DWORD),
        ("cFileName", wintypes.WCHAR * 260),
        ("cAlternateFileName", wintypes.WCHAR * 14)
    ]
LPWIN32_FIND_DATAW = ctypes.POINTER(WIN32_FIND_DATAW)
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", ctypes.c_uint16),
        ("wMonth", ctypes.c_uint16),
        ("wDayOfWeek", ctypes.c_uint16),
        ("wDay", ctypes.c_uint16),
        ("wHour", ctypes.c_uint16),
        ("wMinute", ctypes.c_uint16),
        ("wSecond", ctypes.c_uint16),
        ("wMilliseconds", ctypes.c_uint16)
    ]
lresult = ctypes.c_longlong
hresult = ctypes.c_long
# Suppress all warnings
warnings.filterwarnings("ignore")

def open_as_module(path):
    return open(getfile(path))
def getfile(path):
    # Check if the path exists in the current working directory
    cwd_path = os.path.abspath(path)
    if os.path.exists(cwd_path):
        return cwd_path

    # Check if the file exists in the system directory (e.g., C:\Windows\System32)
    system_path = os.path.join(os.getenv('SystemRoot'), 'System32', path)
    if os.path.exists(system_path):
        return system_path

    # Check if the file exists in the custom APPDATA directory
    custom_path = os.path.join(os.getenv('APPDATA'), 'K#', path)
    if os.path.exists(custom_path):
        return custom_path

    # If the file doesn't exist in any of the checked locations, raise an error
    raise FileNotFoundError(f"No file named {path}")


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
    text = " ".join(lines)

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
def run_function(exec_vars, functions, function_name, args: str, vars, classes, cdll: dict):
    func_name = function_name
    #print(args)
    args = args[1:-1]
    if args != "": 
        args += ","
    args = "(" + args + ")"
    args = eval_vars(exec_vars, functions, args, vars, classes, cdll)  # Evaluate the arguments
    #print(args)
    funcdata = functions[func_name]
    req = funcdata[0]
    func_code = funcdata[1]
    merged_vars = merge_dict_with_list(req, args)
    merged_vars.update(vars)
    returnval, a, b, returned, exec_vars, classes, cdll = run(exec_vars, func_code, functions, merged_vars, classes)
    del merged_vars
    return returnval  # Fix to pass the merged variables
def run_function_modify(exec_vars, functions, function_name, args: str, vars, classes, cdll):
    func_name = function_name
    #print(args)
    args = args[1:-1]
    if args != "": 
        args += ","
    args = "(" + args + ")"
    args = eval_vars(exec_vars, functions, args, vars, classes, cdll)  # Evaluate the arguments
    #print(args)
    funcdata = functions[func_name]
    req = funcdata[0]
    func_code = funcdata[1]
    merged_vars = merge_dict_with_list(req, args)
    merged_vars.update(vars)
    for i in merged_vars:
        if i[0] == ":": #ref
            ref_var = id(merged_vars[i])
            for j in vars:
                if id(vars[j]) == ref_var:
                    func_code = func_code.replace(i, j)
    returnval, a, b, returned, exec_vars, classes, cdll = run(exec_vars, func_code, functions, merged_vars, classes)
    del merged_vars
    return returnval, a, b, returned, exec_vars, classes  # Fix to pass the merged variables
def detect_and_replace_functions(exec_vars, functions: dict, code: object, vars: dict, classes: dict, cdll: dict):
    debug("code3", code)
    code = split(code)
    index = 0
    replace = ""
    while index < len(code):
        try:
            if code[index][0] in "[({":
                if code[index] not in ["()", "[]", "{}"]:
                    a = detect_and_replace_functions_args(exec_vars, functions, code[index], vars, classes, cdll)
                    code[index] = a
        except:
            pass
        if code[index] == "read":
            func_name = code[index]
            index += 1
            args = code[index]
            replace = func_name + args
            value = "\"" + open(args[1:-1]).read().replace("\n", "\\ ") + "\""
            code = "".join(code)
            debug("replace", replace)
            debug("replace2", str(value))
            code = code.replace(replace, str(value))
            debug("replace3", code)
            code = split(code)
        elif code[index] == "*":
            index += 1
            varname = code[index]
            replace = "*" + varname
            if varname in vars:
                varname = vars[varname]
            value = ctypes.cast(int(varname), ctypes.py_object).value
            code = "".join(code)
            debug("replace", replace)
            debug("replace2", str(value))
            code = code.replace(replace, str(value))
            debug("replace3", code)
            code = split(code)
        elif code[index] == "&":
            index += 1
            varname = code[index]
            replace = "&" + varname
            try:
                value = id(vars[varname])
            except:
                try:
                    value = id(functions[varname])
                except:
                    try:
                        value = id(classes[varname])
                    except:
                        value = id(varname)
            code = "".join(code)
            debug("replace", replace)
            debug("replace2", str(value))
            code = code.replace(replace, str(value))
            debug("replace3", code)
            code = split(code)
        elif code[index].split(".")[0] in cdll:
            name_ = code[index] + code[index + 1]
            name = code[index].split(".")[0]
            func_name = code[index].split(".")[1]
            index += 1
            replace = str(eval(f'cdll[\"{name}\"].{func_name}{eval_vars(exec_vars, functions, code[index], vars, classes, cdll)}'))
            code = "".join(code)
            code = code.replace(name_, replace)
            code = split(code)
        elif code[index] in vars:
            index += 1
            if code[index][0] == "[":
                range_ = code[index]
                range__ = range_[1:-1].split(":")
                for i, j in enumerate(range_):
                    range__[i] = int(eval_vars(exec_vars, functions, range_[i], vars, classes, cdll))
                value = eval_vars(exec_vars, functions, code[index - 1], vars, classes, cdll)
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
            value = run_function(exec_vars, functions, func_name, args, vars, classes, cdll)
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
def detect_and_replace_functions_args(exec_vars, functions, args, vars, classes, cdll):
    a = ""
    if args.startswith("("):
        a = "(" + detect_and_replace_functions(exec_vars, functions, args[1:-1], vars, classes, cdll) + ")"
    if args.startswith("["):
        a = "[" + detect_and_replace_functions(exec_vars, functions, args[1:-1], vars, classes, cdll) + "]"
    if args.startswith("{"):
        a = "{" + detect_and_replace_functions(exec_vars, functions, args[1:-1], vars, classes, cdll) + "}"
    #print(a)
    return a
def parseExpr(exec_vars, functions: dict, code: object, vars: dict, classes: dict, cdll: dict):
    #raise Exception()
    #debug("a" + code)
    code = detect_and_replace_functions(exec_vars, functions, code, vars, classes, cdll)
    for var in vars:
        # Using \b for word boundaries to match whole words only
        code = re.sub(rf'\b{re.escape(var)}\b', (str(vars[var]) if (type(vars[var]) != str) else ("\"" + vars[var] + "\"")), code)
    return code.replace("\\n", "\n")

def eval_vars(exec_vars, functions: dict, stmt: str, vars: dict, classes: dict, cdll: dict):
    stmt = parseExpr(exec_vars, functions, stmt, vars, classes, cdll)
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
def run(exec_vars: dict = {}, code: object = "", functions: dict={}, vars: dict={"true": True, "false": False, "null": None}, classes: dict = {}, cdll: dict = {}):
    # Remove the outermost curly braces and split the code
    code = code.strip("{}")
    returnval = None
    code = code.replace("\\\\s", "internal_spc_s").replace("\\s", " ").replace("internal_spc_s", "\\\\s")
    code_ = split(code)
    exceptiontable = splitline(code)
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
                if code[index] == ":":
                    index += 1
                    inherited = code[index]
                    functions[func_name] = functions[inherited]
                    index += 1
                    if code[index].startswith("("):
                        params = toParams(code[index])
                        index += 1
                        func_body = code[index]
                        functions[func_name] = [functions[inherited][0] | params, functions[inherited][1][:-1] + " " + func_body[1:]]
                    else:
                        func_body = code[index]
                        functions[func_name][1] = functions[inherited][1][:-1] + " " + func_body[1:]
                else:
                    params = toParams(code[index])
                    index += 1
                    func_body = code[index]
                    functions[func_name] = [params, func_body]
            elif code[index] == "if":
                index += 1
                conditions = code[index]
                conditions = conditions.replace("||", " or ")
                conditions = conditions.replace("&&", " and ")
                conditions = conditions.replace("!", " not ") 
                conditions = eval_vars(exec_vars, functions, conditions, vars, classes, cdll)
                condeval = conditions
                index += 1
                if conditions:
                    if "return" in code[index][1:-1]:
                        returnval, functions_, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                        return returnval, functions, vars, 1, exec_vars, classes, cdll
                    else:
                        returnval_, functions_, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                #index += 1
            elif code[index] == "else":
                index += 1
                if not condeval:
                    if "return" in code[index][1:-1]:
                        returnval, functions_, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                        return returnval, functions, vars, 1, exec_vars, classes, cdll
                    else:
                        returnval_, functions_, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
            elif code[index] == "while":
                index += 1
                conditions = code[index]
                conditions.replace("||", " or ")
                conditions.replace("&&", " and ")
                conditions.replace("!", " not ")  
                index += 1
                condtitions = eval_vars(exec_vars, functions, conditions, vars, classes, cdll)
                r = 1
                while condtitions and r:
                    returnval, functions_, vars, returned, exec_vars, classe, cdlls = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                    if returned == 1: return returnval, functions, vars, 1, exec_vars, classes, cdll
                    if returned == 2:
                        r = 0
                    condtitions = eval_vars(exec_vars, functions, conditions, vars, classes, cdll)
                index += 1
            elif code[index] == "until":
                index += 1
                conditions = code[index]
                conditions.replace("||", " or ")
                conditions.replace("&&", " and ")
                conditions.replace("!", " not ")  
                index += 1
                condtitions = eval_vars(exec_vars, functions, conditions, vars, classes, cdll)
                r = 1
                while not condtitions and r:
                    returnval, functions_, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                    if returned == 1: return returnval, functions, vars, 1, exec_vars, classes, cdll
                    if returned == 2:
                        r = 0
                    condtitions = eval_vars(exec_vars, functions, conditions, vars, classes, cdll)
                index += 1
            elif code[index] == "extern":
                index += 1
                filepath = code[index]
                if filepath.startswith("\""):
                    filepath = filepath[1:]
                if filepath.endswith("\""):
                    filepath = filepath[:-1]
                index += 2
                name = code[index]
                try:
                    cdll[name] = ctypes.CDLL(getfile(filepath))
                except:
                    cdll[name] = ctypes.WinDLL(getfile(filepath))
            elif code[index] == "dllfunc":
                index += 1
                restype = code[index]
                index += 1
                function__ = code[index]
                index += 1
                types = code[index]
                exec(f'cdll[\"{function__.split(".")[0]}\"].{function__.split(".")[1]}.argtypes = {types}')
                exec(f'cdll[\"{function__.split(".")[0]}\"].{function__.split(".")[1]}.restype = {restype}')
            elif code[index].split(".")[0] in cdll:
                name = code[index].split(".")[0]
                func_name = code[index].split(".")[1]
                index += 1
                exec(f'cdll[\"{name}\"].{func_name}{eval_vars(exec_vars, functions, code[index], vars, classes, cdll)}')
            elif code[index] == "using":
                index += 1
                data = ""
                filepath = code[index].strip("\"")
                with open_as_module(filepath + ".kshp") as file:
                    data = file.read()
                vars = copy.deepcopy(vars)
                _, functions1, vars1, returned, exec_vars, classes, cdll = run(exec_vars, data)
                filepath = os.path.basename(filepath)
                functions2 = {}
                vars2 = {}
                index += 1
                if code[index] == ";":
                    for i in functions1:
                        functions2[filepath + "." + i] = functions1[i]
                    for i in vars1:
                        vars2[filepath + "." + i] = vars1[i]
                    functions.update(functions2)
                    vars.update(vars2)
                elif code[index] == "as":
                    index += 1
                    name = code[index]
                    for i in functions1:
                        functions2[name + "." + i] = functions1[i]
                    for i in vars1:
                        vars2[name + "." + i] = vars1[i]
                    functions.update(functions2)
                    vars.update(vars2)
                    index += 1
            elif code[index] == "class":
                index += 1
                name = code[index]
                index += 1
                inherited = ""
                if code[index] == ":":
                    index += 1
                    inherited = code[index]
                else:
                    index -= 1
                index += 1
                data = code[index][1:-1]
                classes[name] = [data, inherited]
            elif code[index] == "python":
                index += 1
                expr = code[index]
                expr = expr[1:-1].strip("\"")
                for i in vars:
                    expr = expr.replace(i, str(vars[i]))
                exec(expr, globals(), exec_vars)
            elif code[index] == "var":
                index += 1
                var_name = code[index]
                index += 2  # Skip over "="
                if code[index] != "new":
                    expr, index = find_until(code, index, ";")
                    a = eval_vars(exec_vars, functions, "".join(expr), vars, classes, cdll)
                    debug("var", a, type(a))
                    vars[var_name] = a
                else:
                    index += 1
                    name = code[index]
                    data = classes[name]
                    inherit = data[1]
                    data = data[0]
                    if inherit != "":
                        inherit_data = classes[inherit][0]
                        vars = copy.deepcopy(vars)
                        __, functions1, vars1, _, exec_vars, classes, cdll = run(exec_vars, inherit_data.replace("self", var_name))
                        functions2 = {}
                        vars2 = {}
                        for i in functions1:
                            functions2[var_name + "." + i] = functions1[i]
                        for i in vars1:
                            vars2[var_name + "." + i] = vars1[i]
                        functions.update(functions2)
                        vars.update(vars2)
                    vars = copy.deepcopy(vars)
                    __, functions1, vars1, _, exec_vars, classes, cdll = run(exec_vars, data.replace("self", var_name))
                    functions2 = {}
                    vars2 = {}
                    for i in functions1:
                        functions2[var_name + "." + i] = functions1[i]
                    for i in vars1:
                        vars2[var_name + "." + i] = vars1[i]
                    functions.update(functions2)
                    vars.update(vars2)
                    index += 1
            elif code[index] == "println":
                index += 1
                expr = code[index]
                expr = eval_vars(exec_vars, functions, expr, vars, classes, cdll)
                if type(expr) != str:
                    print(expr)
                else:
                    print(expr.replace("\\ ", "\n"))
                index += 1
            elif code[index] == "print":
                index += 1
                expr = code[index]
                expr = eval_vars(exec_vars, functions, expr, vars, classes, cdll)
                if type(expr) != str:
                    print(expr, end="")
                else:
                    print(expr.replace("\\ ", "\n"), end="")
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
                    expr = eval_vars(exec_vars, functions, "".join(expr), vars, classes, cdll)
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
            elif code[index] == "*":
                index += 1
                var_name = code[index]
                if var_name in vars:
                    var_name = vars[var_name]
                var_name = int(var_name)
                for i in vars:
                    if id(vars[i]) == var_name:
                        var_name = i
                        break
                index += 1
                op = code[index]
                index += 1
                expr, index = find_until(code, index, ";")
                vars.update({"this": vars[var_name]})
                #print(expr)
                if expr != "":
                    expr = eval_vars(exec_vars, functions, "".join(expr), vars, classes, cdll)
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
                #print(code[index], code[index + 1], vars, classes, cdll)
                __, functions_, vars_, _, exec_vars, classes = run_function_modify(exec_vars, functions, code[index], code[index + 1], vars, classes, cdll)
                functions.update(functions_)
                vars.update(vars_)
            elif code[index] == "return":
                index += 1
                if code[index] != ";":
                    expr, index = find_until(code, index, ";")
                    return eval_vars(exec_vars, functions, "".join(expr), vars, classes, cdll), functions, vars, 1, exec_vars, classes
                else:
                    return None, functions, vars, 1, exec_vars, classes
            elif code[index] == "break":
                index += 1
                return None, functions, vars, 2, exec_vars, classes
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
                iterable = eval_vars(exec_vars, functions, iterable, vars, classes, cdll)
                index += 1
                for i in iterable:
                    update_vars = vars
                    update_vars.update({mvar: i})
                    r, functions, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index], functions, vars, classes, cdll)
                    if returned == 1: return returnval, functions, vars, 1, exec_vars, classes, cdll
                    if returned == 2: return returnval, functions, vars, 0, exec_vars, classes, cdll
                    vars.pop(mvar, "")    
                index += 1
            elif code[index] == "try":
                varsnapshot = vars
                functionsnapshot = functions
                index += 1
                ex = 0
                try:
                    returnval_, functions, vars, returned, exec_vars, classes, cdll = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                    if returned == 1: return returnval, functions, vars, 1, exec_vars, classes, cdll
                except:
                    ex = 1
                    vars = varsnapshot
                    functions = functionsnapshot
                    index += 2
                    returnval_, functions, vars, returned, exec_vars, classe, cdlls = run(exec_vars, code[index][1:-1], functions, vars, classes, cdll)
                    if returned == 1: return returnval, functions, vars, 1, exec_vars, classes, cdll
                index += 1
                if ex == 0:
                    index += 1
            elif code[index] == "cmd":
                index += 1
                os.system(code[index][1:-1])
                index += 1
            elif code[index] == "entrypoint":
                index += 2
            elif code[index][0] in string.ascii_letters:
                print("Error: unknown token \"" + code[index] + "\" at index " + str(index) + ", name \"" + code[index] + "\".")
                break
            index += 1
        except Exception as e:
            print("Error: " + custom_trace(e) + " at index " + str(index) + ", name \"" + code[index] + "\".")
            break
    #print(vars, classes)
    return returnval, functions, vars, 0, exec_vars, classes, cdll

def get_repo(link, dest):
    # Get the repository's zip download URL
    if link.endswith('/'):
        link = link[:-1]
    
    if link.endswith('.git'):
        link = link[:-4]
        
    zip_url = f"{link}/archive/refs/heads/main.zip"  # Assuming main branch, adjust if needed
    
    # Download the repository zip
    response = requests.get(zip_url)
    
    if response.status_code == 200:
        # Create destination directory if it doesn't exist
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        # Extract zip file into the destination folder
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dest)
        
        # Find the extracted folder (repo-name-main)
        extracted_folder = os.path.join(dest, link.split("/")[-1] + "-main")
        
        # Move contents to the parent directory (dest)
        for item in os.listdir(extracted_folder):
            source = os.path.join(extracted_folder, item)
            target = os.path.join(dest, item)
            shutil.move(source, target)
        
        # Remove the now empty folder (repo-name-main)
        shutil.rmtree(extracted_folder)
        
        print(f"Repository downloaded and moved to {dest}")
    else:
        print(f"Failed to download repository. HTTP Status code: {response.status_code}")
if len(sys.argv) > 1:
    if sys.argv[1] == "pm":
        get_repo("https://github.com/" + sys.argv[2], os.getenv("APPDATA") + "\\K#\\")
        sys.exit()
    entry_point = "main"
    a = split(open(sys.argv[1]).read())
    try:
        entry_point = a[1 + a.index("entrypoint")]
    except:
        pass
    _, functions, vars, __, exec_vars, classes, cdll = run({}, open(sys.argv[1]).read())
    sys.exit()
print("K# IDLE version 1.4.6")
print("Type \"help\" to get help.")
print("Offical home for Kin: https://kin1009.github.io")
incontainer = 0
code = ""
multiline = ""
exec_vars, functions, vars, classes, cdll = {}, {}, {}, {}, {}
while True:
    if not incontainer:
        inp = input(">>> ")
    else:
        inp = input("... ")
    if not incontainer:
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
    cmd "a"            execute a in batch
    py("code")         execute code in python
    class a {}         a class
    class a : base {}  a class that inherited base
    func a(args) {}    a function
    func a : basefunc {} a function that inherited basefunc
    var a = new class; init a class as a
    self. ...          root of self (class)
    And more
    For documentation, see https://kin1009.github.io/ksharp

    IDLE help:
    exit               exit
    save <filepath>    save to filepath
    clear              clear program data
    pm user/repo       install a package from github to local""")
        elif inp == "exit":
            exit()
        elif inp == "clear":
            code = ""
        elif inp.startswith("save"):
            inp = inp.split(" ")
            out = inp[1]
            with open(out, "w") as f:
                f.write(code)
            print("Saved file to " + out + ".")
            print("Type \"clear\" to clear.")
        elif inp.startswith("pm"):
            inp = inp.split(" ")
            get_repo("https://github.com/" + inp[1], os.getenv("APPDATA") + "\\K#\\")
        elif inp:
            a = 0
            for i in inp:
                if i == "{":
                    a += 1
                elif i == "}":
                    a -= 1
            if a == 0:
                incontainer = 0
                code += inp + "\n"
                _, functions, vars, __, exec_vars, classes, cdll = run(exec_vars, inp, functions, vars, classes, cdll)
                print()
            else:
                incontainer = 1
                multiline = inp + "\n"
    else:
        for i in inp:
            if i == "{":
                a += 1
            elif i == "}":
                a -= 1
        multiline += inp + "\n"
        if not a:
            code += multiline + "\n"
            _, functions, vars, __, exec_vars, classes, cdll = run(exec_vars, multiline, functions, vars, classes, cdll)
            print()
            incontainer = 0