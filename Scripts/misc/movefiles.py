import os
import shutil
import time

baseDir = os.getenv("HOME") + "/BlockchainResearch"
source = baseDir + "/Data/EtherscanData/Scraping/Tokens"
dest = baseDir + "/Data/TokenData"

for tokenDir in os.listdir(source):
    if tokenDir != ".DS_Store":
        
        if not os.path.exists(dest+"/"+tokenDir):
            os.mkdir(dest+"/"+tokenDir)

        files = os.listdir(source + "/" + tokenDir)
        for f in files:
            shutil.move(source+"/"+tokenDir+"/"+f, dest+"/"+tokenDir)