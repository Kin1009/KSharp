func bit_length(n) {
    return evalp("n.bit_length()");
}

func to_bytes(n, length, byteorder) {
    return evalp("n.to_bytes(length, byteorder)");
}

func from_bytes(b, byteorder) {
    return evalp("int.from_bytes(b, byteorder)");
}
