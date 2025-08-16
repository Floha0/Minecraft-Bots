from system.lib import minescript as m
import time
import pyautogui
import keyboard

# 1- go island and pull items from /çiftçi
# 2- open suitable chest and send there
# 3- go trader and trade items
# 4- scan chests and trade them all

pos = [(817, 355), (851, 356), (887, 355), (923, 354), (961, 354), (996, 355), (1032, 355), (1066, 356), (1104, 354), (817, 388), (851, 389), (885, 391), (924, 389), (959, 391), (996, 391), (1030, 389), (1069, 389), (1106, 393), (816, 426), (853, 423), (888, 426), (925, 425), (962, 428), (998, 427), (1034, 430), (1069, 426), (1106, 430), (816, 459), (851, 460), (888, 463), (924, 464), (959, 463), (998, 463), (1032, 463), (1067, 463), (1106, 462), (812, 495), (850, 496), (888, 497), (925, 499), (961, 501), (996, 501), (1032, 501), (1067, 500), (1103, 499), (816, 532), (850, 532), (886, 534), (921, 534), (960, 536), (995, 535), (1031, 535), (1069, 535), (1105, 535)]
invPos = [(818, 597), (854, 599), (885, 596), (925, 598), (961, 596), (995, 598), (1032, 596), (1071, 596), (1104, 596), (816, 635), (854, 634), (890, 632), (925, 633), (962, 633), (996, 634), (1035, 633), (1068, 633), (1104, 632), (817, 669), (852, 668), (890, 669), (923, 667), (961, 669), (997, 668), (1032, 669), (1068, 669), (1104, 670), (817, 713), (853, 713), (888, 713), (925, 714), (959, 714), (997, 713), (1032, 713), (1067, 712), (1106, 714)]
traderCocoaPos = [(778, 493), (1141, 448)]
craftPos = [(965, 442), (925, 661), (961, 661), (1047, 446)]
fullChests = []

def waitForAction(action):
    # action values:
    # 0- pv 1 ... 4- pv 5
    # 5- pv
    # 6- trader
    # 7- çiftçi
    # 8- is go trade
    # 9- warp takas
    if 0 <= action <= 4:
        i = 0
        while True:
            container = m.container_get_items()
            if container is not None:
                detector = next((item for item in container if item.slot == action and item.item == "minecraft:gold_ingot"), None)
                if detector is not None:
                    break

            i += 1
            x,y = pyautogui.position()
            if i > 20:
                m.execute("/pv")
                waitForAction(5)
                time.sleep(1)
                pyautogui.moveTo(x,y)
                time.sleep(0.02)
                pyautogui.click()
                break

            time.sleep(0.05)
    elif action == 5:
        while True:
            container = m.container_get_items()
            if container is not None and container[0].item == 'minecraft:barrel':
                break
            time.sleep(0.05)
    elif action == 6:
        while True:
            container = m.container_get_items()
            if container is not None:
                detector = next((item for item in container if item.slot == 11 and item.item == "minecraft:emerald"), None)
                if detector is not None:
                    break
                break
            time.sleep(0.05)
    elif action == 7:
        while True:
            container = m.container_get_items()
            if container is not None and container[0].item == 'minecraft:gray_stained_glass_pane':
                break
            time.sleep(0.05)
    elif action == 8:
        while True:
            if m.player_position()[0] > 10000:
                break
            time.sleep(0.05)
        time.sleep(0.25)
    elif action == 9:
        while True:
            if m.player_position()[0] < 1000:
                break
            time.sleep(0.05)
        time.sleep(0.25)
        print("in takas")
    
    time.sleep(0.1)

def openFirstSuitableChest():
    # Returns False if found no chest
    for i in range(5):
        if i in fullChests:
            continue
        # open chest
        m.execute("/pv")
        
        waitForAction(5)

        time.sleep(0.1)
        pyautogui.moveTo(pos[i])
        time.sleep(0.02)
        pyautogui.click()
        waitForAction(i)

        # scan slots
        container = m.container_get_items()
        filled_slots = {item.slot for item in container}
        haveSpace = False
        for slot in range(54):
            if slot not in filled_slots:
                haveSpace = True
                break
        print(haveSpace)
        if haveSpace:
            return True
        fullChests.append(i)
        time.sleep(0.02)

