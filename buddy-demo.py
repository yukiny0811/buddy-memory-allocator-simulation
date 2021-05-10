
#
# buddy-demo.py
# buddy memory allocator simulation
#
# Created by Yuki Kuwashima on 2021/05/09
# Copyright © 2021 Yuki Kuwashima. All rights reserved.
#

# python3 buddy-demo.py

blocks = "0"

# 0 -> 64blocks
# 2 -> 32blocks
# 4 -> 16blocks
# 6 -> 8blocks
# 8 -> 4blocks
# a -> 2blocks
# c -> 1blocks

def neededBlocksNum(needed):
    # needed must be int
    if needed <= 1:
        return 0xc
    elif needed <= 2:
        return 0xa
    elif needed <= 4:
        return 0x8
    elif needed <= 8:
        return 0x6
    elif needed <= 16:
        return 0x4
    elif needed <= 32:
        return 0x2
    elif needed <= 64:
        return 0x0
        
def getNumFromHex(char):
    if char == "0":
        return 64
    elif char == "1":
        return 64
    elif char == "2":
        return 32
    elif char == "3":
        return 32
    elif char == "4":
        return 16
    elif char == "5":
        return 16
    elif char == "6":
        return 8
    elif char == "7":
        return 8
    elif char == "8":
        return 4
    elif char == "9":
        return 4
    elif char == "a":
        return 2
    elif char == "b":
        return 2
    elif char == "c":
        return 1
    elif char == "d":
        return 1
        

def convertToDashes(blocksString):
    outputString = "|" + blocksString
    outputString = outputString.replace("0", "----------------------------------------------------------------|")
    outputString = outputString.replace("1", "################################################################|")
    outputString = outputString.replace("2", "--------------------------------|")
    outputString = outputString.replace("3", "################################|")
    outputString = outputString.replace("4", "----------------|")
    outputString = outputString.replace("5", "################|")
    outputString = outputString.replace("6", "--------|")
    outputString = outputString.replace("7", "########|")
    outputString = outputString.replace("8", "----|")
    outputString = outputString.replace("9", "####|")
    outputString = outputString.replace("a", "--|")
    outputString = outputString.replace("b", "##|")
    outputString = outputString.replace("c", "-|")
    outputString = outputString.replace("d", "#|")
    return outputString

def getIndexOfChunk(dashString, num):
    if num == 0:
        return 0
    dashList = list(dashString)
    nowCount = 0
    dashCount = 0
    for i in range(len(dashList)):
        if dashList[i] == "|":
            dashCount += 1
        else:
            nowCount += 1
        if nowCount == num:
            return dashCount
    return 0
    
def isBlockStartOfAChunk(dashString, num):
    if num == 0:
        return True
    dashList = list(dashString)
    nowCount = 0
    for i in range(len(dashList)):
        if dashList[i] != "|":
            nowCount += 1
        if nowCount == num + 1:
            if dashList[i-1] == "|" and dashList[i] == "#":
                return True
            else:
                return False
    return False
    

while True:
    print("How many blocks do you want to allocate/free?")
    inputs = input().split(" ")
    if len(inputs) != 2:
        print("enexpected command... finishing.")
        break
    if inputs[0] != 'a' and inputs[0] != 'f' and inputs[0] != 'q':
        print("enexpected command... finishing.")
        break
    if inputs[0] == 'q':
        break
    number = 0
    try:
        number = int(inputs[1])
    except:
        print("enexpected command... finishing.")
        break
    if inputs[0] == "a":
        blocksList = list(blocks)
        count = 0
        while count < len(blocksList):
            int16B = int(format(int(blocksList[count], 16), "#x"), 0)
            needed = neededBlocksNum(number)
            if int16B % 0x2 == 0 and int16B < needed:
                total = 0
                for temp in blocksList[0:count]:
                    total += getNumFromHex(temp)
                print("splitting " + str(total) + "/" + str(getNumFromHex(blocksList[count])))
                blocksList[count] = format(int16B + 0x2, "x") + format(int16B + 0x2, "x")
                blocks = "".join(blocksList)
                blocksList = list(blocks)
                count = 0
                continue
            if int16B == needed:
                total = 0
                for temp in blocksList[0:count]:
                    total += getNumFromHex(temp)
                print("Blocks " + str(total) + "-" + str(total + getNumFromHex(format(int16B, "x"))) + " allocated:")
                blocksList[count] = format(int16B + 0x1, "x")
                break
            count += 1
            
        blocks = "".join(blocksList)
    if inputs[0] == "f":
        if isBlockStartOfAChunk(convertToDashes(blocks), number):
            index = getIndexOfChunk(convertToDashes(blocks), number)
            blocksList = list(blocks)
            blocksList[index] = format(int(format(int(blocksList[index], 16), "#x"), 0) - 0x1, "x")
            blocks = "".join(blocksList)
            
            blocksList = list(blocks)
            count = 1
            while count < len(blocksList):
                if blocksList[count-1] == blocksList[count] and int(blocksList[count-1], 16) % 2 == 0:
                    total = 0
                    for temp in blocksList[0:count]:
                        total += getNumFromHex(temp)
                    totalMinus = 0
                    for temp in blocksList[0:count-1]:
                        totalMinus += getNumFromHex(temp)
                    print("merging " + str(totalMinus) + "/" + str(getNumFromHex(blocksList[count])) + " and " + str(total) + "/" + str(getNumFromHex(blocksList[count])))
                    blocksList[count] = ""
                    count = 1
                    blocksList[count-1] = format(int(format(int(blocksList[count-1], 16), "#x"), 0) - 0x2, "x")
                    blocks = "".join(blocksList)
                    blocksList = list(blocks)
                    continue
                count += 1
            
            blocks = "".join(blocksList)
    outputString = convertToDashes(blocks)
    
    
    print(outputString)
    

