
# Diamond-Square Terrain Generator
#### Procedurally generates terrain using the [Diamond-Square algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)


#### Prerequisites
 * Python 3.6 or up
 * `PIL`, `tkinter` libraries

#### test.py

![The program](https://cdn.discordapp.com/attachments/690652979036028929/838970063301640213/unknown.png)

The image at the top is the terrain. Blue represents water, peach is sand, green is grass, gray is rocks/mountains, and white is snow/mountain peaks. Each image is generated uniquely, so you will get something different when running it. 

(Gif sped up 3x to show terrain generation)

![New terrain generated at the push of a button. Sped up 3x for the purpose of showing the terrain.](https://cdn.discordapp.com/attachments/690652979036028929/839327224724848700/button2.gif)

The "Map Size" slider allows the user to adjust the size of the terrain, with the image size being 2^(slider value) + 1. The slider goes from 1 to 20, meaning that the image size can be 3 by 3 to 1,048,577 by 1,048,577. Be warned, the amount of time it takes to generate maps with successive map heights increases exponentially. 
