import pygame

import os
import random
import pygame
import sys
import math
#import ann

class Player(object):

    def __init__(self, size):
        self.rect = pygame.Rect(32, 32, size, size)
        self.size = size

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.x = pos[0]
        self.y = pos[1]


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

m = 49   #col
n = 49   #row

# Set up the display
pygame.display.set_caption("Simulation Theory")
screen = pygame.display.set_mode((m*16, n*16))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player(16) # Create the player

threshold = 8

def recursiveMaze(level, nSt, n, mSt, m, quadrant):
    global threshold
    if (n-nSt) > threshold and (m-mSt) > threshold:
        for x in range(nSt, n):
            if quadrant == 0 or quadrant == 4 or quadrant == 3:
                if x == nSt:
                    for y in range(mSt, m):
                        level[x][y] = 1           #horizontal
                if x == n - 1 and quadrant == 0:
                    for y in range(mSt, m):
                        level[x][y] = 1           #horizontal
            #else:
            outer = m - 1
            if quadrant == 0 or quadrant == 4 or quadrant == 1:
                for y in range(mSt, m):
                    if y == mSt:
                        level[x][y] = 1        #vertical
                    elif y == outer and quadrant != 4 and quadrant != 1:
                        level[x][y] = 1


        #print("Coordinates: ", nSt, (n-nSt)//2, (m-mSt)//2, m)
        level = recursiveMaze(level, nSt, nSt+((n-nSt)//2), mSt, mSt+((m-mSt)//2), 2)   #top left
        level = recursiveMaze(level, nSt, nSt+((n-nSt)//2), mSt+((m-mSt)//2), m, 1)    #top right
        level = recursiveMaze(level, nSt+((n-nSt)//2), n, mSt, mSt+((m-mSt)//2), 3)    #bottom left
        level = recursiveMaze(level, nSt+((n-nSt)//2), n, mSt+((m-mSt)//2), m, 4)     #bottom right

    return level


def pathExists(key, previous):
    global paths, final, exists
    if key == final:
        exists = True

    if key in paths.keys():
        for el in paths[key]:
            if el != previous:
                #print(key, " -> ", el)
                pathExists(el, key)


font_name = pygame.font.match_font('ubuntu')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


exists = False

"""
CONSTRUCTS A POSSIBLE MAZE TO BE SOLVED
"""
while not exists:
    level = [[0 for x in range(m)] for y in range(n)]

    level = recursiveMaze(level, 0, n, 0, m, 0)

    lofRecursion = int(math.log(m)//math.log(2) - round(math.log(threshold)/math.log(2)))
    cell_width = int(math.log(m)//math.log(2))
    cell_height = int(math.log(n)//math.log(2))


    # only 1 or 2 pls, 3 crashes the program
    probability = 1   # CONTROLS DIFFICULTY; ALSO INCREASES LOAD TIME :(
    paths = {}


    #holes in rows
    for row in range(cell_height+1, n-1, cell_height+1):  #all of the rows with walls
        i = int(row/(cell_height+1))
        for el in range(cell_width+1, m, cell_width+1):
            block = random.randint(1, cell_width)
            j = int(el/(cell_width+1))
            blk = str(i) + "," + str(j)
            passed = False
            if random.randint(0, probability) == 0:
                level[row][el-block] = 0
                passed = True
            if passed:       #means there is a WAY from (i,j) to (i+1,j)
                addThis = str(i+1) + "," + str(j)
                if blk not in paths.keys():
                    paths[blk] = [addThis]
                else:
                    (paths[blk]).append(addThis)

    #holes in cols
    level = list(map(list, zip(*level))) #transpose matrix
    for col in range(cell_width+1, m-1, cell_width+1):
        j = int(col/(cell_width+1))
        for el in range(cell_height+1, n, cell_height+1):
            block = random.randint(1, cell_height)
            i = int(el/(cell_height+1))
            blk = str(i) + "," + str(j)
            passed = False
            if random.randint(0, probability) == 0:
                level[col][el-block] = 0
                passed = True
            if passed:        #means there is a WAY from (i,j) to (i,j+1)
                addThis = str(i) + "," + str(j+1)
                if blk not in paths.keys():
                    paths[blk] = [addThis]
                else:
                    (paths[blk]).append(addThis)
    level = list(map(list, zip(*level)))

    final = str(int(n/(cell_height+1))) + "," + str(int(m/(cell_width+1)))

    pathExists("1,1", "0,0")
    #print(exists)


x = y = 0
for row in level:
    for col in row:
        if col == 1:
            Wall((x, y))
        if col == 0:
            end_rect = pygame.Rect(x, y, 16, 16)
            end_x = x
            end_y = y
        x += 16
    y += 16
    x = 0


step_size = player.size
running = True

coinImg = pygame.image.load('coin.png')
coinImg = pygame.transform.scale(coinImg, (25, 25))

playerImg = pygame.image.load('turna.jpg')
playerImg = pygame.transform.scale(playerImg, (16, 16))

xWall = []
yWall = []

for o in range(0, m, cell_width+1):
    xWall.append(o)

for o in range(0, n, cell_height+1):
    yWall.append(o)

dist_bottom = 0
dist_right = 0
dist_left = 0
dist_right = 0

for xx in range(1, len(xWall)):
    if player.rect.x < xWall[xx] and player.rect.x > xWall[xx-1]:
        dist_left = player.rect.x - xWall[xx-1]
        dist_right = xWall[xx] - player.rect.x

for yy in range(1, len(yWall)):
    if player.rect.y < yWall[yy] and player.rect.y > yWall[yy-1]:
        dist_top = player.rect.y - yWall[yy-1]
        dist_bottom = yWall[yy] - player.rect.y


stats = [dist_left-1, dist_right-1, dist_top-1, dist_bottom-1]

#print(stats)
# f = open("data.txt", "w")
# f.write("left,right,top,bottom,mov\n")
# f.close()
moves = 0

while running:

    clock.tick(10)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()

    # HUMAN CONTROL
    if key[pygame.K_LEFT]:
        moves += 1
        stats[0] = (stats[0] - 1) % cell_width
        stats[1] = (stats[1] + 1) % cell_width
        player.move(-step_size, 0)

        f = open("data.txt", "a")
        f.write(str(stats[0]) + "," + str(stats[1]) + "," + str(stats[2]) + "," + str(stats[3]) + "," + "4" + "\n")
        f.close()
    if key[pygame.K_RIGHT]:
        moves += 1
        stats[1] = (stats[1] - 1) % cell_width
        stats[0] = (stats[0] + 1) % cell_width
        player.move(step_size, 0)

        f = open("data.txt", "a")
        f.write(str(stats[0]) + "," + str(stats[1]) + "," + str(stats[2]) + "," + str(stats[3]) + "," + "2" + "\n")
        f.close()
    if key[pygame.K_UP]:
        moves += 1
        stats[2] = (stats[2] - 1) % cell_height
        stats[3] = (stats[3] + 1) % cell_height
        player.move(0, -step_size)

        f = open("data.txt", "a")
        f.write(str(stats[0]) + "," + str(stats[1]) + "," + str(stats[2]) + "," + str(stats[3]) + "," + "3" + "\n")
        f.close()
    if key[pygame.K_DOWN]:
        moves += 1
        stats[3] = (stats[3] - 1) % cell_height
        stats[2] = (stats[2] + 1) % cell_height
        player.move(0, step_size)

        f = open("data.txt", "a")
        f.write(str(stats[0]) + "," + str(stats[1]) + "," + str(stats[2]) + "," + str(stats[3]) + "," + "1" + "\n")
        f.close()


    #A.I. CONTROL
    # direction = ann.fit(stats)
    # print(stats)
    # if direction == 4:     #LEFT
    #     stats[0] = (stats[0] - 1) % cell_width
    #     stats[1] = (stats[1] + 1) % cell_width
    #     moves += 1
    #     player.move(-step_size, 0)
    # if direction == 2:     #RIGHT
    #     stats[1] = (stats[1] - 1) % cell_width
    #     stats[0] = (stats[0] + 1) % cell_width
    #     moves += 1
    #     player.move(step_size, 0)
    # if direction == 3:     #UP
    #     stats[2] = (stats[2] - 1) % cell_height
    #     stats[3] = (stats[3] + 1) % cell_height
    #     moves += 1
    #     player.move(0, -step_size)
    # if direction == 1:     #DOWN
    #     stats[3] = (stats[3] - 1) % cell_height
    #     stats[2] = (stats[2] + 1) % cell_height
    #     moves += 1
    #     player.move(0, step_size)



    if player.rect.colliderect(end_rect):   #WIN CONDITION
        raise SystemExit("You win!")

    # Draw the scene
    screen.fill((34, 47, 62))
    for wall in walls:
        pygame.draw.rect(screen, (241, 242, 246), wall.rect)
    pygame.draw.rect(screen, (34, 47, 62), end_rect)
    pygame.draw.rect(screen, (255, 159, 67), player.rect)

    screen.blit(coinImg, (end_x-8, end_y-8))
    screen.blit(playerImg, (player.rect.x, player.rect.y))

    draw_text(screen, str(moves), 50, (m*16)-36, 26)
    pygame.display.flip()
