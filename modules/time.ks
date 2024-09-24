func sleep(seconds) {
    evalp("__import__('time').sleep(seconds)");
}

func time() {
    return evalp("__import__('time').time()");
}

func localtime() {
    return evalp("__import__('time').localtime()");
}

func strftime(format, t) {
    return evalp("__import__('time').strftime(format, t)");
}

func strptime(date_string, format) {
    return evalp("__import__('time').strptime(date_string, format)");
}

func perf_counter() {
    return evalp("__import__('time').perf_counter()");
}

func process_time() {
    return evalp("__import__('time').process_time()");
}

func monotonic() {
    return evalp("__import__('time').monotonic()");
}

func time_ns() {
    return evalp("__import__('time').time_ns()");
}
