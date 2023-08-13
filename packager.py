import subprocess
import os
import shutil
import sys
sys.path.append(os.path.join(os.getcwd(),"./Patcher"))
#sys.path.append(r"C:\Users\Xaver\Documents\Uber\Skripte\UberPatcher")
import UberPatcher
#result = subprocess.run(["python -m nuitka --mingw64 --onefile UberPatcher.py"], shell=True, capture_output=True, text=True)

#print(result.stdout)

#result = subprocess.run(["python", "-m", "nuitka", "--mingw64", "UberPatcher.py" ], capture_output = True, text = True, check=True)

#print(result.stdout)


#import subprocess
def runNuitka():
    current_dir =os.getcwd()
    print(current_dir)
    os.chdir("./Patcher/exe")

    try:

        output = subprocess.check_output([r"C:\Users\Xaver\AppData\Local\Programs\Python\Python310\python.exe", r"-m", r"nuitka", r"--mingw64", "../UberPatcher.py" ], text=True)

        print(output)

    except subprocess.CalledProcessError as e:

        print(f"Command failed with return code {e.returncode}")

    os.chdir(current_dir)
    print("current dir: "+ os.getcwd())
    os.mkdir("UberPatcher")

def copyNeededFiles(current_dir=os.getcwd()):

    destination_dir = os.path.join(current_dir, "UberPatcher")
    filePackageDir = os.path.join(current_dir, "Patcher/packageInfo")
    exePath = os.path.join(current_dir, "Patcher", "exe", "UberPatcher.exe")

    UberPatcher.replaceFiles(filePackageDir, destination_dir)

    shutil.copy(exePath, destination_dir)
    
    return destination_dir


def createZip(path):

    shutil.make_archive(path, 'zip', path)

if __name__ == "__main__":
    runNuitka()
    tempFolderForZip = copyNeededFiles()
    createZip(tempFolderForZip)
    shutil.rmtree(tempFolderForZip)

