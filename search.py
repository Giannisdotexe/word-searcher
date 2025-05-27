
#depreceated code
#this was too slow but worked without a chrome driver

from PIL import ImageGrab, Image
import keyboard
import numpy as np
import pyautogui
import pytesseract
import threading
import concurrent.futures
from solver import Solver
import datetime

start = datetime.datetime.now()


BOX_SIZE = 560
BOX_X = 670
BOX_Y = 216
CELL_SIZE = 35
CELL_NUMBER = 16
WORD_BOX_WIDTH = 660
WORD_BOX_HEIGHT = 100
WORD_BOX_X = 620
WORD_BOX_Y = 825

r = (BOX_X, BOX_Y, BOX_X+BOX_SIZE, BOX_Y+BOX_SIZE)
shot = ImageGrab.grab(bbox=r)
shot.save("img.png")

r = (WORD_BOX_X, WORD_BOX_Y, WORD_BOX_X+WORD_BOX_WIDTH, WORD_BOX_Y+WORD_BOX_HEIGHT)
shot = ImageGrab.grab(bbox=r)
shot.save("words.png")


pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract\tesseract'

img = Image.open("img.png")
w = Image.open("words.png")

grid = [["A" for j in range(16)] for i in range(16)]


text = pytesseract.image_to_string(w)
text = text.replace("\n", " ").strip()
words = text.split(" ")

def find_letter(i, j):
    crop = img.crop((j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE))
    crop.save(f"crop[{j}].png")
    im = Image.open(f"crop[{j}].png")
    letter = pytesseract.image_to_string(im, config="--psm 10").strip("\n").upper()
    if len(letter) > 1:
        letter = letter[0]
    if letter == "|":
        letter = "I"
    print(letter)
    grid[i][j] = letter

#weird bug with threads:
#for some reason the first 8 letters are always skipped
#my assumption is because the threads take some time to start up so by the time they have been initialized
#the loop does not wait for them to finish and instead continues to the next iteration
#so i have to do an extra loop (hence the range starts from -1) in order for the threads to be initialized


with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(-1, 16):
        #grid.append([])
        for j in range(0, 9, 8):
            args = [[i, i, i, i, i, i, i, i], [j, j+1, j+2, j+3, j+4, j+5, j+6, j+7]]
            executor.map(find_letter, *args)

            
        # t1 = threading.Thread(target=find_letter, args=(i, j,))
        # t1.start()
        # t2 = threading.Thread(target=find_letter, args=(i, j+1,))
        # t2.start()
        # t3 = threading.Thread(target=find_letter, args=(i, j+2,))
        # t3.start()
        # t4 = threading.Thread(target=find_letter, args=(i, j+3,))
        # t4.start()
        # t5 = threading.Thread(target=find_letter, args=(i, j+4,))
        # t5.start()
        # t6 = threading.Thread(target=find_letter, args=(i, j+5,))
        # t6.start()
        # t7 = threading.Thread(target=find_letter, args=(i, j+6,))
        # t7.start()
        # t8 = threading.Thread(target=find_letter, args=(i, j+7,))
        # t8.start()

        # t1.join()
        # t2.join()
        # t3.join()
        # t4.join()
        # t5.join()
        # t6.join()
        # t7.join()
        # t8.join()
    

end = datetime.datetime.now()

delta = end - start
print(delta.total_seconds())

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


# letter: CELL_SIZExCELL_SIZE
# grid: 560x560
# TL: 670 207
# BR: 1230 767
