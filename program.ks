using "modules/test.ks";
using "modules/io.ks";
var a = range(0, 11, 1);
a = a[-1:0:-1] + [a[0]];
print(a);