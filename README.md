# PacMan.exe
This is a 3D horror game made with python. It uses [PyGame](https://www.pygame.org/) library and [Ray Casting](https://ru.wikipedia.org/wiki/Ray_casting) technology. I made it in one week. I would not mind if you tried it and appreciated

![](readme_media/frame1.png)

![](readme_media/img.png)

## Requirements
* Git
* Python 3.9
* Pip

## Installation
Create a new folder and open it in terminal

Then enter this command to clone my repository
```
git clone https://github.com/Olzeev/PacManExe.git
```
Go to 'PacMacExe' folder
```commandline
cd PacManExe
```
Also you may need to install some libraries:
```commandline
pip install pygame
pip install keyboard
```
Now you can start the game
```commandline
python3 main.py
```
or 
```
python main.py
```

## Change game parameters

In 'const' file you can change some game params.
```commandline
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FPS = 40

FOV = 90
TILE_SIZE = 100
RAY_LENGTH = TILE_SIZE * 10
RAYS_AMOUNT = int(WIDTH / 15)
WALL_HEIGHT = int(HEIGHT * 0.8)
DISTANCE_TO_SCREEN = 100
SENSITIVITY = 0.3
```

I don't recommend to change 'TILE_SIZE', 'WALL_HEIGHT' and 'DISTANCE_TO_SCREEN' variables.
They are critical to the proper functioning of the game. Feel free to change other.
Remember that 'RAYS_AMOUNT' must be a divider of 'WIDTH' variable.