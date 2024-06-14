from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from bs4 import BeautifulSoup
import math
import time
import cv2

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
                # print(str(i) + " " + str(j))

                action_chain = ActionChains(driver)
                action_chain.w3c_actions.pointer_action._duration = 0
                action_chain.move_to_element_with_offset(canvas, start_width+j, start_height+i).click().perform()
                # action_chain.move_to_element(canvas).move_by_offset(start_width+j, start_height+i).click().perform()

def main():
    # ignoring errors lol!
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
                print(prompts[0].get_text())

                canvases = driver.find_elements(By.TAG_NAME, "canvas")
                relevant_canvases = [x for x in canvases if x.size["width"]/x.size["height"] == 758/424]

                canvas = relevant_canvases[-1] # width=1516, height=848
                size = canvas.size

                # print(canvas.size)

                image = cv2.imread("images/silly.jpg")
                edge = cv2.Canny(cv2.resize(image, dsize=(math.floor(size["width"]), math.floor(size["height"]))), 50, 150)

                # is this slow ???
                time.sleep(5)
                draw(driver, canvas, edge)

            # so we dont repeat the drawing
            while driver.current_url == current_url:
                time.sleep(0.1)

    # listen for keypress
    driver.quit()

if __name__ == "__main__":
    main()