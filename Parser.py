__author__ = 'oxsc'

# Open the file for reading
f = open("C:\Users\oxsc\Desktop\Log.txt", "r")

currLevel = 0

# Iterate over the lines in the file
for line in f:
    if "|" in line:
        splitLine = line.split("|")
        if splitLine[1] == "METHOD_ENTRY":
            currLevel += 1
            print currLevel * "\t" + splitLine[4]
        if splitLine[1] == "CONSTRUCTOR_ENTRY":
            currLevel += 1
            print currLevel * "\t" + splitLine[3]
        if splitLine[1] == "METHOD_EXIT":
            currLevel -= 1
        if splitLine[1] == "CONSTRUCTOR_EXIT":
            currLevel -= 1

