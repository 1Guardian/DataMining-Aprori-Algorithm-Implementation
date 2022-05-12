import numpy as np
import itertools
from itertools import combinations

###########################################################
#
# Configuration values for the calculation.
#
###########################################################
minsup = 3
minconf = 0.9

possible_Vals = ('a','b','c','d','e')
origin = possible_Vals

dictionary = {1: ('a','b','d','e'), 2: ('b','c','d'), 3: ('a','b','d','e'), 4: ('a','c','d','e'), 5:('b','c','d','e'), 6:('b','d','e'), 7:('c','d'), 8:('a','b','c'), 9:('a','d','e'), 10:('b','d')}

###########################################################
#
# Code and functions for generating the aprori calculations
#
###########################################################
currRound = 1
possibleCounts = np.zeros(len(possible_Vals))
repeat = 2
passdict = dict()

#funciton for combining the arrays
def combineArrays(input, origin, cycle):

    #new array to hold
    newArr=[]
    
    #handle the edge case
    if (cycle == 0):
        for i, ele in enumerate(input):
            j = i+1
            while(j < len(input)):
                newArr.append([ele, input[j]])
                j+=1

        return newArr

    #handle all other cycles
    else: 
        for i, ele in enumerate(input):
            j = i+1

            passed = True

            while(j < len(input)):
                countCycle = cycle
                while(countCycle != 0):
                    if (input[j][countCycle-1] != ele[countCycle-1]):
                        passed = False
                    countCycle -= 1
                if (passed == True):
                    tmp = ele
                    newArr.append(list(sorted(set(np.concatenate((tmp, input[j]), axis=0)))))
                j+=1
        
        return newArr

#function to find sub arrays
def find_subarray(first_arr, second_arr):
    first_ptr = 0
    second_ptr = 0

    first_arr_len = len(first_arr)
    second_arr_len = second_arr.size

    continuefg = False
    completefg = False

    if second_arr_len == 1:
        for val in first_arr:
            if val == second_arr:
                return True
        return False

    elif second_arr_len > 1:
        for val in second_arr:
            continuefg = False
            for otherval in first_arr:
                if val == otherval:
                    continuefg = True
                    
            if continuefg == False:
                return False
        return True

    return False


#_______MAIN()_____________
currRound = 0

previousRun = []
previousZero = []
previousRuns = []

while True:
    #get each round
    for i, val in enumerate(possible_Vals):
        for x in dictionary:
            if find_subarray(dictionary[x], np.asarray(val)):
                possibleCounts[i] += 1

    finished = False

    #print the original pass
    print("==================[ Old ]======================")
    for i, (x, y) in enumerate(zip(possible_Vals, possibleCounts)):
        print(x, end=" : ")
        print(y)
    print("===============================================\n")

    #remove minsup sub elements
    temporaryArray_Vals = []
    temporaryArray_Count = []

    for i, (x, y) in enumerate(zip(possible_Vals, possibleCounts)):
            if y >= minsup:
                temporaryArray_Vals.append(x)
                temporaryArray_Count.append(y)

    possible_Vals = temporaryArray_Vals
    possibleCounts = temporaryArray_Count

    #remove non-set elements
    temporaryArray_Vals = []
    temporaryArray_Count = []

    for i, (x, y) in enumerate(zip(possible_Vals, possibleCounts)):
            yasSet = set(x)
            yasSet = list(yasSet)
            if(len(yasSet) == len(x)):
                temporaryArray_Vals.append(x)
                temporaryArray_Count.append(y)

    possible_Vals = temporaryArray_Vals
    possibleCounts = temporaryArray_Count

    #print the kept pass
    print("=================[ Kept ]======================")
    for i, (x, y) in enumerate(zip(possible_Vals, possibleCounts)):
        print(x, end=" : ")
        print(y)
    print("===============================================\n")

    #create a previous point in the dictionary list
    for i, (x, y) in enumerate(zip(possible_Vals, possibleCounts)):
        passdict.update( {tuple(x) : y} )
    previousRuns.append(passdict)

    previousRun = possible_Vals
    previousZero = possibleCounts

    possible_Vals = combineArrays(possible_Vals, origin, currRound)

    if(len(possible_Vals) == 0):

        print("===============[ Final Results ]===============")

        #get all possible rules    
        for array, zeros in zip(previousRun, previousZero):
            list_combinations = list()
            
            for n in range(len(array) + 1):
                    list_combinations += list(combinations(array, n))

            for i, x in enumerate(list_combinations):
                list_combinations[i] = list(set(x))

            output = set(map(lambda x: tuple(sorted(x)),list_combinations))

            for i, val in enumerate(list(output)):
                if val in passdict:
                    if val is val:
                        holdValue = zeros/passdict[val]
                        if holdValue > minconf:
                            print(val, end=": ")
                            print(str(zeros) + "/" + str(passdict[val]) + "* 100", end=" = " )
                            print(holdValue * 100)
        exit()
        

    #flatten the new arrays
    newarr = []
    for x in possible_Vals:
            xnum = (np.array(x))
            newarr.append(xnum.flatten())
    
    possible_Vals = newarr

    #reset possibleCounts based on length 
    #of possible_Vals left
    realLength = 0
    for var in possible_Vals:
        realLength += 1
    possibleCounts = np.zeros(realLength)

    currRound += 1
