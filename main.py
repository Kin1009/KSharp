import string, ast
import operator

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
def split(text=str):
    b = text.split("\n")
    for j, i in enumerate(b):
        if "#" in i:
            b[j] = i[:i.find("#")]
    text = "\n".join(b)
    text = text.replace("\n", "")
    res = []
    a = ""
    type_ = "str"
    layer = 0
    openm = "([{"
    closem = ")]}"
    for i in text:
        if layer == 0:
            if i in string.ascii_letters + string.digits:
                if type_ == "str":
                    a += i
                else:
                    res.append(a)
                    a = i
                    type_ = "str"
            if i in string.punctuation and (i not in openm):
                if type_ == "punc":
                    a += i
                else:
                    res.append(a)
                    a = i
                    type_ = "punc"
            if i == " ":
                res.append(a)
                a = ""
            if i in openm:
                layer += 1
                res.append(a)
                a = i
                type_ = "container"
        else:
            a += i
            if i in openm:
                layer += 1
            if i in closem:
                layer -= 1
            if layer == 0:
                res.append(a)
                a = ""
                type_ = "str"
    if a:
        res.append(a)
    try:
        while True:
            res.remove("")
    except:
        pass
    return res
def toParams(val: str):
    val = val.strip("()")
    val = val.split(",")
    for i, j in enumerate(val):
        val[i] = j.strip(" ")
    params = {}
    for i in val:
        i = i.split("=")
        if len(i) == 1:
            params[i[0]] = ("required", "")
        if len(i) == 2:
            params[i[0]] = ("optional", i[1])
    return params
def parseExpr(code: str, vars: dict):
    for i in vars:
        code = code.replace(i, str(vars[i]))
    return code
def eval_vars(stmt: str, vars: dict):
    for i in vars:
        stmt = stmt.replace(i, str(vars[i]))
    return eval(stmt)
def run(code: str, functions={}, vars={}):

    def find_until(tokens, index, end_token):
        result = []
        while index < len(tokens) and tokens[index] != end_token:
            result.append(tokens[index])
            index += 1
        return result, index

    # Remove the outermost curly braces and split the code
    code = code.strip("{}")
    code = split(code)
    print(code)
    index = 0
    callstack = []
    while index < len(code):
        if code[index] == "func":
            index += 1
            func_name = code[index]
            index += 1
            params = toParams(code[index])
            index += 1
            functions[func_name] = (params, code[index])
        elif code[index] == "print":
            index += 1
            expr, index = find_until(code, index, ";")
            print(eval_vars(" ".join(expr).strip("()"), vars))
        elif code[index] == "var":
            index += 1
            var_name = code[index]
            index += 2  # Skip over "="
            expr, index = find_until(code, index, ";")
            vars[var_name] = eval_vars(" ".join(expr), vars)
        elif code[index] in vars:
            var_name = code[index]
            index += 1
            op = code[index]
            index += 1
            expr, index = find_until(code, index, ";")
            expr = eval_vars(" ".join(expr), vars)
            
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
        index += 1
run("""func greet(name, greeting="Hello") {print("hi");
    }
print("hello");
print(13);
var b = 2;
var a = 1 + b;
a -= 1;
"Hello, world!";
print(a + 1);""")
