func println(z) {
    print('z');
}
func print(z) {
    execp "print('z', end='')";
}
func input(c) {
    var d = "\"" + evalp(input('c')) + "\"";
    return d;
}