def openFirstFullChest():
    for i in range(5):
        if i not in fullChests:
            continue
        # open chest
        m.execute("/chest")
        waitForAction(5)
        time.sleep(0.1)
        pyautogui.moveTo(pos[i])
        time.sleep(0.02)
        pyautogui.click()
        waitForAction(i)
        return i

def findCocoasInInv():
    container = m.container_get_items()
    cocoa_items = [
        item for item in container
        if item.slot > 53 and "cocoa" in item.item.lower()
    ]
    return cocoa_items[:2]  

def findCocoasInChest():
    container = m.container_get_items()
    cocoa_items = [
        item for item in container
        if item.slot < 54 and "cocoa" in item.item.lower()
    ]
    return cocoa_items[:2]  

def pullAndPushItems():
    m.execute("/is go trade")
    waitForAction(8)
    while True:
        m.execute("/çiftçi")
        waitForAction(7)
        pyautogui.moveTo(pos[14])
        time.sleep(0.02)
        pyautogui.rightClick()
        time.sleep(0.1)
        keyboard.press_and_release("e")
        chestOpened = openFirstSuitableChest()
        if not chestOpened:
            return
        time.sleep(0.1)
        cocoasInInv = findCocoasInInv()
        pyautogui.moveTo(invPos[cocoasInInv[0].slot - 54])
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.02)
        pyautogui.moveTo(invPos[cocoasInInv[1].slot - 54])
        keyboard.press("shift")
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.025)
        pyautogui.leftClick()
        time.sleep(0.02)
        keyboard.release("shift")
        
        container = m.container_get_items()
        filled_slots = {item.slot for item in container}
        haveSpace = False
        for slot in range(54):
            if slot not in filled_slots:
                haveSpace = True
                break
        print(haveSpace)
        if not haveSpace:
            fullChests.append(fullChests[-1] + 1 if fullChests else 0)
                
def moveToTrader():
    m.execute("/warp takas")
    waitForAction(9)
    m.player_press_forward(True)
    time.sleep(1)
    keyboard.press("ctrl")
    time.sleep(0.5)
    keyboard.release("ctrl")
    time.sleep(1)

    while True:
        x,y,z = m.player_position()
        x,z = int(x), int(z)
        if x == 115 and z == -1:
            m.player_press_forward(False)
            time.sleep(0.1)
            m.player_look_at(118.5,56.5,-1.5)
            time.sleep(0.1)
            m.player_press_forward(True)
            time.sleep(0.25)
            m.player_press_forward(False)
            break
        time.sleep(0.02)
    
def pullItemsFromChest(chestIndex):
    cocoasInChest = findCocoasInChest()
    if len(cocoasInChest) != 2:
        fullChests.remove(chestIndex)
        return
    pyautogui.moveTo(pos[cocoasInChest[0].slot])
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.02)
    pyautogui.moveTo(pos[cocoasInChest[1].slot])
    keyboard.press("shift")
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.025)
    pyautogui.leftClick()
    time.sleep(0.02)
    keyboard.release("shift")
    time.sleep(0.02)
    cocoasInChest = findCocoasInChest()
    if len(cocoasInChest) != 2:
        fullChests.remove(chestIndex)

