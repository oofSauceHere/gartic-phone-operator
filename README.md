# gartic phone operator

Program that takes a Gartic phone prompt, converts it into an image using StarryAI's API, and draws the image pixel-by-pixel in the Gartic canvas.
---
This one's meant to be silly, but it actually taught me a lot about browser automation and web scraping. In order to get the drawing prompt from the page, the code has to scrape the site. Originally I thought simply using BeautifulSoup would be enough, but Gartic is an online game and attempting to access a game instance's current page from an outside source just takes you to the homepage. This is where Selenium comes in, allowing the code to run in tandem with the browser, giving us access to the current game page. Pretty cool.
I also used OpenCV's built in Canny edge detection to convert the image into a more workable form. It doesn't look *that* good... but hey. It works. AND I have some ideas for how to make it better, so we're not quite done yet.
