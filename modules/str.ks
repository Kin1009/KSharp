func upper(a) {
    return evalp("str.upper(a)");
}

func lower(a) {
    return evalp("str.lower(a)");
}

func strip(a) {
    return evalp("str.strip(a)");
}

func split(a) {
    return evalp("str.split(a)");
}

func join(a, iterable) {
    return evalp("\"a\".join(iterable)");
}

func replace(a, old, new) {
    return evalp("str.replace(a, old, new)");
}

func find(a, sub) {
    return evalp("str.find(a, sub)");
}


func startswith(a, prefix) {
    return evalp("str.startswith(a, prefix)");
}

func endswith(a, suffix) {
    return evalp("str.endswith(a, suffix)");
}
