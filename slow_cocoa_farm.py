from system.lib import minescript as m
import time
import pyautogui
import keyboard

def takeItemFromChest():
    print("take item from chest")
    time.sleep(0.1)
    pos = [(817, 355), (851, 356), (887, 355), (923, 354), (961, 354), (996, 355), (1032, 355), (1066, 356), (1104, 354), (817, 388), (851, 389), (885, 391), (924, 389), (959, 391), (996, 391), (1030, 389), (1069, 389), (1106, 393), (816, 426), (853, 423), (888, 426), (925, 425), (962, 428), (998, 427), (1034, 430), (1069, 426), (1106, 430), (816, 459), (851, 460), (888, 463), (924, 464), (959, 463), (998, 463), (1032, 463), (1067, 463), (1106, 462), (812, 495), (850, 496), (888, 497), (925, 499), (961, 501), (996, 501), (1032, 501), (1067, 500), (1103, 499), (816, 532), (850, 532), (886, 534), (921, 534), (960, 536), (995, 535), (1031, 535), (1069, 535), (1105, 535)]

    def chestWorth():
        # checks if there is at least 9 stacks of blocks
        while m.container_get_items() == None:
            time.sleep(0.02)
        quantity_log = 0
        quantity_cocoa = 0
        for item in m.container_get_items():
            if item.item == 'minecraft:jungle_log' and item.slot <= 53:
                quantity_log += item.count
            elif item.item == 'minecraft:cocoa_beans' and item.slot <= 53:
                quantity_cocoa += item.count
        if quantity_log >= 64 and quantity_cocoa >= 256:
            return True
        return False

    print("what??")

    chestIndex = 0
    while True:
        m.execute("/chest")
        time.sleep(1)
        pyautogui.moveTo(pos[chestIndex])
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.3)
        if chestWorth():
            break
        
        time.sleep(0.1)
        keyboard.press_and_release("e")
        chestIndex += 1
        time.sleep(0.1)
        
    
    time.sleep(0.5)

    keyboard.press("shift")
    log_stack_count = 0
    cocoa_stack_count = 0
    container = m.container_get_items()
    for i in container:
        m.echo(i.item , "||||||||" , i.slot)
        if i.item == 'minecraft:jungle_log' and log_stack_count < 1:
            pyautogui.moveTo(pos[i.slot][0], pos[i.slot][1])
            time.sleep(0.02)
            pyautogui.click()
            log_stack_count += 1
        elif i.item == 'minecraft:cocoa_beans' and cocoa_stack_count < 4:
            pyautogui.moveTo(pos[i.slot][0], pos[i.slot][1])
            time.sleep(0.02)
            pyautogui.click()
            cocoa_stack_count += 1
        if log_stack_count + cocoa_stack_count == 5:
            print("total is: ", log_stack_count + cocoa_stack_count)
            keyboard.release("shift")
            time.sleep(0.1)
            keyboard.press_and_release("esc")
            break

def placeLog(corner): # corner = 0 - 1 - 2
    ## Jump and place log
    time.sleep(0.1)
    inv = m.player_inventory()
    for item in inv:
        if "jungle_log" in item.item and 0 <= item.slot <= 8:
            m.player_inventory_select_slot(item.slot)
            break
    time.sleep(0.1)
    m.player_press_jump(True)
    time.sleep(0.1)
    m.player_press_jump(False)
    time.sleep(0.1)
    if corner == 0:
        m.player_set_orientation(45, 90)
    elif corner == 1:
        m.player_set_orientation(45, 65)
    elif corner == 2:
        m.player_set_orientation(-135, 65)
    m.player_press_use(True)
    time.sleep(0.5)
    m.player_press_use(False)
    time.sleep(0.1)

def placeCocoas(corner):
    time.sleep(0.1)
    for item in inv:
        if "cocoa" in item.item and 0 <= item.slot <= 8:
            m.player_inventory_select_slot(item.slot)
            break
    time.sleep(0.1)
    if corner == 1:
        m.player_set_orientation(22, 64)
    else:
        m.player_set_orientation(-160, 64)
    time.sleep(0.1)
    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(0.1)
    if corner == 1:
        m.player_set_orientation(70, 64)
    else:
        m.player_set_orientation(-110, 64)
    time.sleep(0.1)
    m.player_press_use(True)
    m.player_press_use(False)

def moveToCorner(whereTo):
    time.sleep(0.1)
    if whereTo == 2:
        m.player_set_orientation(45, 30)
    else:
        m.player_set_orientation(-135, 30)
    m.echo("started moving")
    m.player_press_forward(True)
    time.sleep(2)
    m.echo("stopped moving")
    m.player_press_forward(False)
    

m.echo("script started, waiting 1 second")
time.sleep(1)

while True:
    ## 1-is go 2
    ## 5 blok ileride blok var ise sağa geç 
    ## dümdüz git, 3 blok kala dur
    ## yerleştirmeye başla

    m.execute("/is go 2")
    time.sleep(1)
    
    inv = m.player_inventory()
    jungle_log_items = [item for item in inv if "jungle_log" in item.item]
    jungle_log_count = sum(item.count for item in jungle_log_items)

    cocoa_items = [item for item in inv if "cocoa_beans" in item.item]
    cocoa_count = sum(item.count for item in cocoa_items)

    if cocoa_count < 4 or jungle_log_count < 1:
        time.sleep(0.05)
        takeItemFromChest()
        time.sleep(0.05)

    m.player_press_sneak(False)

    while True:
        isgo_target = m.player_get_targeted_block(5)
        if isgo_target is not None:
            oldx, oldy, oldz = m.player_position()

            m.player_press_right(True)

            while True:
                print("a")
                newx, newy, newz = m.player_position()
                if abs(newz - oldz) >= 2.75:
                    m.player_press_right(False)
                    break
                time.sleep (0.01)
        else:
            break

    m.player_press_forward(True)
    while m.player_get_targeted_block(3) is None:
        time.sleep(0.02)
    m.player_press_forward(False)
    m.player_press_sneak(True)
    time.sleep(0.02)

    placeLog(0)
    m.player_set_orientation(45, 90)
    time.sleep(0.1)
    m.player_press_backward(True)
    time.sleep(2)
    m.player_press_backward(False)

    

    while True:
        # 1 means (to) first corner
        placeCocoas(1)
        moveToCorner(2)
        placeCocoas(2)
        placeLog(2)
        placeCocoas(2)
        moveToCorner(1)
        placeCocoas(1)

        inv = m.player_inventory()
        jungle_log_items = [item for item in inv if "jungle_log" in item.item]
        jungle_log_count = sum(item.count for item in jungle_log_items)

        if jungle_log_count == 0:
            time.sleep(0.05)
            break

        print("log count: ",jungle_log_count)
        placeLog(1)
    time.sleep(0.05)
