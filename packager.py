import subprocess
import os
import shutil
import sys
sys.path.append(os.path.join(os.getcwd(),"./Patcher"))
import UberPatcher

class Packager:
    def __init__(self, name, package_path, exe_path):
        self.name = name
        self.package_path = package_path
        self.exe_path = exe_path

    def generateExe(self):
        filepath= "../"+self.name+".py"

        try:
            output = subprocess.check_output([r"C:\Users\Xaver\AppData\Local\Programs\Python\Python310\python.exe", r"-m", r"nuitka", r"--mingw64", filepath ], cwd=self.exe_path, text=True)
            print(output)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")

    def createTempDirectory(self):
        if os.path.exists("./"+self.name):
            self.deleteTempDirectory()
        
        os.mkdir(self.name)
    
    def deleteTempDirectory(self):
        shutil.rmtree("./"+self.name)

    def copyFiles(self):
        raise NotImplementedError()

    def packageAsZip(self):
        self.createTempDirectory()
        self.copyFiles()
        shutil.make_archive("./"+self.name, 'zip', "./"+self.name)
        self.deleteTempDirectory()

def packageHandler():
    patcher=True
    installer=True
    packager_list =[]
    if patcher:
        patcher_instance=PatcherPackager("UberPatcher", "./Patcher/packageInfo", "./Patcher/exe")
        packager_list.append(patcher_instance)
    
    if installer:
        installer_instance=InstallerPackager("UberInstaller", "./Patcher/packageInfo", "./Installer/exe")
        packager_list.append(installer_instance)

    for packager in packager_list:
        packager.generateExe()
        packager.packageAsZip()


class PatcherPackager(Packager):
    def copyFiles(self):
        UberPatcher.replaceFiles(self.package_path, "./"+self.name)

        exe_filepath=self.exe_path+"/"+self.name+".exe"
        shutil.copy(exe_filepath, "./"+self.name)

class InstallerPackager(Packager):
    def copyFilesFromUberstrikeInstallation(self):
        self.executeUberPatcher()
        UberPatcher.replaceFiles(r"C:\Program Files (x86)\Steam\steamapps\common\UberStrike" ,"./"+self.name+"/UberStrike" )

    def executeUberPatcher(self):
        try:
            output = subprocess.check_output([r"C:\Users\Xaver\AppData\Local\Programs\Python\Python310\python.exe", "./Patcher/UberPatcher.py" ], text=True)
            print(output)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
        pass


    def copyFiles(self):
        UberPatcher.replaceFiles(self.package_path, "./"+self.name)

        exe_filepath=self.exe_path+"/"+self.name+".exe"
        shutil.copy(exe_filepath, "./"+self.name)

        self.copyFilesFromUberstrikeInstallation()




if __name__ == "__main__":
    packageHandler()
