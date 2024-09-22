var PI = 3.14159265358979;
var E = 2.718281828459;
func pow(a, b) {
    var c = a ** b;
    return c;
}
func mod(a, b) {
    var c = a % b;
    return c;
}
func abs(n) {
    if (n >= 0) {
        return n;
    }
    if (n < 0) {
        n -= n;
        n -= n;
        return n;
    }
}
func sqrt(n) {
    return pow(n, 0.5);
}
func min(a, b) {
    if (a < b) {
        return a;
    }
    return b;
}
func max(a, b) {
    if (a < b) {
        return b;
    }
    if (a >= b) {
        return a;
    }
}
func floor(n) {
    if (mod(n, 1) == 0) {
        return n;
    }
    return n - mod(n, 1);
}
func ceil(n) {
    if (mod(n, 1) == 0) {
        return n;
    }
    return n + 1 - mod(n, 1);
}
func round(n) {
    var decimalPart = mod(n, 1);
    if (decimalPart >= 0.5) {
        return ceil(n);
    }
    return floor(n);
}
func sign(n) {
    if (n > 0) {
        return 1;
    }
    if (n < 0) {
        return -1;
    }
    return 0;
}
func exp(n) {
    return pow(E, n);
}
func log(n) {
    var result = 0;
    var approx = n - 1;
    while (approx > 0) {
        approx = approx / E;
        result += 1;
    }
    return result;
}
func fact(n) {
    if (n == 0) {
        return 1;
    }
    if (n > 0) {
        var b = fact(n - 1);
        b *= n;
        return b;
    }
}
func gcd(a, b) {
    while (b != 0) {
        var temp = b;
        b = mod(a, b);
        a = temp;
    }
    return a;
}
func random(a, b) {
    var c = evalp("__import__(\"random\").randint(a, b)");
    return c;
}