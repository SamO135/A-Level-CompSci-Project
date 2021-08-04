from data.settings import *

"""BINARY SEARCH"""     """BINARY SEARCH"""     """BINARY SEARCH"""

def binarySearch(List,item):
    first = 0
    last = len(List)-1
    done = False

    while first <= last and not done:
        mid = (first+last)//2

        if List[mid][0] == item:
            done = True
        else:
            if str(List[mid][0]) > str(item):
                last = mid - 1
            else:
                first = mid + 1
    
    return List[mid][1], List[mid][2], List[mid][3], List[mid][4]





def get_image_coords(img_name):
    with open (XML_FILE, "r") as imgFile:
        allSpritePos = []
        for line in imgFile:            #Loops through each line
            lineList = line.split('"')      #splits at every "

            for item in lineList:
                index = lineList.index(item)
                if ".png" not in item:  #if not the image/file name
                    try:
                        lineList[index] = int(lineList[index])  #try to cast to int
                    except:
                        lineList[index] = None  #If can't cast to int and it's not the image name, its a bit I want to get rid of so set it to 'None', because
            for item in lineList:               #if i popped it, the item would disappear from list and each item after that one would move along 1 space to the left,
                if item == None:                #then the counter in incremented and skips over a value that hasn't been checked (the next value). (this is used in method 2)
                    lineList.pop(lineList.index(item))
                
            allSpritePos.append(lineList)
        allSpritePos.pop(0)
            
        
    return binarySearch(allSpritePos, img_name)



"""BUBBLE SORT"""       """BUBBLE SORT"""       """BUBBLE SORT"""


##def bubbleSort(arr):
##    Sorted = False
##    endPoint = 1
##    swaps = 0
##
##    while not Sorted:
##        count = 0
##        for pos in range(0, len(arr)-endPoint):
##            if arr[pos] > arr[pos+1]:
##                temp = arr[pos]
##                arr[pos] = arr[pos+1]
##                arr[pos+1] = temp
##                swaps += 1
##
##        endPoint += 1
##        if len(arr)-endPoint == 0:
##            Sorted = True
##
##    #print("Number of swaps:", swaps)
##    #return arr




"""MERGE SORT"""        """MERGE SORT"""        """MERGE SORT"""


# ITSO = Item To Sort On
def merge(arr, left, mid, right, ITSO):
    n1 = round(mid - left + 1)
    n2 = round(right - mid)

    LEFT = [0 for i in range(0, n1)]
    RIGHT = [0 for i in range(0, n2)]

    for i in range(0 , n1):
        LEFT[i] = arr[left + i]
            
    for j in range(0 , n2):
        RIGHT[j] = arr[mid + 1 + j]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if LEFT[i][ITSO] >= RIGHT[j][ITSO]: #ITSO = Item To Sort On, Uses this value in
                arr[k] = LEFT[i]            #the 2D array to base the sorting around
                i += 1
        else:
                arr[k] = RIGHT[j]
                j += 1
        k += 1

    while i < n1:
        arr[k] = LEFT[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = RIGHT[j]
        j += 1
        k += 1

def mergeSort(arr, left, right, ITSO):
    if left < right:

        mid = round((left+(right-1))/2)

        mergeSort(arr, left, mid, ITSO)
        mergeSort(arr, mid+1, right, ITSO)
        merge(arr, left, mid, right, ITSO)
    return arr
