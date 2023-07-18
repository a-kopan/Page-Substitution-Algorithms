from operator import attrgetter
from random import randint
import copy
class Page:
    def __init__(self,reference,waiting_time):
        self.reference = reference
        self.waiting_time = waiting_time

page_frames = 3
reference_String = [Page(x,0) for x in [2,3,2,1,5,2,4,5,3,2,5,2]]

#1. FIFO (we remove the page that has been in physical memory the longest) 
def FIFO(page_references, memory_capacity):
    memory = []
    faults = 0
    
    for page in page_references:
        if page not in memory:
            faults += 1
            if len(memory) == memory_capacity:
                memory.pop(0)
            memory.append(page)
    
    return faults
#2. OPT (optimal - we remove the page that will not be used the longest) 
def OPT(references, frameSize):
    #create an array of elements that contain both page and waiting time
    pageArr = copy.deepcopy(references)
    faults = 0
    memory = []
    for page in pageArr:
        #check if the page is already in the memory
        if not (page.reference in [x.reference for x in memory]):
            #if memory is full
            if(len(memory)>=frameSize):
                faults+=1
                #pick the page that has the most waiting time
                max_num = max(memory,key=attrgetter('waiting_time'))
                #replace it with the page that is still in the virtual memory
                memory[memory.index(max_num)] = page
                #add the waiting time
                for page in memory:
                    page.waiting_time+=1
            #if memory is not full, just fill it up
            else:
                faults+=1
                memory.append(page)
                for page in memory:
                    page.waiting_time+=1
        else:
            #if it's in the memory, just add the waiting time
            for page in memory:
                page.waiting_time+=1
    return faults
#3. LRU (we delete the 3 that has not been referenced for the longest time) 
def LRU(references, frameSize):
    #create an array of elements that contain both page and waiting time
    pageArr = copy.deepcopy(references)
    faults = 0
    memory = []
    for page in pageArr:
        #check if the page is already in the memory
        if not (page.reference in [x.reference for x in memory]):
            faults+=1
            #if memory is full
            if(len(memory)>=frameSize):
                #add the waiting time
                for pageH in memory:
                    pageH.waiting_time+=1
                #pick the page that has the most waiting time
                max_num = max(memory,key=attrgetter('waiting_time'))
                #replace it with the page that is still in the virtual memory
                #memory[memory.index(max_num)] = Page(page.reference,0)
                memory[memory.index(max_num)] = page
            #if memory is not full, just fill it up
            else:
                memory.append(page)
                for pageH in memory:
                    pageH.waiting_time+=1
        else:
            #if it's in the memory, just add the waiting time
            for pageHold in memory:
                pageHold.waiting_time+=1
                
            #if the page is in the memory, then it was just referenced, so set it's waiting time to 0
            index = 0
            for x in memory:
                if(x.reference == page.reference):
                    index = memory.index(x)
            memory[index].waiting_time = 0
            
    return faults
#4. approximated LRU (second chance algorithm) 
def aLRU(references, frameSize):
    faults = 0
    referenceString = [x.reference for x in references].copy()
    #a variable that holds 'the next in line' to check if it can be kicked out
    current = 0
    #physicall memory (will hold referenced pages)
    memory = []
    #reference bit array that holds reference bits for each element (initially fill with 0's)
    refBits = [0 for x in range(0,frameSize)]
    for ref in referenceString:
        #if the ref is in the memory, change its refBit to 1 (in case it's 0)
        if ref in memory:
            i = memory.index(ref)
            #if the bit is 0, change to 1
            if(not refBits[i]):
                refBits[i]+=1
        #if the ref is not in the memory
        else:
            faults+=1
            #if the memory is full
            if(len(memory)==frameSize):
                #start from startFrom integer and progress through the whole array
                while True:
                    #check if current is out of bounds, if so then reset it to the beggining
                    if(current==frameSize):
                        current = 0
                    #break once i meet the reference with refBit==0
                    if(refBits[current]==0):
                        memory.pop(current)
                        memory.insert(current,ref)
                        current+=1
                        break
                    else:
                        refBits[current] = 0
                        current+=1
            #if the memory isnt full
            else:
                memory.append(ref)
    return faults
#5. RAND (we remove a random page) 
def RAND(references, frameSize):
    memory = []
    faults = 0
    for ref in references:
        if not (ref in memory):
            faults+=1
            if(len(memory)==frameSize):
                indexToDelete = randint(0,frameSize-1)
                memory.pop(indexToDelete)
                memory.insert(indexToDelete,ref)
            else:
                memory.append(ref)
    return faults
            
print("FIFO: ", FIFO(reference_String, page_frames))
print("OPT: ", OPT(reference_String, page_frames))
print("LRU: ", LRU(reference_String, page_frames))
print("aLRU: ", aLRU(reference_String, page_frames))
print("RAND: ", RAND(reference_String, page_frames))