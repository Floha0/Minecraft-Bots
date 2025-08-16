from system.lib import minescript as m
import time
import pyautogui
import keyboard
import sys

pos = [(817, 355), (851, 356), (887, 355), (923, 354), (961, 354), (996, 355), (1032, 355), (1066, 356), (1104, 354), (817, 388), (851, 389), (885, 391), (924, 389), (959, 391), (996, 391), (1030, 389), (1069, 389), (1106, 393), (816, 426), (853, 423), (888, 426), (925, 425), (962, 428), (998, 427), (1034, 430), (1069, 426), (1106, 430), (816, 459), (851, 460), (888, 463), (924, 464), (959, 463), (998, 463), (1032, 463), (1067, 463), (1106, 462), (812, 495), (850, 496), (888, 497), (925, 499), (961, 501), (996, 501), (1032, 501), (1067, 500), (1103, 499), (816, 532), (850, 532), (886, 534), (921, 534), (960, 536), (995, 535), (1031, 535), (1069, 535), (1105, 535)]
columnPos = [15136, -55231]

def pullItems():
    def chestWorth():
        while m.container_get_items() == None:
            time.sleep(0.02)
        quantity_log = 0
        quantity_cocoa = 0
        for item in m.container_get_items():
            if item.item == 'minecraft:jungle_log' and item.slot < 54 and item.count == 64:
                quantity_log += 1
            elif item.item == 'minecraft:cocoa_beans' and item.slot < 54 and item.count == 64:
                quantity_cocoa += 1
        if quantity_log >= 1 and quantity_cocoa >= 4:
            return True
        return False
    
    def pull():
        container = m.container_get_items()
        jungle_log_items = [item for item in container if "jungle_log" in item.item and item.slot < 54 and item.count == 64]
        cocoa_items = [item for item in container if "cocoa" in item.item and item.slot < 54 and item.count == 64]

        keyboard.press("shift")
        time.sleep(0.02)
        pyautogui.moveTo(pos[jungle_log_items[0].slot])
        time.sleep(0.02)
        pyautogui.click()
        time.sleep(0.05)
        for i in range(4):
            pyautogui.moveTo(pos[cocoa_items[i].slot])
            time.sleep(0.02)
            pyautogui.click()
            time.sleep(0.05)
        time.sleep(0.1)
        keyboard.release("shift")

    chestIndex = 0
    while True:
        m.execute("/chest")
        time.sleep(1.5)
        pyautogui.moveTo(pos[chestIndex])
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(1.5)
        if chestWorth():
            break
        
        chestIndex += 1
        time.sleep(0.1)
        if chestIndex > 4:
            print("exiting...")
            sys.exit()
    
    pull()

def getToLogSpot():
    def findSuitableLane():
        firstz = int(m.player_position()[2])
        while True:
            m.player_press_right(True)
            time.sleep(0.5)

            while (firstz - int(m.player_position()[2])) % 3:
                time.sleep(0.01)
            
            m.player_press_right(False)
            time.sleep(0.1)
            print(m.player_get_targeted_block(4))

            if m.player_get_targeted_block(4) is None:
                print("None")
                break

    def walkThroughLane():
        m.player_press_forward(True)
        print()
        while True:
            time.sleep(0.02)
            if(m.player_get_targeted_block(3) is not None):
                break
        m.player_press_forward(False)

    m.execute("/is go farm")
    time.sleep(2)
    m.player_set_orientation(90, 10.8)
    time.sleep(0.05)
    keyboard.press("shift")
    time.sleep(0.1)
    keyboard.release("shift")
    time.sleep(0.1)
    findSuitableLane()
    walkThroughLane()

    global columnPos
    columnPos = [int(m.player_position()[0]), int(m.player_position()[2])]

def placeLogs():
    # replace hand with jungle log, if there is no break the code
    jungle_log_items = [item for item in m.player_inventory() if "jungle_log" in item.item and item.slot < 9 and item.count == 64]
    if jungle_log_items == []:
        return
    m.player_inventory_select_slot(jungle_log_items[0].slot)
    time.sleep(0.5)

    while True:
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("space")
        time.sleep(0.1)
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("space")
        time.sleep(0.1)

        m.player_set_orientation(90,90)
        time.sleep(0.05)

        
        keyboard.press("space")
        time.sleep(0.02)
        
        
        # fly and place logs
        tmp_log_count = 0
        broken_loop = 0
        while True:
            pyautogui.click(button="right")
            print("click")
            time.sleep(0.01)
            main_hand_item = m.player_hand_items().main_hand
            if main_hand_item is None:
                keyboard.release("space")
                time.sleep(0.1)
                keyboard.press("space")
                time.sleep(0.1)
                keyboard.release("space")
                time.sleep(0.1)
                keyboard.press("space")
                time.sleep(0.1)
                keyboard.release("space")
                time.sleep(1) 
                return
            if main_hand_item.count == tmp_log_count:
                broken_loop += 1
            else:
                broken_loop = 0
            print(broken_loop)
            tmp_log_count = main_hand_item.count

            if broken_loop >= 3:
                break
            
