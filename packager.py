import subprocess
import os
import shutil
import sys
sys.path.append(os.path.join(os.getcwd(),"./Patcher"))
import UberPatcher


def generateExe(patcher, installer):

    patcher_dir="./Patcher/exe"
    installer_dir="./Installer/exe"

    if patcher is True:
        runPatch(patcher_dir)

    if installer is True: 
        runPatch(installer_dir)    
        
def runPatch(patcher_dir):
    current_dir = os.getcwd()
    os.chdir(patcher_dir)
    runNuitka(patcher_dir)
    os.chdir(current_dir)

def runNuitka(path):

    patcher_name:str
    if "Installer" not in path and "Patcher" not in path:
        pass
        #throw Exception
    if "Installer" in path:
        patcher_name = "UberInstaller.py"
    if "Patcher" in path:
        patcher_name= "UberPatcher.py"
    
    patcher_filepath= "../"+patcher_name


    try:

        output = subprocess.check_output([r"C:\Users\Xaver\AppData\Local\Programs\Python\Python310\python.exe", r"-m", r"nuitka", r"--mingw64", patcher_filepath ], text=True)

        print(output)

    except subprocess.CalledProcessError as e:

        print(f"Command failed with return code {e.returncode}")


def copyFiles(destination_dir, filePackageDir, exePath):


    UberPatcher.replaceFiles(filePackageDir, destination_dir)

    shutil.copy(exePath, destination_dir)
    
    return destination_dir

def copyFilesForZip(patcher, installer):

    current_dir = os.getcwd()

    patcher_destination_dir:str
    installer_destination_dir:str

    if patcher is True:
        folder_name = "UberPatcher"
        os.mkdir(folder_name)
        patcher_destination_dir = os.path.join(current_dir, folder_name)
        filePackageDir = os.path.join(current_dir, "Patcher/packageInfo")
        exePath = os.path.join(current_dir, "Patcher", "exe", "UberPatcher.exe")
        copyFiles(patcher_destination_dir, filePackageDir, exePath)
    if installer is True:
        folder_name = "UberInstaller"
        os.mkdir(folder_name)
        installer_destination_dir = os.path.join(current_dir, folder_name)
        filePackageDir = os.path.join(current_dir, "Installer/packageInfo")
        exePath = os.path.join(current_dir, "Installer", "exe", "UberInstaller.exe")
        copyFiles(installer_destination_dir, filePackageDir, exePath)

    return patcher_destination_dir, installer_destination_dir

def createZip(path):

    zip_file_name_with_path = path
    folder_path = path
    shutil.make_archive(zip_file_name_with_path, 'zip', folder_path)

if __name__ == "__main__":
    generateExe(True, True)
    tempFolderForZipPatcher, tempFolderForZipInstaller = copyFilesForZip(True, True)
    if tempFolderForZipPatcher != "":
        createZip(tempFolderForZipPatcher)
        shutil.rmtree(tempFolderForZipPatcher)

    if tempFolderForZipInstaller != "":
        createZip(tempFolderForZipInstaller) 
        shutil.rmtree(tempFolderForZipInstaller)   



