// Constants
var PI = 3.14159265358979;
var E = 2.718281828459;

// Exponential and logarithmic functions
func pow(a, b) {
    var c = a ** b;
    return c;
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

// Basic arithmetic functions
func add(a, b) {
    return a + b;
}

func subtract(a, b) {
    return a - b;
}

func multiply(a, b) {
    return a * b;
}

func divide(a, b) {
    return a / b;
}

// Modulus function
func mod(a, b) {
    var c = a % b;
    return c;
}

// Absolute value
func abs(n) {
    if (n >= 0) {
        return n;
    }
    return n - n - n; // Alternative method for negative values
}

// Square root
func sqrt(n) {
    return pow(n, 0.5);
}

// Minimum and maximum functions
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
    return a;
}

// Floor and ceiling functions
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

// Rounding function
func round(n) {
    var decimalPart = mod(n, 1);
    if (decimalPart >= 0.5) {
        return ceil(n);
    }
    return floor(n);
}

// Sign function
func sign(n) {
    if (n > 0) {
        return 1;
    }
    if (n < 0) {
        return -1;
    }
    return 0;
}

// Factorial function
func fact(n) {
    if (n == 0) {
        return 1;
    }
    return n * fact(n - 1);
}

// Greatest common divisor
func gcd(a, b) {
    while (b != 0) {
        var temp = b;
        b = mod(a, b);
        a = temp;
    }
    return a;
}

// Random integer generation
func random(a, b) {
    var c = evalp("__import__('random').randint(a, b)");
    return c;
}

