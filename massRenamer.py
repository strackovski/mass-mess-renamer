__author__ = 'vstrackovski'

import re
import uuid
import os
import sys

print "Welcome to Vlado\'s Mass File Rename utility.\n\n" \
      "This tool will recursively iterate a directory tree \n" \
      "starting from source root, replicate the directory \n" \
      "structure in target root, and remove mess from file \n" \
      "names in the process. Folder names remain unchanged.\n\n "

print "WARNING: this tool will MOVE your files, not copy them!\n\n"

sourceRoot = raw_input("Enter source root directory: ")
if not os.path.exists(sourceRoot):
    sys.exit("Provided source path %s does not exist!" % (sourceRoot))

print "Source root directory set to %s" % (sourceRoot)

targetRoot = raw_input("Enter target root directory: ")
if not os.path.exists(targetRoot):
    sys.exit("Provided target path %s does not exist!" % (targetRoot))

print "Target root directory set to %s" % (targetRoot)

dir = sourceRoot.rstrip("\\")
dir = sourceRoot.rstrip("/")

targetDir = targetRoot.rstrip("\\")
targetDir = targetRoot.rstrip("/")
targetDir = targetDir + "\\"

def sanitizeName(name):
    newName = re.sub(' ', '_', name)
    # replace special characters
    newName = re.sub('[^A-Za-z0-9_]+', '-', newName)
    # replace repeating characters
    newName = newName[:2] +  re.sub(r'(.)\1+', r'\1', newName[2:])
    # strip and uppercase
    newName = newName.rstrip('-')
    newName = newName.rstrip('_')
    newName = newName.upper()
    # ...
    newName = re.sub('--', '', newName)
    newName = re.sub('_-', '-', newName)
    newName = re.sub('-_', '-', newName)

    return newName

fileCount = 0

for root, dirs, files in os.walk(dir):
    path = root.split('/')
    subdir = (len(path) - 1) *'---' , os.path.basename(root)
    for file in files:
        id_ = uuid.uuid4()
        uid = str(id_)[:4].upper()
        dirList = path[0].split("\\")[1:]

        if len(dirList) < 1:
            dirString = '\\'
        else:
            dirString = "\\".join(dirList) + "\\"

        if not os.path.exists(targetDir + dirString):
            os.makedirs(targetDir + dirString)

        newFileName = sanitizeName(os.path.splitext(file)[0])

        oldFile = root + "\\" + file
        print "Renaming " + oldFile + " to " + targetDir + dirString + newFileName + os.path.splitext(file)[1]

        try:
            os.rename(oldFile, targetDir + dirString + newFileName + os.path.splitext(file)[1])
            fileCount += 1
        except:
            newFileName = newFileName + "-" + uid
            print "Filename already exists, trying with filename " + newFileName + os.path.splitext(file)[1]
            os.rename(oldFile, targetDir + dirString + newFileName + os.path.splitext(file)[1])
            fileCount += 1

print "\nOperation complete: %s files renamed." % (fileCount)

