import subprocess
import os
import shutil
import argparse
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
        print("Start generating exe for " + self.name)

        try:
            output = subprocess.run(["python", r"-m", r"nuitka", r"--mingw64", filepath ], cwd=self.exe_path)
            #print(output)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
        print("Done generating exe for " + self.name)

    def createTempDirectory(self):
        if os.path.exists("./"+self.name):
            self.deleteTempDirectory()
        
        os.mkdir(self.name)
    
    def deleteTempDirectory(self):
        shutil.rmtree("./"+self.name)

    def copyFiles(self):
        raise NotImplementedError()

    def packageAsZip(self):
        print("Start packaging for " + self.name)
        self.createTempDirectory()
        self.copyFiles()
        shutil.make_archive("./"+self.name, 'zip', "./"+self.name)
        self.deleteTempDirectory()
        print("Done packaging for " + self.name)

def packageHandler():

    patcher, installer = parseArguments()
    packager_list =[]
    if patcher:
        patcher_instance=PatcherPackager("UberPatcher", "./Patcher/packageInfo", "./Patcher/exe")
        packager_list.append(patcher_instance)
    
    if installer:
        installer_instance=InstallerPackager("UberInstaller", "./Patcher/packageInfo", "./Installer/exe")
        packager_list.append(installer_instance)

    if not packager_list:
        print("specify which patcher to package: --all/-a, --patcher/-p or --installer/-i")
        input()
        return

    for packager in packager_list:
        packager.generateExe()
        packager.packageAsZip()

    print("Done completely!")
    input()
    return

def parseArguments():
    parser = argparse.ArgumentParser(description='UberPatcher packager.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--installer','-i', help=argparse.SUPPRESS, action='store_true') 
    group.add_argument('--patcher','-p', help=argparse.SUPPRESS, action='store_true')
    group.add_argument('--all','-a', help=argparse.SUPPRESS, action='store_true')
    args = parser.parse_args()

    if args.all is True:
        return True, True
        
    return args.patcher, args.installer, 


class PatcherPackager(Packager):
    def copyFiles(self):
        UberPatcher.replaceFiles(self.package_path, "./"+self.name)

        exe_filepath=self.exe_path+"/"+self.name+".exe"
        shutil.copytree(exe_filepath, "./"+self.name)

class InstallerPackager(Packager):
    def copyFilesFromUberstrikeInstallation(self):
        self.executeUberPatcher()
        UberPatcher.replaceFiles(r"C:\Program Files (x86)\Steam\steamapps\common\UberStrike" ,"./"+self.name+"/UberStrike" )

    def executeUberPatcher(self):
        try:
            output = subprocess.call(["python", "./Patcher/UberPatcher.py" ])
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
