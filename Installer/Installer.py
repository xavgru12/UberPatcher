from re import S
import sys
sys.path.append(r"C:\Users\Xaver\Documents\Uber\Skripte\UberPatcher")
import UberPatcher
import os

def main():
    print("Checking for steam installation...")
    steam_path=UberPatcher.getSteamPath()
    print("Starting to install UberStrike in steam...")
    if os.path.isdir("./UberStrike"):
        UberPatcher.replaceFiles("./UberStrike", steam_path+"/steamapps/common/UberStrike")
        print("UberStrike was successfully installed in "+steam_path+"/steamapps/common/UberStrike/UberStrike.exe")
    else:
        print("Please run the Installer in the directory where ./UberStrike folder is in order to install UberStrike.")
    input()
    
    



if __name__ == "__main__":
    main()

