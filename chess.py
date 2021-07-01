import pygame
from pygame import draw
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import reference
import firebase_admin
from firebase_admin import db
from pygame.locals import(
    KEYDOWN,
    QUIT,
)
import random

ref = db.reference()
ref.update({"turn": "W"})

def bishopPossible (board, y, x, iterY, iterX, possible, team):
    global possibleTake

    y += iterY
    x += iterX

    if len(board) > y and len(board[y]) > x and x >= 0 and y >= 0:
        if board[y][x] == "N":
            possible.append([y,x])
            return bishopPossible(board, y, x, iterY, iterX, possible, team)
        else:
            if board[y][x][0] != team:
                possibleTake.append([y,x])
    return possible


def kingPossible (board, y, x, possible, team):
    global possibleTake

    for iterY in [-1,1,0]:
        for iterX in [-1,1,0]:
            
            if iterY == 0 and iterY == iterX:
                continue

            newY = y + iterY
            newX = x + iterX

            if len(board) > newY and len(board[y]) > newX and newX >= 0 and newY >= 0:
                if board[newY][newX] == "N":
                    possible.append([newY,newX])
                else:
                    if board[newY][newX][0] != team:
                        possibleTake.append([newY,newX])
    
    return possible

def horsePossible (board, y, x, possible, team):
    global possibleTake
    for iterY in [-1,1,2,-2]:
        for iterX in [-1, 1, 2, -2]:
            if abs(iterY) == abs(iterX):
                continue
            
            newY = y + iterY
            newX = x + iterX

            if len(board) > newY and len(board[y]) > newX and newX >= 0 and newY >= 0:
                if board[newY][newX] == "N":
                    possible.append([newY,newX])
                else:
                    if board[newY][newX][0] != team:
                        possibleTake.append([newY,newX])
    
    return possible



pygame.init()
font = pygame.font.SysFont('Arial', 12)

alph = "ABCDEFGH"

size = width, height = 740, 740

root = pygame.display.set_mode(size)

running = True

startX = 20
startY = 20

colours = [(21, 0, 43), (255,255,255)]

chosingSides = True

board = [
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
    ['N','N','N','N','N','N','N','N'],
]

w1 = ['WR1','WH1','WB1','WQ','WK','WB2','WH2','WR2']
w2 = ['WP1','WP2','WP3','WP4','WP5','WP6','WP7','WP8']
b1 = ['BR1','BH1','BB1','BK','BQ','BB2','BH2','BR2']
b2 = ['BP1','BP2','BP3','BP4','BP5','BP6','BP7','BP8']

board[-1] = w1
board[-2] = w2
board[0] = b1[::-1]
board[1] = b2[::-1]

mousePressed = False
hoveredPeice = None
hoveredPossible = None
selectedPeice = None

ref.update({"board": board})

possibleColour = (75, 139, 242)
possibleTakeColour = (232, 50, 30)
selectedColour = (75, 242, 158)

possible = []
possibleTake = []

sideSelected = "W"

Qcount = 2

def flipBoard (board):
    flipped = []
    for row in board[::-1]:
        flipped.append(row[::-1])
    
    return flipped


flippedBoard = flipBoard(board)


if sideSelected == "B":
    oppositeSide = "W"
    ref.update({"side": "W"})
    board = flippedBoard

else:
    oppositeSide = "B"
    ref.update({"side": "B"})

turn = False

info = ref.get()