def getDown(direction):
    # 1- backwards 2- right 3- forward 4- left
    time.sleep(0.5)
    
    m.player_set_orientation(90, m.player_orientation()[1])
    match direction:
        case 0:
            m.player_press_backward(True)
        case 1:
            m.player_press_right(True)
        case 2:
            m.player_press_forward(True)
        case 3:
            m.player_press_left(True)
        case _:
            pass
    oldx,oldy,oldz = m.player_position()
    oldx,oldy,oldz = int(oldx),int(oldy),int(oldz)
    while True:
        match direction:
            case 0:
                # x is increasing
                newx = int(m.player_position()[0] + 0.1)
                if newx != oldx:
                    time.sleep(0.1)
                    m.player_press_backward(False)
                    break
            case 1:
                # z is decrasing
                newz = int(m.player_position()[2] - 0.1)
                if newz != oldz:
                    time.sleep(0.1)
                    m.player_press_right(False)
                    break
            case 2:
                # x is decrasing
                newx = int(m.player_position()[0] - 0.15)
                if newx != oldx:
                    time.sleep(0.03)
                    m.player_press_forward(False)
                    break
            case 3:
                # z is increasing
                newz = int(m.player_position()[2] + 0.15)
                if newz != oldz:
                    time.sleep(0.1)
                    m.player_press_left(False)
                    break
            case _:
                pass
        time.sleep(0.02)
    
    print(oldy)
    while oldy - 64 != int(m.player_position()[1]):
        time.sleep(0.02)
    
    time.sleep(0.1)
    print("fix")
    match direction:
        case 0:
            pass
        case 1:
            while True:
                if int(m.player_position()[0]) > columnPos[0]:
                    m.player_press_forward(True)
                    time.sleep(0.02)
                    m.player_press_forward(False)
                    time.sleep(1)
                elif int(m.player_position()[0]) < columnPos[0]:
                    m.player_press_backward(True)
                    time.sleep(0.02)
                    m.player_press_backward(False)
                    time.sleep(1)
                else:
                    break
        case 2:
            while True:
                if int(m.player_position()[2]) > columnPos[1]:
                    m.player_press_right(True)
                    time.sleep(0.02)
                    m.player_press_right(False)
                    time.sleep(1)
                elif int(m.player_position()[2]) < columnPos[1]:
                    m.player_press_left(True)
                    time.sleep(0.02)
                    m.player_press_left(False)
                    time.sleep(1)
                else:
                    break
        case 3:
            while True:
                print(int(m.player_position()[0]))
                print(columnPos[0])
                if int(m.player_position()[0]) > columnPos[0]:
                    m.player_press_forward(True)
                    time.sleep(0.02)
                    m.player_press_forward(False)
                    time.sleep(1)
                elif int(m.player_position()[0]) < columnPos[0]:
                    m.player_press_backward(True)
                    time.sleep(0.02)
                    m.player_press_backward(False)
                    time.sleep(1)
                else:
                    break
        case _:
            pass
        
    print("at down")

def placeCocoas(direction):
    time.sleep(0.5)
    cocoa_items = [item for item in m.player_inventory() if "cocoa" in item.item and item.slot < 9 and item.count == 64]
    if cocoa_items == []:
        return
    m.player_inventory_select_slot(cocoa_items[0].slot)
    time.sleep(0.5)
            
    match int(direction):
        case 0:
            m.player_set_orientation(90,45)
        case 1:
            m.player_set_orientation(0.1,45)
        case 2:
            m.player_set_orientation(-90,45)
        case 3:
            m.player_set_orientation(179,45)
        case _:
            pass

    time.sleep(0.02)
    m.player_press_use(True)
    time.sleep(0.02)
    m.player_press_forward(True)
    time.sleep(0.5)
    m.player_press_forward(False)
    time.sleep(0.5)
    m.player_press_backward(True)
    time.sleep(0.1)
    m.player_press_backward(False)
    time.sleep(0.1)
    m.player_press_use(False)
    time.sleep(0.02)

    
    m.player_set_orientation(m.player_orientation()[0],70)
    time.sleep(0.1)

    oldy = int(m.player_position()[1])


    # fly and place logs
    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(0.1)
    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(0.1)

    keyboard.press("space")
    time.sleep(0.02)

    while True:
        if m.player_get_targeted_block(4) is None:
            keyboard.press("ctrl")
            time.sleep(0.1)
            keyboard.press("q")
            time.sleep(0.02)
            keyboard.release("q")
            time.sleep(0.1)
            keyboard.release("ctrl")
            break

        pyautogui.click(button="right", interval=0)

    m.player_press_forward(True)
    time.sleep(0.15)
    m.player_press_forward(False)
    time.sleep(0.5)
    keyboard.release("space")
    time.sleep(0.1)
    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(0.1)
    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(1)



while True:
    pullItems()
    getToLogSpot()
    placeLogs()
    for i in range(4):
        getDown(i)
        placeCocoas(i)
print("done")
