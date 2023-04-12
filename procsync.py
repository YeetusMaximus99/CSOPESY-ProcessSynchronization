import threading
class FittingRoom:
    def __init__(self, n,blue,green):
        self.slots = n
        self.blue_count = 0
        self.green_count = 0
        self.lock = threading.Lock()
        self.blue_condition = threading.Condition(self.lock)
        self.green_condition = threading.Condition(self.lock)
        self.current_color = None
        self.current_count = 0
        self.total_green = green
        self.total_blue = blue
    def enter(self,color):
        with self.lock:
            if self.current_color is None:
                self.current_color = color
                print(f"{color} only")
            if self.current_color == "blue" and self.green_count == 0:
                while self.current_color != None and self.green_count > 0:
                    
                    self.blue_condition.wait()
                self.blue_count += 1
                self.total_blue -=1
            elif self.current_color == "green" and self.blue_count ==0:
                while self.current_color != None and self.blue_count > 0:
                        self.green_condition.wait()
                self.green_count += 1
                self.total_green -=1

                    
            
            self.current_count += 1
            print(f"{threading.get_ident()} - {color}")
            if self.current_count == self.slots or (self.total_green == 0 and self.current_color == 'green') or (self.total_blue == 0 and self.current_color == 'blue'):  
                self.current_color = None
                self.current_count = 0
                self.blue_count = 0
                self.green_count = 0
                self.blue_condition.notify_all()
                self.green_condition.notify_all()
                
                print("Empty fitting room.") 
        

def run(color, count, fitting_room):
    for i in range(count):
        fitting_room.enter(color)
def main():
    slots = int(input("Enter number of slots inside the fitting room: "))
    blue = int(input("Enter number of Blues:"))
    green = int(input("Enter number of Green:"))
    fitting_room = FittingRoom(slots,blue,green)
    blue_threads = [threading.Thread(target=run, args=("blue", 1, fitting_room)) for i in range(blue)]
    green_threads = [threading.Thread(target=run, args=("green", 1, fitting_room)) for i in range(green)]
    threads = blue_threads + green_threads
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
if __name__ == '__main__':
    main()