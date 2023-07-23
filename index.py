import json
import time
import os
import shutil
import threading
from datetime import datetime


path_to_backup = "/home/weston/Mcbackup/backups"
path_to_temp = "/home/weston/Mcbackup/temp"


def getServers():
    f = open("servers.json")

    data = json.load(f)
    
    f.close()
    
    return data

def AttemptBackupDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print(e)
        
        
def cleanServerName(serverName):
    splitName = serverName.split(" ")
    cleanName = "_"
    for token in splitName:
        cleanName += token + "_"
    return cleanName

def createTopLevel(cleanServerName):
    now = datetime.now()
    os.makedirs(f"{path_to_backup}/{cleanServerName}/{now.year}/{now.month}/{now.day}")
    return f"{cleanServerName}/{now.year}/{now.month}/{now.day}"

def compressWorldFileInTempAndMove(dest):
    now = datetime.now()
    current = shutil.make_archive(f"_{now.hour}:{now.minute}_{now.month}-{now.day}-{now.year}_", "zip", f"{path_to_temp}/world")
    shutil.move(current, dest)
    shutil.rmtree(f"{path_to_temp}/world")

def minusOne(num):
    return num - 1

def compressBackupDir(path, dest, name):
    
    output = shutil.make_archive(name, "zip", path)
    shutil.move(output, dest)
    shutil.rmtree(path)
    
    
def handleDirsAndSave(cleanName):
    now = datetime.now()
    
    if(os.path.exists(f"{path_to_backup}/{cleanName}/{now.year}")):
        print("got To year")
        if(os.path.exists(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}")):
            print("got to month")
            if(os.path.exists(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")):
                print("got to day")
                compressWorldFileInTempAndMove(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
                
            elif(os.path.exists(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{minusOne(now.day)}")):
                print("compress previous day")
                compressBackupDir(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{minusOne(now.day)}", f"{path_to_backup}/{cleanName}/{now.year}/{now.month}", str(minusOne(now.day)))
                os.makedirs(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
                compressWorldFileInTempAndMove(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
                
        elif(os.path.exists(f"{path_to_backup}/{cleanName}/{now.year}/{minusOne(now.month)}")):
            print("compress previous month")
            compressBackupDir(f"{path_to_backup}/{cleanName}/{now.year}/{minusOne(now.month)}", f"{path_to_backup}/{cleanName}/{now.year}", str(minusOne(now.month)))
            os.makedirs(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
            compressWorldFileInTempAndMove(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
            
    elif(os.path.exists(f"{path_to_backup}/{cleanName}/{minusOne(now.year)}")):
        print("compress previous year")
        compressBackupDir(f"{path_to_backup}/{cleanName}/{minusOne(now.year)}", f"{path_to_backup}/{cleanName}", str(minusOne(now.year)))
        os.makedirs(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
        compressWorldFileInTempAndMove(f"{path_to_backup}/{cleanName}/{now.year}/{now.month}/{now.day}")
            
    else:
        print("No existo")
        print(f"{path_to_backup}/{cleanName}/{now.year}")
    
def getDest(serverName, serverPath):
    
    shutil.copytree(serverPath, f"{path_to_temp}/world")
    
    cleanName = cleanServerName(serverName)
    print(cleanName)
    doesTopLevelExist = os.path.exists(f"{path_to_backup}/{cleanName}")
    print(doesTopLevelExist)
    if(doesTopLevelExist):
        handleDirsAndSave(cleanName)
        
    else:
        createTopLevel(cleanName)
        handleDirsAndSave(cleanName)
        

def eventLoop():
    while True:
        servers = getServers()
        for serverOBJ in servers:
            print(serverOBJ)
            getDest(serverOBJ["serverName"], serverOBJ["serverPath"])
            


        time.sleep(60)
def upkeep():
    while True:
        eventLoopOBJ = threading.Thread(target=eventLoop)
        eventLoopOBJ.start()
        eventLoopOBJ.join()
        time.sleep(10)
        
upkeepOBJ = threading.Thread(target=upkeep)
upkeepOBJ.start()

#/home/weston/Mcbackup/backups/_S32_Create_Astral_/2023/6/23