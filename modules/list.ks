func append(item) {
    var a = this + [item];
    return a;
}

func extend(iterable) {
    return evalp("list.extend(this, iterable)");
}

func insert(index, item) {
    return evalp("list.insert(this, index, item)");
}

func remove(item) {
    return evalp("list.remove(this, item)");
}

func pop(index) {
    return evalp("list.pop(this, index)");
}

func clear() {
    return evalp("list.clear(this)");
}

func index(item) {
    return evalp("list.index(this, item)");
}

func count(item) {
    return evalp("list.count(this, item)");
}

func sort() {
    return evalp("list.sort(this)");
}

func reverse() {
    return evalp("list.reverse(this)");
}
