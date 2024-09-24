func get(dct, key, default=None) {
    return evalp("dict.get(dct, key, default)");
}

func keys(dct) {
    return evalp("dict.keys(dct)");
}

func values(dct) {
    return evalp("dict.values(dct)");
}

func items(dct) {
    return evalp("dict.items(dct)");
}

func update(dct, other) {
    return evalp("dict.update(dct, other)");
}

func pop(dct, key, default=None) {
    return evalp("dict.pop(dct, key, default)");
}

func clear(dct) {
    return evalp("dict.clear(dct)");
}

func copy(dct) {
    return evalp("dict.copy(dct)");
}
