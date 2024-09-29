import sys, os
import shutil

scriptdata = open(sys.argv[1]).read()
externaldata = open(sys.argv[2]).read()
os.makedirs("temp", exist_ok=1)
with open("temp/temp.py", "w") as file:
    file.write(scriptdata + "\n")
    file.write(f"import sys\nmain(r\"\"\"{externaldata}\"\"\", sys.argv[1:])")
p = os.getcwd()
os.chdir("temp")
os.system("pyinstaller -F temp.py")
os.chdir(p)
shutil.copyfile("temp/dist/temp.exe", sys.argv[2][:-3] + ".exe")
shutil.rmtree("temp")
print("Build complete.")