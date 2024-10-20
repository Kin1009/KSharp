# K#
K# is a programming language syntacically similar to V# or C# or C++ or python or etc, but with some additions
NOTE: The file size is too big so Drive for this: https://drive.google.com/drive/folders/1ygNvL3y44Y0gZpFXp1G6X8_xtMitlw91?usp=sharing
# Version symbols
- f: Failed version
- a, b, c and d, e: Subversions, usually added in the same day
- t: Testing
# Changelog
- Version 0.0.2: Function calls
- Version 1.0.0: yea i skipped but uhh basics are complete
- Version 1.1.0: add using
- Version 1.2.0: Fixed some bugs, turned execp to a keyword and working evalp()
- Version 1.2.4: Added function nesting
- Version 1.2.5a: Added some custom modules (doesn't work)
- Version 1.2.5b: Added 'this' kw (alavable on modify/create vars, plan on class)
- Version 1.2.6: Added 'for' kw, added range() (on "modules/test.ks")
- Version 1.2.7: Added slicing (a[1:4])
- Version 1.2.8f: Failed, but added compiler
- Version 1.2.9fa: Added C# port (not working)
- Version 1.2.9tb: Added working IO, but under specific 
circumstances
- Version 1.3.0ta: Way for input:
if using the builtin "io" package, put ' on start and end of answer.
Example: 'a';
- Version 1.3.0tb: To represent a string in K# we use 'varname' or "mystring" directly. (we only use ", ' is for another purpose idk)
Example: 
'mystring'
"Hello, world!';
- Version 1.3.0tc: Changed fileextension to .kshp
- Version 1.3.0td: "using" keywords now take no fileextension (uses .kshp default)
- Version 1.3.0te: Somehow K# can call builtin functions
- Version 1.3.1a: Real IO, input() now will be string, some basic list functions
- Version 1.3.1b: Added keywords: define, jump, label
- Version 1.3.2a: Removed evalp and added type functions
- Version 1.3.2b: Also I realized I can use python modules so uhhhh no more builtin modules just diy ones
- Version 1.3.2c: That kinda defeats the purpose of K#
- Version 1.3.3: Alias to 1.3.2, added installer
- Version 1.3.4: Added GUI support (tkinter), python styled syntax
- Version 1.3.5: Added "cmd" keyword
- Version 1.3.7: Inheritable functions, modules have class-like structure
- Version 1.3.8: Added classes (finally), added "self" kw
- Version 1.3.9: Added package manager: ```main.exe pm user\repo```
Example for a class:
myclass.kshp:
```
var a = 0;
func cat() {
    println(self.a);
    self.a += 1;
}
```
program.kshp:
```
class a = myclass;
a.cat(); # 0
a.cat(); # 1
a.cat(); # 2
```
# To do
1. Add package manager