def tradeItems():
    moveToTrader()
    
    while True:
        time.sleep(0.1)
        m.player_press_use(True)
        time.sleep(0.02)
        m.player_press_use(False)
        time.sleep(0.5)
        pyautogui.moveTo(traderCocoaPos[0])
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.02)
        pyautogui.moveTo(traderCocoaPos[1])
        
        inv = m.player_inventory()
        cocoa_items = [item for item in inv if "cocoa" in item.item]
        cocoa_count = sum(item.count for item in cocoa_items)

        i = 0
        while i < cocoa_count / 64 + 1:
            print(i)
            keyboard.press_and_release('space')
            time.sleep(0.02)
            pyautogui.click(interval=0.02)
            i += 1
        
        m.execute("/pv 1")
        waitForAction(0)
        container = m.container_get_items()
        diamond_item = next((item for item in container if item.slot > 53 and item.item == "minecraft:diamond"), None)
        if diamond_item != None:
            time.sleep(0.1)
            pyautogui.moveTo(invPos[diamond_item.slot - 54])
            time.sleep(0.02)
            keyboard.press("shift")
            time.sleep(0.02)
            pyautogui.click()
            time.sleep(0.02)
            keyboard.release("shift")
            time.sleep(0.02)
        else:
            time.sleep(1)

        if len(fullChests) == 0:
            return
        
        chestIndex = openFirstFullChest()
        print("opened")
        pullItemsFromChest(chestIndex)
        print("pulled")
        time.sleep(0.1)
        print("pressed e")
        keyboard.press_and_release("e")
        time.sleep(0.1)
        
def craftDiaBlocks():
    m.execute("/is go trade")
    waitForAction(8)
    m.execute("/pv 1")
    waitForAction(0)
    container = m.container_get_items()
    diamond_items = [item for item in container if item.slot < 54 and item.item == "minecraft:diamond"]
    diamond_count = sum(item.count for item in diamond_items)

    if diamond_count < 641:
        time.sleep(0.02)
        keyboard.press_and_release("e")
        time.sleep(0.02)
        return
    
    pyautogui.moveTo(pos[diamond_items[0].slot])
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.02)
    pyautogui.moveTo(pos[diamond_items[1].slot])
    keyboard.press("shift")
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.025)
    pyautogui.leftClick()
    time.sleep(0.02)
    keyboard.release("shift")
    time.sleep(0.02)
    
    keyboard.press_and_release("e")
    time.sleep(0.1)
    m.player_press_use(True)
    time.sleep(0.02)
    m.player_press_use(False)

    time.sleep(1)
    pyautogui.moveTo(craftPos[0])
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.05)
    pyautogui.moveTo(craftPos[1])
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.02)
    pyautogui.moveTo(craftPos[2])
    keyboard.press("shift")
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.025)
    pyautogui.leftClick()
    time.sleep(0.02)
    pyautogui.moveTo(craftPos[3])
    time.sleep(0.02)
    pyautogui.leftClick()
    time.sleep(0.02)
    keyboard.release("shift")
    time.sleep(0.02)

    m.execute("/pv 1")
    waitForAction(0)
    container = m.container_get_items()
    diamond_block_item = next((item for item in container if item.slot > 53 and "diamond_block" in item.item), None)
    if diamond_block_item is not None:
        time.sleep(0.1)
        pyautogui.moveTo(invPos[diamond_block_item.slot - 54])
        time.sleep(0.02)
        keyboard.press("shift")
        time.sleep(0.02)
        pyautogui.click()
        time.sleep(0.02)
        keyboard.release("shift")
        time.sleep(0.02)

    diamond_items = [item for item in container if item.slot > 53 and item.item == "minecraft:diamond"]

    if len(diamond_items) >= 2:
        pyautogui.moveTo(invPos[diamond_items[0].slot - 54])
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.02)
        pyautogui.moveTo(invPos[diamond_items[1].slot - 54])
        keyboard.press("shift")
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.025)
        pyautogui.leftClick()
        time.sleep(0.02)
        keyboard.release("shift")
        time.sleep(0.02)
    elif len(diamond_items) == 1:
        pyautogui.moveTo(invPos[diamond_items[0].slot - 54])
        time.sleep(0.02)
        keyboard.press("shift")
        time.sleep(0.02)
        pyautogui.leftClick()
        time.sleep(0.02)
        keyboard.release("shift")
        time.sleep(0.02)

    

while True:
    craftDiaBlocks()
    time.sleep(1)
    pullAndPushItems()
    time.sleep(1)
    tradeItems()
    time.sleep(1)