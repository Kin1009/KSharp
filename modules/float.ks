func is_integer(f) {
    return evalp("f.is_integer()");
}

func as_integer_ratio(f) {
    return evalp("f.as_integer_ratio()");
}

func hex(f) {
    return evalp("f.hex()");
}

func fromhex(s) {
    return evalp("float.fromhex(s)");
}
