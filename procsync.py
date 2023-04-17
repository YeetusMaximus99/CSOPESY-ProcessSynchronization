import threading
import time
import queue

class Person(threading.Thread):
    def __init__(self, threadID, color):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.color = color

    def run(self):
        enter(self.threadID, self.color)

def enter(id, color):
    global slots
    global blue
    global green
    global bMax
    global gMax
    global currentColor
    global currentInside
    global greenCount
    global blueCount
    global oldMsg
    global msgHolder

    semaphore.acquire()

    if (currentInside == 0):
        if (oldMsg != str(currentColor) + " only"):
            print(f"{currentColor} only")
            oldMsg = str(currentColor) + " only"
        else:
            for msg in msgHolder:
                print(msg)
            msgHolder = []
            
    if (currentColor == "Blue" and blueCount <= bMax):
        print(f"{currentColor} {blueCount} enters    (currently inside:{currentInside+1})")
        msgHolder.append(f"{currentColor} {blueCount} exits")
        blueCount += 1
        currentInside += 1
    elif (currentColor == "Green" and greenCount <= gMax):
        print(f"{currentColor} {greenCount} enters    (currently inside:{currentInside+1})")
        msgHolder.append(f"{currentColor} {greenCount} exits")
        greenCount += 1
        currentInside += 1
    else:
        # at this point slots (semaphore._value) is back to n, meaning no threads are acquiring a lock
        # print(f"slots = {semaphore._value}")
        for msg in msgHolder:
            print(msg)
        msgHolder = []
        print("----Empty Fitting room.----  (currently inside:0)\n")
        # print(f"slots = {semaphore._value}")
        if currentColor == "Blue":
            currentColor = "Green"
            if (oldMsg != str(currentColor) + " only"):
                print(f"{currentColor} only")
                oldMsg = str(currentColor) + " only"
            else:
                for msg in msgHolder:
                    print(msg)
                msgHolder = []
            print(f"{currentColor} {greenCount} enters    (currently inside:{currentInside+1})")
            msgHolder.append(f"{currentColor} {greenCount} exits")
            greenCount += 1
        elif currentColor == "Green":
            currentColor = "Blue"
            if (oldMsg != str(currentColor) + " only"):
                print(f"{currentColor} only")
                oldMsg = str(currentColor) + " only"
            else:
                for msg in msgHolder:
                    print(msg)
                msgHolder = []
            print(f"{currentColor} {blueCount} enters    (currently inside:{currentInside+1})")
            msgHolder.append(f"{currentColor} {blueCount} exits")
            blueCount += 1
    
    if (currentColor == "Blue"):
        counter2 = blue
    else:
        counter2 = green
        
    if (currentInside == slots or currentInside >= counter2):
        currentInside = 0
        if (currentColor == "Blue" and greenCount-1 != gMax):
            for msg in msgHolder:
                print(msg)
            msgHolder = []
            print("----Empty Fitting room.----  (currently inside:0)\n") 
            currentColor = "Green"
        elif(currentColor == "Green" and blueCount-1 != bMax):
            for msg in msgHolder:
                print(msg)
            msgHolder = []
            print("----Empty Fitting room.----  (currently inside:0)\n") 
            currentColor = "Blue"
    time.sleep(2)
    semaphore.release()

slots = int(input("Enter number of slots inside the fitting room: "))
blue = int(input("Enter number of Blues:"))
green = int(input("Enter number of Green:"))

semaphore = threading.BoundedSemaphore(value = slots)

bMax = blue
gMax = green
currentInside = 0
oldMsg = ""
msgHolder = []
blueCount = 1
greenCount = 1

people = []

if(blue > green):
    currentColor = "Blue"
else:
    currentColor = "Green"

blue_threads = [Person(str(i), "Blue") for i in range(1, blue + 1)]
green_threads = [Person(str(i), "Green") for i in range(1, green + 1)]

for thread in blue_threads + green_threads:
    thread.start()

for thread in blue_threads + green_threads:
    thread.join()

while(True):
    if (threading.active_count() == 1):
        for msg in msgHolder:
            print(msg)
        msgHolder = []
        print("----Empty Fitting room.----  (currently inside:0)")
        break

