# dumbass roblox purchase api that keeps the notforsale json error persisting maybe might fix it someday but im using the pyautogui module instead
"""
import datetime
import time
import threading 
import traceback
import json
import requests
from requests import get, Session
from uuid import uuid4

# selenium module is needed to interact with chrome in order to login the bot account and do other stuff
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



file = open("Roblox Cookie.txt", "r", encoding="utf-8-sig")
ROBLOSECURITY = file.read()

# grabbing the id of the deal
item_id = 4773588762

# NOTE: the line below is the id related attached to your roblox account 
userID = 1054849647

session = Session()
session.cookies['.ROBLOSECURITY'] = ROBLOSECURITY

# grab csrf token needed to purchase a logged deal 
csrf = session.post('https://auth.roblox.com/v2/login').headers['x-csrf-token']

# Get base item details
response = session.get(f"https://catalog.roblox.com/v1/catalog/items/{item_id}/details?itemType=Asset", headers={"x-csrf-token": csrf}, cookies={".ROBLOSECURITY": ROBLOSECURITY})
data = response.json()

collid = data.get("collectibleItemId")
if not collid:
    raise ValueError(f"[ERROR] collectibleItemId not found in response: {data}")

print(collid)

details = session.post("https://apis.roblox.com/marketplace-items/v1/items/details", json={"itemIds": [collid]}, headers={"x-csrf-token": csrf}, cookies={".ROBLOSECURITY": ROBLOSECURITY}).json()
if not details or not isinstance(details, list):
    ValueError(f"[ERROR] Unexpected details response: {details}")

details = details[0]

resellers = session.get(f"https://apis.roblox.com/marketplace-sales/v1/item/{collid}/resellers?limit=1", headers={"x-csrf-token": csrf}, cookies={".ROBLOSECURITY": ROBLOSECURITY}).json()
if not resellers or not isinstance(resellers, list):
    ValueError(f"[ERROR] Unexpected resellers response: {resellers}")

first_reseller = resellers["data"][0]

print("\n",first_reseller)

product_id = details.get("collectibleProductId")
price = details.get("lowestResalePrice")
creator = details.get("creatorId")
seller_id = first_reseller.get("sellerId")
collid_instance = first_reseller.get("collectibleItemInstanceId")

print(f"GETTING MORE INFO ON ITEM")
print(f"CSRF: {csrf} Product ID: {product_id} - Price: {price} - Creator ID: {creator} - Collectible ID: {collid} Collectible Instance ID: {collid_instance} Seller ID: {seller_id}")
print("\n")

response = session.post(f'https://apis.roblox.com/marketplace-sales/v1/item/{collid}/purchase-item', json = {"collectibleItemId": collid, "expectedCurrency": 1, "expectedPrice": price, "expectedPurchaserId": str(userID), "expectedPurchaserType": "User", "expectedSellerId": 1, "expectedSellerType": "User", "collectibleItemInstanceId": collid_instance, "idempotencyKey": str(uuid4()), "collectibleProductId": product_id}, headers = {'X-CSRF-TOKEN': csrf})
print(f'https://apis.roblox.com/marketplace-sales/v1/item/{collid}/purchase-item', "collectibleItemId", collid, "expectedCurrency", 1, "expectedPrice", price, "expectedPurchaserId", str(userID), "expectedPurchaserType", "User", "expectedSellerId", 1, "expectedSellerType", None, "collectibleItemInstanceId", collid_instance, "idempotencyKey", str(uuid4()), "collectibleProductId", product_id, 'X-CSRF-TOKEN', csrf)
print("\n")

print(response.json())

#except Exception as e:
#    print(f"whoops failed buying the limited here is the error: {traceback.format_exc()}")

headers = {
    "cookie": f".ROBLOSECURITY={ROBLOSECURITY}",
    "x-csrf-token": csrf,
    "content-type": "application/json"
}

# getting asset details

payload = {
    "items": [
        {
            "itemType": 1,
            "id": item_id
        }
    ]
}

details = requests.post("https://catalog.roblox.com/v1/catalog/items/details", data = json.dumps(payload), headers = headers).json()
details = details["data"][0]
productId = details["productId"]

payload = {
    "expectedSellerId": details["creatorTargetId"],
    "expectedCurrency": 1,
    "expectedPrice": details["lowestResalePrice"]
}

# buying item

buyres = requests.post(f"https://economy.roblox.com/v1/purchases/products/{productId}", headers = headers, data = json.dumps(payload))
print(buyres.json())

"""


import pyautogui 
import time 
import re

"""
#time.sleep(4)
#print(pyautogui.position())

loop = False

list = []

# coords for opening the chrome for testing session

chrome_coords = pyautogui.locateOnScreen("image.png", confidence=0.7)

string_coords = str(chrome_coords).replace("int64", "")
x_y_chrome_choords = re.findall(r'\d+', string_coords)

print(x_y_chrome_choords)

pyautogui.moveTo(int(x_y_chrome_choords[0]), int(x_y_chrome_choords[1]))
pyautogui.leftClick()
pyautogui.leftClick()

# coords for buying and confirming 

while loop == False:

    if pyautogui.pixelMatchesColor(1243, 511, (51, 95, 255)):
        pyautogui.moveTo(1243, 511)
        pyautogui.leftClick()
        pyautogui.moveTo(904, 762)
        loop = True

time.sleep(5)

"""


recursion = None

def Clicking_Buttons(): 

    try:

        loop = False

        while loop == False:
                    
            if pyautogui.locateOnScreen("Buy_Button.png", confidence=0.7):

                buy_coords = pyautogui.locateOnScreen("Buy_Button.png", confidence=0.7)
                buy_string_coords = str(buy_coords).replace("int64", "")
                x_y_buy_choords = re.findall(r'\d+', buy_string_coords)
                pyautogui.moveTo(int(x_y_buy_choords[0]), int(x_y_buy_choords[1]))
                pyautogui.leftClick()
                #pyautogui.leftClick()

                confirm_coords = pyautogui.locateOnScreen("Confirm_Button.png", confidence=0.7)
                confirm_string_coords = str(confirm_coords).replace("int64", "")
                x_y_confirm_choords = re.findall(r'\d+', confirm_string_coords)
                pyautogui.moveTo(int(x_y_confirm_choords[0]), int(x_y_confirm_choords[1]))
                #pyautogui.leftClick()

                time.sleep(5)
                #driver.switch_to.window(driver.window_handles[0])
                #driver.refresh()
                
                print("SUCCESSFULLY PURCHASED LIMITED YOOOOOOO")
                Recursion = True

                return Recursion

    except Exception:
        None
        

while recursion == None:
    recursion = Clicking_Buttons()