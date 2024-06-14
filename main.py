# gartic could ban me for this

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from bs4 import BeautifulSoup

import requests
import math
import time
import cv2
import json

from dotenv import load_dotenv
import os

# opencv testing
# image = cv2.imread("images/silly.jpg")
# edge = cv2.Canny(cv2.resize(image, dsize=(1516, 848)), 50, 150)
# cv2.imshow("edge", edge)
# cv2.waitKey()

def draw(driver, canvas, img):
    start_width = -1*(canvas.size["width"]/2)
    start_height = -1*(canvas.size["height"]/2)

    height, width = img.shape
    for i in range(0, height, 3):
        for j in range(0, width, 3):
            if img[i, j] == 255:
                action_chain = ActionChains(driver, duration=0)
                action_chain.move_to_element_with_offset(canvas, start_width+j, start_height+i).click().perform()
                # action_chain.move_to_element(canvas).move_by_offset(start_width+j, start_height+i).click().perform()

def make_image(prompt) -> str:
    url = "https://api.starryai.com/creations/"

    payload = {
        "prompt": prompt,
        "aspectRatio": "landscape",
        "images": "1"
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": os.getenv("API_KEY")
    }

    response = requests.post(url, json=payload, headers=headers)

    time.sleep(1) # not good...
    return json.loads(response.json())["id"]

def get_image(id):
    url = "https://api.starryai.com/creations/"

    headers = {
        "accept": "application/json",
        "X-API-Key": os.getenv("API_KEY")
    }

    # remember to check if image status is "completed" before getting url
    response = requests.get(url+id, headers=headers)
    image_url = json.loads(response.json())["images"][0]["url"]

def main():
    # ignoring errors...
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = uc.Chrome(options=options)

    # going to gartic phone
    print("starting...")
    driver.get('https://garticphone.com')
    print("started !!")

    # evermore
    while True:
        current_url = driver.current_url
        if "draw" in current_url:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            prompts = soup.find_all("h3") # prompt is always in an h3 tag (i checked)

            if len(prompts) > 0:
                # find the prompt and make an image from it
                prompt = prompts[0].get_text()
                # id = make_image(prompt)
                # get_image(id)

                # determine where the gartic canvas is and determine its dimensions
                canvases = driver.find_elements(By.TAG_NAME, "canvas")
                relevant_canvases = [x for x in canvases if x.size["width"]/x.size["height"] == 758/424]
                canvas = relevant_canvases[-1] # width=1516, height=848
                size = canvas.size

                # print(canvas.size)

                # read in image and scale appopriately
                filename = input("Enter filename: ")
                image = cv2.imread("images/" + filename)
                width, height, _ = image.shape
                if(width > height):
                    height = math.floor(height * size["width"]/width)
                    width = size["width"]
                else:
                    width = math.floor(width * size["height"]/height)
                    height = size["height"]
                
                # get edges (to be drawn)
                edge = cv2.Canny(cv2.resize(image, dsize=(width, height)), 50, 150)

                # allow time for player to choose pixel size (will be automated)
                time.sleep(5)
                draw(driver, canvas, edge)

            # so we dont repeat the drawing
            while driver.current_url == current_url:
                time.sleep(0.1)

    # listen for keypress (not done yet)
    driver.quit()

if __name__ == "__main__":
    load_dotenv() # so we can access api key
    main()