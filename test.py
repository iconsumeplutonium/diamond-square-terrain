from random import *
from PIL import ImageColor, ImageTk
import PIL.Image
from tkinter import *
import time

size = 10
heightMin = 0
heightMax = 100
windowSize = 750

def main():
    # Perform and time the algorithm
    m_size = int(pow(2, size) + 1)
    start_time = time.time()
    img = img_from_diamond_square(m_size)
    end_time = time.time()

    # Settings for the tkinter window
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.geometry(str(windowSize) + "x" + str(windowSize))
    root.title("CS50X Final - Diamond Square algorithm")
    img_size = int(windowSize * 0.75)

    # Resize the image to 75% of the window Size and display it
    resized_img = img.resize((img_size, img_size), PIL.Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(resized_img)
    label = Label(root, image=new_pic)
    label.pack(pady=5)

    # Text that displays how long it took to generate the map and image
    generationTime = "Generated map and image in " + str(round(end_time - start_time, 3)) + " seconds"
    t = Label(root, text=generationTime)
    t.pack(pady=1)

    # Slider
    slider = Scale(root, from_=1, to=20, orient=HORIZONTAL)
    slider.set(size)
    slider.pack(pady=1)

    # Slider label and warning
    t1 = Label(root, text="Map Size")
    t1.pack()
    t2 = Label(root, text="Map size will be a square with side length of 2ⁿ + 1")
    t2.pack()
    t3 = Label(root, text="Warning: Setting the map size slider too high may cause the program to stop responding if you have a lower-end computer.")
    t3.pack()

    # Button that generates a new map on each button press
    generate_button = Button(root, command=lambda: generate_button_callback(slider.get(), root, label, img_size, t), text="Generate new map")
    generate_button.pack(side=BOTTOM, pady=10)

    root.mainloop()
    
# Diamond-Square Algorithm
def diamond_square(mapSize):
    # Creates the 2D array
    _map = [[0 for i in range(mapSize)] for j in range(mapSize)]

    # Set the four corners of the map to some random value
    _map[0][0] = randint(heightMin, heightMax)
    _map[0][mapSize  - 1] = randint(heightMin, heightMax)
    _map[mapSize - 1][0] = randint(heightMin, heightMax)
    _map[mapSize - 1][mapSize - 1] = randint(heightMin, heightMax)

    # The diamond-square algorithm itself
    chunkSize = mapSize - 1
    roughness = 10
    while chunkSize > 1:
        diamond_step(mapSize, int(chunkSize), _map, roughness)
        square_step(mapSize, int(chunkSize), _map, roughness)
        chunkSize /= 2
        roughness /= 2

    # Due to the roughness function, there is a possibility for "negative landmasses" to exist:
    # massive continents or chunks of land that are entirely comprised of negative numbers. 
    # This loop goes through the map and makes sure every value is positive, turning those negative landmasses
    # into normal landmasses. 
    for i in range(0, mapSize):
        for j in range(0, mapSize):
            _map[i][j] = abs(_map[i][j])

    return _map

# Performs the square step in the Diamond-Step algorithm
def square_step(mapSize, cSize, _map, roughness):
    h = int(cSize / 2)
    for i in range(0, mapSize, h):
        for j in range((i + h) % cSize, mapSize, cSize):
            value = 0
            count = 0

            # Sometimes values might not have 4 points around them. For example, a corner might only have 3
            # This code takes those outliers into account.
            if not j - h < 0:
                value += _map[i][j - h]
                count += 1
            
            if not j + h > mapSize - 1:
                value += _map[i][j + h]
                count += 1
            
            if not i + h > mapSize - 1:
                value += _map[i + h][j]
                count += 1
            
            if not i - h < 0:
                value += _map[i - h][j]
                count += 1

            _map[i][j] = (value / count) + roughness_offset(roughness)

# Performs the diamond step in the Diamond-Step algorithm
def diamond_step(mapSize, cSize, _map, roughness):
    h = int(cSize / 2)
    for i in range(0, mapSize - 1, cSize):
        for j in range(0, mapSize - 1, cSize):            
            value = (_map[i][j] + _map[i][j + cSize] + _map[i + cSize][j] + _map[i + cSize][j + cSize])
            value = (value / 4) + roughness_offset(roughness)
            _map[i + h][j + h] = value

# Assigns colors based on the "height" of each point of the terrain.
# 0 to 50 = water
# 50 to 55 = sand
# 55 to 90 = grass
# 90 to 110 = mountain
# 110 or up = mountain peaks/snow
def color_assignment(value):
    if value <= 50:
        return 'blue'
    elif value > 50 and value <= 55:
        return '#FFEFD5' # Hexcode for X11 code 'Papaya Whip'
    elif value > 55 and value <= 90:
        return 'green'
    elif value > 90 and value <= 110:
        return "#808080" # gray
    else:
        return 'white'

# Returns a random roughness offset
def roughness_offset(roughness):
    return uniform(-7.0, 7.0) * roughness

# Performs the diamond-square algorithm, and converts the resulting 2D array into an image.
def img_from_diamond_square(m_size): 
    m = diamond_square(m_size)

    img = PIL.Image.new(mode="RGB", size=(m_size - 1, m_size - 1))
    for i in range(0, m_size - 1):
        for j in range(0, m_size - 1):            
            img.putpixel((i, j), ImageColor.getrgb(color_assignment(m[i][j])))
    
    return img

# Callback function that is executed whenever the "Generate Map" button is pressed.
# It generates a new map+image using the img_from_diamond_square() function and 
# replaces the existing image currently displayed, as well as updates the time
def generate_button_callback(m_size, root, imglabel, winSize, timelabel):

    size = pow(2, m_size) + 1
    
    start_time = time.time()
    img = img_from_diamond_square(size)
    end_time = time.time()

    resized_img = img.resize((winSize, winSize), PIL.Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(resized_img)

    imglabel.config(image=new_pic)
    imglabel.image = new_pic

    timelabel.config(text="Generated map and image in " + str(round(end_time - start_time, 3)) + " seconds")

main()