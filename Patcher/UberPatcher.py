from io import BytesIO
from urllib.request import urlopen
from xmlrpc.client import Boolean
from zipfile import ZipFile

#steam installation finder
import sys
import winreg

#uber path finder
import os

#sys.tracebacklimit=0

#replace files
import shutil

#argparser with parseArguments function
import argparse

def downloadPatchfiles(zipurl):
    #zipurl = 'http://uberforever.eu/patcher.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            test= zfile.extractall('/tmpuber')
            #for debug
            #print(test, zfile)
    patchname= zipurl.split("/")[-1].replace(".zip","") #get patchname from zipurl, eg: 'http://uberforever.eu/patcher.zip' -> patcher
    print("Patchname: ", patchname)
    patcher_dir = '/tmpuber/'+patchname+'/patchfiles'
    return patcher_dir

def getSteamPath():

    try: 
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Valve\Steam")

    try:
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        steam_path = None
        print(sys.exc_info())
        return None

    #for debug
    #print(steam_path[0])


    winreg.CloseKey(hkey)

    return steam_path[0]


def getUberInstallationPath(steam_path):
    if not os.path.isdir(steam_path):
        return None

    uber_path=steam_path+"/steamapps/common/UberStrike"
    if os.path.isfile(uber_path+"/UberStrike.exe"):
        return uber_path
    
    libraries_file = steam_path+"/steamapps/libraryfolders.vdf"
    library_paths=[]
    if os.path.isfile(libraries_file):
        with open(libraries_file, 'r') as file:
            for line in file:
                if "path" in line:
                    lib = line.replace("\"path\"","").strip().replace("\"","")
                    library_paths.append(lib)
                    print(lib)

    for path in library_paths:
        check_path=path+"/UberStrike"
        if os.path.isdir(check_path):
            check_path=uber_path
            return uber_path

    
    return None

def replaceFiles(root_src_dir, root_dst_dir):

    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir) 

def cleanupCreatedFiles(folder):
    folderToDelete= os.path.dirname(os.path.dirname(folder))
    shutil.rmtree(folderToDelete)  #since files were moved, only need to delete folders

def parseArguments():
    parser = argparse.ArgumentParser(description='Patching uber files.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--testserver','-ts', help=argparse.SUPPRESS, action='store_true') #store_true will be true, if -ts is written or not
    group.add_argument('--source','-src', help=argparse.SUPPRESS) #arparse.suppress will not show this in help message
    args = parser.parse_args()
    if not args.testserver and not args.source:
        return False

    if args.testserver:
        return True

    if args.source:
        return str(args.source)

def main():
    print("Finding uber steam installation...")
    steam_path=getSteamPath()
    uber_path=getUberInstallationPath(steam_path)
    
    if uber_path is None:
        raise FileExistsError("Could not find uber installation")
    checkParser = parseArguments()
 
    if type(checkParser) is Boolean:
        print("Downloading files...")
        if checkParser is False:
            zipurl = 'http://uberforever.eu/patcher.zip'
        elif checkParser is True:
            zipurl = 'http://uberforever.eu/testserverpatcher.zip'
        patcher_dir=downloadPatchfiles(zipurl)
    else:
        patcher_dir=checkParser  # <path>\patcher_dir\patcher/patcher/patchfiles, subdir of patchfiles is UberStrike_Data
     


    print("Patching files...")
    replaceFiles(patcher_dir, uber_path)
    print("Cleaning up...")
    if type(checkParser) is Boolean:
        cleanupCreatedFiles(patcher_dir)
    print("DONE. Patcher has been installed. You can run the game without patcher from now on.")
    input()


if __name__ == "__main__":
    main()
    