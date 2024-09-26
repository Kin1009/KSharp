import sys, os
scriptdata = open(sys.argv[1]).read()
externaldata = open(sys.argv[2]).read()
with open("temp.py", "w") as file:
    file.write(scriptdata + "\n")
    file.write(f"main(r\"\"\"{externaldata}\"\"\")")
os.system("pyinstaller -F temp.py")
os.system("copy dist/temp.exe \"" + sys.argv[1] + ".exe\"")
print("Build complete.")