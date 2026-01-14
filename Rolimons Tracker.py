import datetime
import time
import threading 
import traceback
import pyautogui 
import re

# selenium module is needed to interact with chrome in order to login the bot account and do other stuff
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

CHROME_FOR_TESTING_BINARY = r"/home/hubyark/chrome-linux64/chrome" # where your chrome for testing directory is held
CHROMEDRIVER_PATH = r"/home/hubyark/chromedriver-linux64/chromedriver" # the path where u store chromedriver for selenium
options = webdriver.ChromeOptions()
options.binary_location = CHROME_FOR_TESTING_BINARY

def Roblox_Login():

    # read a seperate text file that contains your roblox security cookie and set the cookie variable as the contents of the text file 
    file = open("Roblox Cookie.txt", "r", encoding="utf-8-sig")
    ROBLOSECURITY = file.read()

    try:
        driver.get('https://www.roblox.com/')
        driver.add_cookie({'name': '.ROBLOSECURITY', 'value': ROBLOSECURITY, 'domain': 'roblox.com'})
        driver.refresh()
        print("logged into roblox")

        driver.get("https://www.rolimons.com/deals")
        # run the timer function refreshing the rolimons page in the background to prevent it interfering with the main function - Huby
        background_process = threading.Thread(target=refresh_rolimons)
        background_process.start()

    except Exception as e:
        print(f"your screwed failed login {e} ")

    return ROBLOSECURITY

def bypass_random_id():

    try:
        main_element = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[5]')
        div_grabbed_id = main_element.get_attribute("id")
        print(f"stolen random id: {div_grabbed_id} time stolen: {datetime.datetime.now()}")

    except Exception as e:
        print(f"you screwed up here is what happened: {e}")

    return div_grabbed_id

def refresh_rolimons():
    # refresh once every 14 mins and 30 secs (time before prompting to refresh 15 mins)
    try: 
        countdown = 870

        while True:

            if countdown == 0:
                # refresh rolimons to keep monitoring deals without stopping on a different thread in the background 
                driver.refresh()
                refresh_rolimons()

            else:
                time.sleep(1)
                countdown -= 1

    except Exception as e:
        print(f"goofy error once more: {e}")

def File_Writer(deal_percentage, RAP_range, price_range, item_name, profit):
    # instead of writing to the file also put it on append mode so you can modify the data while not overwriting the contents of it altogether
    file = open("Rolimons Data.csv", "a", encoding='utf-8-sig')
    file.write(f"\n{item_name}, {RAP_range}, {price_range}, {deal_percentage}%, {profit}, {datetime.datetime.now()}")

def Blacklisted_Items():

    Item_Blacklist = []

    file = open("Item Blacklist.txt", "r", encoding='utf-8-sig')

    for line in file:
        row = line.strip().split(",")
        Item_Blacklist.append(str(row[0]))

    return Item_Blacklist

