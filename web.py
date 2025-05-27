from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import time
import keyboard
import datetime
import pyautogui
import numpy as np
from solver import Solver

BOX_SIZE = 520
BOX_X = 690
BOX_Y = 240
CELL_SIZE = 32.44
CELL_NUMBER = 16

WORD_BOX_WIDTH = 660
WORD_BOX_HEIGHT = 100
WORD_BOX_X = 620
WORD_BOX_Y = 825


options = Options()
#options.binary_location = "F:/Desktop/Chrome_Testing/chrome-win64/chrome.exe"
browser = webdriver.Chrome(service=Service("F:/Desktop/Chrome_Testing/chromedriver132/chromedriver-win64/chromedriver.exe"))

url = 'https://thewordsearch.org/'

#cellVal cellVal16

browser.get(url)

while True:
    while True:
        if keyboard.is_pressed('s'):
            break


    page_source = browser.page_source

    soup = bs(page_source, 'html.parser')
    divs = soup.find_all('div', class_='cellVal')
    words = soup.find_all('li', class_='word')
    words = [word.get_text() for word in words]
    letters = [div.get_text() for div in divs]

    #print(letters)

    grid = []

    def to_matrix(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    grid = to_matrix(letters, 16)

    print(grid)
    print(words)

    solver = Solver(grid, words)
    solution = solver.solve()


    print(solution)



    while True:
        if keyboard.is_pressed('s'):
            for word in words:
                if len(solution[word]) > 0:
                    start_x, start_y = BOX_X + CELL_SIZE/2 + solution[word][0][1]*CELL_SIZE, BOX_Y + CELL_SIZE/2 + solution[word][0][0]*CELL_SIZE
                    end_x, end_y = BOX_X + CELL_SIZE/2 + solution[word][-1][1]*CELL_SIZE, BOX_Y + CELL_SIZE/2 + solution[word][-1][0]*CELL_SIZE
                    pyautogui.moveTo(start_x, start_y, duration=0.001)
                    pyautogui.mouseDown()  # Press the mouse button
                    pyautogui.moveTo(end_x, end_y, duration=0.001)  # Move to end position
                    pyautogui.mouseUp()  # Release the mouse button
            break
        if keyboard.is_pressed('q'):
            browser.quit()