while running:
    if turn == False:
        info = ref.get()

        if info['turn'] == sideSelected:
            turn = True

    if sideSelected == "B":
        board = flipBoard(info['board'])
    else:
        board = info['board']
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if turn:
                    if hoveredPeice != None or hoveredPossible != None:
                        mousePressed = True
                    else:
                        selectedPeice = None
                        possible = []
                        possibleTake = []
        
    root.fill((200,200,200))

    hoveredPeice = None
    hoveredPossible = None
    for y in range (8):
        if y%2 == 1:
            main = colours[1]
            second = colours[0]
        else:
            main = colours[0]
            second = colours[1]
        
        rowNum = font.render(str(abs(7 - y) + 1), True, (0,0,0))
        root.blit(rowNum, (5, 55 + 90 * y))

        currRow = board[y]
        
        for x in range (8):
            peice = currRow[x]

            if (y,x) == selectedPeice:
                currColour = selectedColour
                multiplier = 1

                if "P" == peice[1]:

                    if y > 0 and y < 7:
                        if "N" == board[y-(1*multiplier)][x]:
                            possible.append([y-(1*multiplier),x])
                            if y == 6:
                                if "N" == board[y-(2*multiplier)][x]:
                                    possible.append([y-(2*multiplier),x])

                        if x > 0:
                            if peice[0] != board[y-(1*multiplier)][x-1][0] and "N" != board[y-(1*multiplier)][x-1]:
                                possibleTake.append([y-(1*multiplier), x-1])
                        
                        if x < 7:
                            if peice[0] != board[y-(1*multiplier)][x+1][0] and "N" != board[y-(1*multiplier)][x+1]:
                                possibleTake.append([y-(1*multiplier), x+1])

                elif "B" == peice[1]:
                    for a in [-1, 1]:
                        for b in [-1, 1]:
                            possible = bishopPossible(board, y, x, a, b, possible, peice[0])
                
                elif "R" == peice[1]:
                    for a in [0,1]:
                        for b in [-1, 1]:
                            possible = bishopPossible(board, y, x, b * a, b * (1-a), possible, peice[0])
                
                elif "Q" == peice[1]:
                    for a in [0,1]:
                        for b in [-1, 1]:
                            possible = bishopPossible(board, y, x, b * a, b * (1-a), possible, peice[0])
                    for a in [-1, 1]:
                        for b in [-1, 1]:
                            possible = bishopPossible(board, y, x, a, b, possible, peice[0])

                elif "K" == peice[1]:
                    possible = kingPossible(board, y, x ,possible, peice[0])
                
                elif "H" == peice[1]:
                    possible = horsePossible(board, y, x, possible, peice[0])

            elif [y,x] in possibleTake:
                currColour = possibleTakeColour   

            else:
                if x%2 == 1:
                    currColour = main
                else:
                    currColour = second
            
            coloumnLetter = font.render(alph[abs(x)], True, (0,0,0))
            root.blit(coloumnLetter, (65 + 90 * x, 3))

            draw.rect(root, currColour, (startX + 90 * x, startY + 90 * y, 90, 90))

            if [y,x] in possible:
                draw.circle(root, possibleColour, (startX + 45 + 90 * x, startY + 45 + 90 * y), 15)

            peiceColor = (0,0,0)
            if peice != 'N':
                if "W" == peice[0]:
                    peiceColor = (255,255,255)
                    fileDir = "./White/"
                else:
                    fileDir = "./Black/"
                
                PeiceType = peice[1]
                if "P" == PeiceType:
                    fileDir += "Pawn"

                    if peice[0] == "B":
                        if y == 7:
                            Qcount += 1
                            board[y][x] = f"BQ{Qcount}"
                    
                    if peice[0] == "W":
                        if y == 0:
                            Qcount += 1
                            board[y][x] = f"WQ{Qcount}" 
                    
                elif "B" == PeiceType:
                    fileDir += "Bishop"
                
                elif "H" == PeiceType:
                    fileDir += "Horse"
                
                elif "K" == PeiceType:
                    fileDir += "King"
                
                elif "Q" == PeiceType:
                    fileDir += "Queen"
                
                elif "R" == PeiceType:
                    fileDir += "Rook"

                peiceImg = pygame.image.load(f"{fileDir}.png")
                peiceImgRect = peiceImg.get_rect()
                peiceImgRect.topleft = (startX + 90 * x, startY + 90 * y)
                if peiceImgRect.collidepoint(pygame.mouse.get_pos()):
                    hoveredPeice = (y,x)
                    if mousePressed:
                        if selectedPeice != hoveredPeice:
                            if sideSelected == peice[0]:
                                selectedPeice = hoveredPeice
                                possible = []
                                possibleTake = []
                        if [y,x] not in possibleTake:
                            mousePressed = False

                root.blit(peiceImg, peiceImgRect)
            
            
            if [y,x] in possible or [y,x] in possibleTake:
                possibleRect = pygame.Rect(startX + 90 * x, startY + 90 * y, 90, 90)
                if possibleRect.collidepoint(pygame.mouse.get_pos()):
                    hoveredPossible = (y,x)
                    if mousePressed:
                        board[y][x] = board[selectedPeice[0]][selectedPeice[1]]
                        board[selectedPeice[0]][selectedPeice[1]] = "N" 
                        possible = []
                        possibleTake = []     
                        selectedPeice = None
                        mousePressed = False
                        
                        
                        if sideSelected == "B":
                            ref.update({"board": flipBoard(board)})
                        else:
                            ref.update({"board": board})
                        turn = False     
                        ref.update({"turn": oppositeSide})

            

    pygame.display.update()