def track_rolimons():

    try:

        # as the script runs and errors appear the rolimons website will refresh a lot so for now put a cooldown here as a band aid solution  
        driver.get("https://www.rolimons.com/deals")
        time.sleep(1)

        print("starting to track rolimons (once more maybe)")

        MAX_DEAL_PERCENTAGE = 100

        # adjust this to your liking for buying items with greater or equal amounts of RAP same applies to the percentage off 
        RAP_FILTER = 2500
        PERCENT_DEAL_FILTER = 35
        PRICE_FILTER = 1750
        MIN_PROFIT = 575
        
        # these variables soley exist for logging and not actually buying any of the items to gather more data
        LOGGING_RAP_FILTER = 10000000
        LOGGING_PERCENT_DEAL_FILTER = 35
        LOGGING_PRICE_FILTER = 10000000
        LOGGING_MIN_PROFIT = 1

        LPP_ITEM_PRICE_FILTER = 90
        LPP_ITEM_PROFIT = 1000

        # filtering by making all the items with the best deals appear the top instead of random order via most recent deal      
        sort_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page_content_body"]/div[4]/div[1]/button')))
        driver.execute_script("arguments[0].click();", sort_button)

        best_deal_sort = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page_content_body"]/div[4]/div[1]/btn-block/a[3]')))
        driver.execute_script("arguments[0].click();", best_deal_sort)
        
        div_grabbed_id = bypass_random_id() 

        # the waiting process for the bot to find the best deal possible also stop the script tempoarily so that in a scenario where an item gets picked its not the second one cuz its too fast
        time.sleep(0.3)
        while True: 

            time.sleep(0.25)
            deal_percentage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a/div/div[3]/div[3]/div[2]'))).text.replace("%", "").replace(",", "") 
            RAP_range = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a/div/div[3]/div[2]/div[2]'))).text.replace(",", "")
            price_range = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a/div/div[3]/div[1]/div[2]'))).text.replace(",", "")
            item_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a/div/div[1]/div'))).text.replace(",", "")
            
            # the profit you could make at the current moment 
            unrounded_profit = (int(RAP_range) * 0.7) - int(price_range)
            profit = int(unrounded_profit)

            for i in range(0, len(Item_Blacklist)):
                if item_name == Item_Blacklist[i] and int(deal_percentage) >= PERCENT_DEAL_FILTER:
                    print(f"Blacklisted item wont be bought or logged: {item_name} (RAP: {RAP_range}, Price: {price_range}, Percent off: {deal_percentage}%, Profit: {profit}, Date logged: {datetime.datetime.now()})")
                    return None

            # items with values will move down the deal percent element position down a column meaning we need to update the old position element with the new position element
            if int(deal_percentage) > MAX_DEAL_PERCENTAGE:
                deal_percentage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a/div/div[3]/div[4]/div[2]'))).text.replace("%", "") 

            if int(deal_percentage) >= PERCENT_DEAL_FILTER and int(RAP_range) >= RAP_FILTER and int(price_range) >= int(PRICE_FILTER) and profit >= MIN_PROFIT and Logging_Mode == False:

                print(f"\nYES BUYING A DEAL!: Name: {item_name}, RAP: {RAP_range}, Price: {price_range}, Percent off: {deal_percentage}%, Profit: {profit}, Date logged: {datetime.datetime.now()}")
                File_Writer(deal_percentage, RAP_range, price_range, item_name, profit)
                buying_the_limited(div_grabbed_id)
                time.sleep(2)

                return deal_percentage, RAP_range, price_range, item_name, profit

            elif int(deal_percentage) >= LOGGING_PERCENT_DEAL_FILTER and int(RAP_range) <= LOGGING_RAP_FILTER and int(price_range) <= int(LOGGING_PRICE_FILTER) and profit >= LOGGING_MIN_PROFIT:

                print(f"\nYES FOUND A DEAL!: Name: {item_name}, RAP: {RAP_range}, Price: {price_range}, Percent off: {deal_percentage}%, Profit: {profit}, Date logged: {datetime.datetime.now()}")
                File_Writer(deal_percentage, RAP_range, price_range, item_name, profit)
                time.sleep(2)
                return deal_percentage, RAP_range, price_range, item_name, profit 
            
            # this condition is purely there to buy items that have been put at an extremely low price in an attempt to buy it 
            elif int(price_range) <= LPP_ITEM_PRICE_FILTER and profit >= LPP_ITEM_PROFIT and Logging_Mode == False:
                print(f"\nYES FOUND A LPPED DEAL!: Name: {item_name}, RAP: {RAP_range}, Price: {price_range}, Percent off: {deal_percentage}%, Profit: {profit}, Date logged: {datetime.time.now()}")
                
                File_Writer(deal_percentage, RAP_range, price_range, item_name, profit)
                buying_the_limited(div_grabbed_id)
                time.sleep(2)
                return deal_percentage, RAP_range, price_range, item_name, profit 

            
    except Exception as e:
        print(f"oooh you screwed up big time lol: {traceback.format_exc()}")

