import threading
import time
import queue

class Person(threading.Thread):
    def __init__(self, threadID, color):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.color = color

    def run(self):
        time.sleep(2)
        while(True): 
            if(self.color == currentColor):
                enter(self.threadID, self.color)
                break
            else:
                continue


def enter(id, color):
    global slots
    global blue
    global green
    global currentColor
    global currentInside
    global greenCount
    global blueCount

    semaphore.acquire()

    if(currentInside == 0):
        print(f"{currentColor} only")
    
    print(f"{color} {id}")
    currentInside += 1

    if(color == "Blue"):
        blueCount += 1
    else:
        greenCount += 1

    if(currentInside == slots or blueCount == blue or greenCount == green):
        currentInside = 0
        time.sleep(2)
        print("Empty fitting room")
        
        if(currentColor == "Blue"):
            currentColor == "Green"
        else:
            currentColor = "Blue"

    semaphore.release()

slots = int(input("Enter number of slots inside the fitting room: "))
blue = int(input("Enter number of Blues:"))
green = int(input("Enter number of Green:"))

semaphore = threading.BoundedSemaphore(slots)

currentInside = 0
blueCount = 0
greenCount = 0

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