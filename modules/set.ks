func add(s, item) {
    return evalp("set.add(s, item)");
}

func remove(s, item) {
    return evalp("set.remove(s, item)");
}

func discard(s, item) {
    return evalp("set.discard(s, item)");
}

func pop(s) {
    return evalp("set.pop(s)");
}

func clear(s) {
    return evalp("set.clear(s)");
}

func union(s, other) {
    return evalp("set.union(s, other)");
}

func intersection(s, other) {
    return evalp("set.intersection(s, other)");
}

func difference(s, other) {
    return evalp("set.difference(s, other)");
}

func symmetric_difference(s, other) {
    return evalp("set.symmetric_difference(s, other)");
}