def Clicking_Buttons(Recursion): 

    try:

        if pyautogui.locateOnScreen("Buy_Button.png", confidence=0.7):

            buy_coords = pyautogui.locateOnScreen("Buy_Button.png", confidence=0.7)
            buy_string_coords = str(buy_coords).replace("int64", "")
            x_y_buy_choords = re.findall(r'\d+', buy_string_coords)
            pyautogui.moveTo(int(x_y_buy_choords[0]), int(x_y_buy_choords[1]))
            pyautogui.leftClick()

            if pyautogui.locateOnScreen("Not_Enough.png", confidence=0.7):

                print("nvm brah the item is too expensive...")
                driver.switch_to.window(driver.window_handles[0])
                driver.refresh()
                Recursion = True

                return Recursion
            
            else:

                confirm_coords = pyautogui.locateOnScreen("Confirm_Button.png", confidence=0.7)
                confirm_string_coords = str(confirm_coords).replace("int64", "")
                x_y_confirm_choords = re.findall(r'\d+', confirm_string_coords)
                pyautogui.moveTo(int(x_y_confirm_choords[0]), int(x_y_confirm_choords[1]))
                pyautogui.leftClick()

                time.sleep(5)
                driver.switch_to.window(driver.window_handles[0])
                driver.refresh()
                
                print("SUCCESSFULLY PURCHASED LIMITED YOOOOOOO")
                Recursion = True

                return Recursion

    except Exception:
        None

def buying_the_limited(div_grabbed_id):

    try: 

        # PLEASE READ: because the roblox api sucks this script uses pyautogui which is sensitive of where your cursor goes to buy it automatically 
        # so adjust this as you will with how your pc is setup  

        # grabbing the id of the deal
        link_element = driver.find_element(By.XPATH, f'//*[@id="{div_grabbed_id}"]/div[1]/a')
        driver.execute_script("arguments[0].click();", link_element)
        
        # pyautogui module will try to find the image at 100% confidence by default so allow some tolerence
        # that is enough to locate the app accurately also this is a way better solution compared to hard coding 
        # pixel coordinates that are very unstable if for example your taskbar increases in size
        chrome_coords = pyautogui.locateOnScreen("image.png", confidence=0.7)
        string_coords = str(chrome_coords).replace("int64", "")

        # index 0 and 1 contain the x and y coordinates of the chrome for testing browser app in the taskbar
        # while the other indexes are irrelevant info
        x_y_chrome_choords = re.findall(r'\d+', string_coords)

        Recursion = None

        # your cursor is very likely moving while your doing other stuff so do this repeatedly to make sure the cursor dosent miss the icon being clicked
        for i in range(0, 5):
            pyautogui.moveTo(int(x_y_chrome_choords[0]), int(x_y_chrome_choords[1]))
        pyautogui.leftClick()
        pyautogui.leftClick()

        while Recursion == None:
            Recursion = Clicking_Buttons(Recursion)

    except Exception as e:
        print(f"whoops failed buying the limited here is the error: {traceback.format_exc()}")

# MAIN PROGRAM 

input_validation = False
Logging_Mode = False

while input_validation == False:

    headless_input = input("Do you want to run the script in headless mode? (y/n): ").lower()

    if headless_input == 'y':
        HEADLESS_MODE = True
        Logging_Mode = True
        input_validation = True

        # for anyone using an os other than linux or you use X11 display server feel free to remove this argument below otherwise you may wanna keep this 
        # to prevent any gpu errors that arise from launching google chrome for testing sessions that stop the script from functioning whatsoever - Huby 
        options.add_argument(f"--ozone-platform-hint=wayland")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu") # Optional, can help with performance in headless mode

    elif headless_input == 'n':
        HEADLESS_MODE = False
        input_validation = True
    
    else:
        print("\nyou didn't do this right enter the input again.")

# this line below is what launches chrome for testing 
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
ROBLOSECURITY = Roblox_Login()
Item_Blacklist = Blacklisted_Items()

# your gonna be constantly tracking rolimons 24/7 so if an error did occur just call the function again
while True:
     track_rolimons()