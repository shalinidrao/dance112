# This file runs the entirety of the game (if in Pyzo, press command + shift + 
# e if on Mac, or control + shift + e on PC)

# The user is able to choose a song to play the game to, end the game early if # they wish, and see high scores for their chosen song when finished. 

#pygame framework taken from Lukas Peraza
#15-112 F15 Pygame Optional Lecture, 11/11/15

import pygame
import random
import sys

from pygame.mixer import *
pygame.mixer.pre_init(47000, -16, 2, 4096)
pygame.mixer.quit()
pygame.mixer.init()

pygame.font.init()

# https://stackoverflow.com/questions/4706499/how-do-you-append-to-a-file
def appendFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)

#taken from course notes - Strings unit
def readFile(path):
    with open(path, "rt") as f:
        return f.read()


class PygameGame(object):

    def init(self):
        #moving arrows
        self.arrowGroup = pygame.sprite.Group(Arrow())
       
        #permanent arrows
        self.permanentArrowsGroup = pygame.sprite.Group(DefaultArrow(0))
        self.permanentArrowsGroup.add(DefaultArrow(1))
        self.permanentArrowsGroup.add(DefaultArrow(2))
        self.permanentArrowsGroup.add(DefaultArrow(3))
        
        #permanent arrow bounds
        self.bounds = dict()
        for arrow in self.permanentArrowsGroup:
            self.bounds[arrow.type] = [arrow.x, arrow.y, arrow.x + \
             arrow.width, arrow.y + arrow.height]
        
        self.state = "homeScreen"
        self.score = 0
        self.song = "despacito.mp3"
        
        #bounds for each button depending on the screen state
        self.buttons = dict()
        self.buttons["homeScreen"] = dict()
        self.buttons["instructions"] = dict()
        self.buttons["songChoice"] = dict()
        self.buttons["playMode"] = dict()
        self.buttons["endScreen"] = dict()
        self.buttons["highScores"] = dict()

        self.fractal = False
        self.fractalDraws = 0
   
    #if arrow is in bounds with the permanent arrows and returns points, if any
    def isInBounds(self, other):
        scoreAdd = 0
        type = other.type
        if other.x == self.bounds[type][0] and other.y == \
        self.bounds[type][1]:
            scoreAdd = 5
            self.fractal = True
        elif abs(other.y - self.bounds[type][1]) < 15:
            scoreAdd = 2
        elif abs(other.y - self.bounds[type][1]) < 30:
            scoreAdd = 1
        return scoreAdd
    
    #returns which button mouse press is in, if any
    def inButtonBounds(self, eventX, eventY):
        result = None
        for i in self.buttons[self.state]:
            x = self.buttons[self.state][i][0]
            y = self.buttons[self.state][i][1]
            w = self.buttons[self.state][i][2]
            h = self.buttons[self.state][i][3]
            
            if eventX>x and eventX<x+w and eventY>y and eventY<y+h:
                result = i
        return result
        
    def mousePressed(self, x, y):
        result = self.inButtonBounds(x, y)
        if self.state == "homeScreen":
            if result == "play":
                self.state = "instructions"
        
        elif self.state == "instructions":
            if result == "play":
                self.state = "songChoice"
        
        elif self.state == "songChoice" and result != None:
            self.setSong(result)
            self.state = "playMode"
            pygame.mixer.music.play()
            
        elif self.state == "playMode":
            if result == "end":
                pygame.mixer.music.stop()
                appendFile(self.song + ".mp3.txt", "\n" + str(self.score))
                self.state = "endScreen"
        
        elif self.state == "endScreen":
            if result == "highscores":
                self.state = "highScores"
            elif result == "playagain":
                self.state = "homeScreen"
                self.init()
        
        elif self.state == "highScores":
            if result == "playagain":
                self.state = "homeScreen"
                self.init()
        
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_LEFT or keyCode == pygame.K_DOWN or \
            keyCode == pygame.K_UP or keyCode == pygame.K_RIGHT:
            for arrow in self.arrowGroup:
                #only give points if correct arrow key was pressed
                if (arrow.type == 0 and keyCode == pygame.K_LEFT) or \
                (arrow.type == 1 and keyCode == pygame.K_DOWN) or \
                (arrow.type == 2 and keyCode == pygame.K_UP) or \
                (arrow.type == 3 and keyCode == pygame.K_RIGHT):
                    scoreAdd = self.isInBounds(arrow)
                    if scoreAdd > 0:
                        self.score += scoreAdd
                        self.arrowGroup.remove(arrow)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt, calls):
        if self.state == "playMode":
            self.arrowGroup.update(self.width, self.height)
            for arrow in self.arrowGroup:
                if arrow.rect.bottom < 0:
                    self.arrowGroup.remove(arrow)
            if calls % 15 == 0:
                self.arrowGroup.add(Arrow())
                
            #end game if song is over
            if not pygame.mixer.music.get_busy():
                appendFile(self.song + ".mp3.txt", "\n" + str(self.score))
                self.state = "endScreen"
                
    def redrawAll(self, screen):
        myFont = pygame.font.SysFont("Arial", 50)
        scoreFont = pygame.font.SysFont("Arial", 35)
        bigFont = pygame.font.SysFont("Arial", 80)
        
        if self.state == "homeScreen":
            
            screen.fill((0,0,0))
            welcome = pygame.transform.scale(pygame.image.load\
                    ('welcometowhite.png').convert_alpha(), (325, 70))
            
            titleImage = pygame.transform.scale(pygame.image.load\
                    ('dance112title.png').convert_alpha(), (500, 150))
            playButton = pygame.transform.scale(pygame.image.load\
                    ('playbutton.png').convert_alpha(), (150, 100))
            screen.blit(welcome, (150, 150))
            screen.blit(titleImage, (50, 230))
            screen.blit(playButton, (225, 400))
            
            #play button
            self.buttons["homeScreen"]["play"] = [225, 400, 150, 100]
            
        elif self.state == "instructions":
            
            screen.fill((0, 0, 0))
            
            instructionsImage = pygame.transform.scale(pygame.image.load\
                    ('instructionswhite.png').convert_alpha(), (500, 80))
            instructions2 = myFont.render("Use the arrow keys to press",\
             False, (255, 255, 255))
            instructions3 = myFont.render("an arrow when it reaches the top",\
            False, (255, 255, 255))            
            playButton2 = pygame.transform.scale(pygame.image.load\
                    ('playbutton2.png').convert_alpha(), (200, 100))
                    
            screen.blit(instructionsImage, (50, 150))
            screen.blit(instructions2, (70, 250))
            screen.blit(instructions3, (40, 300))
            screen.blit(playButton2, (200, 400))
            
            #play button
            self.buttons[self.state]["play"] = [200, 400, 200, 100]
            
        elif self.state == "songChoice":
            
            screen.fill((0, 0, 0))
            songName1 = pygame.transform.scale(pygame.image.load\
                    ('despacitotitlewhite.png').convert_alpha(), (300, 60))
            songName2 = pygame.transform.scale(pygame.image.load\
                    ('sweetcarolinetitlewhite.png').convert_alpha(), \
                    (300, 60))
            songName3 = pygame.transform.scale(pygame.image.load\
                    ('shutupanddancetitlewhite.png').convert_alpha(), \
                    (300, 60))
            songName4 = pygame.transform.scale(pygame.image.load\
                    ('dancingqueentitlewhite.png').convert_alpha(), \
                    (300, 60))
                    
            songName5 = pygame.transform.scale(pygame.image.load\
                    ('workthisbodytitlewhite.png').convert_alpha(), (300, 60))
                    
            chooseYourSong = pygame.transform.scale(pygame.image.load\
                    ('chooseyoursong.png').convert_alpha(), (500, 70))

            screen.blit(chooseYourSong, (50, 15))
            screen.blit(songName1, (150, 100))
            screen.blit(songName2, (150, 200))
            screen.blit(songName3, (150, 300))
            screen.blit(songName4, (150, 400))
            screen.blit(songName5, (150, 500))
            
            #song buttons
            self.buttons[self.state]["despacito"] = [150, 100, 300, 60]
            self.buttons[self.state]["sweetcaroline"] = [150, 200, 300, 60]
            self.buttons[self.state]["shutupanddance"] = [150, 300, 300, 60]
            self.buttons[self.state]["dancingqueen"] = [150, 400, 300, 60]
            self.buttons[self.state]["workthisbody"] = [150, 500, 300, 60]
            
        elif self.state == "playMode":
            
            self.permanentArrowsGroup.draw(screen)
            self.arrowGroup.draw(screen)
            scoreDisplay = scoreFont.render("Score: " + str(self.score),\
             False, (0, 0, 0))
            screen.blit(scoreDisplay,(10, 10))
            
            endGame = pygame.transform.scale(pygame.image.load\
                    ('endgame.png').convert_alpha(), (115, 30))
            screen.blit(endGame, (475, 5))
            
            #end game button
            self.buttons[self.state]["end"] = [480, 5, 130, 30]
            
            #if user hits arrow key at perfect time, a fractal is drawn
            if self.fractal == True:
                self.drawFractal(screen, 50, 100, 20, 1)
                self.fractalDraws += 1
                if self.fractalDraws == 100:
                    self.fractal = False
                    self.fractalDraws = 0
            
        elif self.state == "endScreen":

            screen.fill((255, 0, 0))

            gameOver = pygame.transform.scale(pygame.image.load\
                    ('gameover.png').convert_alpha(), (400, 80))
            screen.blit(gameOver, (100, 150))
            
            yourScore = pygame.transform.scale(pygame.image.load\
                    ('yourscore.png').convert_alpha(), (300, 50))
            screen.blit(yourScore, (110, 250))
            score = bigFont.render(": " + str(self.score), False, (0, 0, 0))
            screen.blit(score, (430, 250))
            
            playAgain = pygame.transform.scale(pygame.image.load\
                    ('playagainbutton.png').convert_alpha(), (250, 75))
            screen.blit(playAgain, (175, 350))
            
            highScores = pygame.transform.scale(pygame.image.load\
                    ('highscoresbutton.png').convert_alpha(), (250, 75))
            screen.blit(highScores, (175, 450))
            
            #high score and play again buttons
            self.buttons[self.state]["playagain"] = [175, 350, 250, 75]
            self.buttons[self.state]["highscores"] = [174, 450, 250, 75]
        
        elif self.state == "highScores":
            
            screen.fill((0, 0, 255))
    
            highScoresFor = pygame.transform.scale(pygame.image.load\
                    ('highscores.png').convert_alpha(), (400, 150))
            screen.blit(highScoresFor, (100, 25))
            
            highScoreSong = pygame.transform.scale(pygame.image.load \
                    (self.song + 'titlewhite.png').convert_alpha(), \
                    (350, 75))
            screen.blit(highScoreSong, (125, 180))
            
            #read and sort all scores for song that was just played
            highScores = readFile(self.song + ".mp3.txt").splitlines()
            highNums = []
            for score in highScores:
                if score.isnumeric():
                    highNums.append(int(score))
            highNums = sorted(highNums)
            
            #display highest 3 scores of the song
            hs2 = myFont.render("1. " + str(highNums[-1]), False, (0, 0, 0))
            hs3 = myFont.render("2. " + str(highNums[-2]), False, (0, 0, 0))
            hs4 = myFont.render("3. " + str(highNums[-3]), False, (0, 0, 0))
          
            screen.blit(hs2, (200, 300))
            screen.blit(hs3, (200, 350))
            screen.blit(hs4, (200, 400))
            
            
            playAgain = pygame.transform.scale(pygame.image.load\
                    ('playagainbutton.png').convert_alpha(), (250, 75))
            screen.blit(playAgain, (175, 450))
            
            #play again button
            self.buttons[self.state]["playagain"] = [175, 450, 250, 75]
            
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=600, fps=50, title="Dance112"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (158, 131, 234)
        pygame.init()
    
    #obtain bpm for chosen song and set frame speed
    def setSong(self, song):
        self.song = song
        self.setSpeed()
        pygame.mixer.music.load(self.song + ".mp3")
        
    def setSpeed(self):
        songs = readFile("songs.txt")
        for s in songs.splitlines():
            if self.song in s:
                bpm = float(s.split(",")[1])
        self.fps = 6000//bpm
    
    def drawFractal(self, screen, xc, yc, r, level):
        hyp = int(2**0.5 * r)
        arrowImage = pygame.transform.scale(pygame.image.load\
        ('ddrarrow.png').convert_alpha(),(r, r))
        if level == 0:
    
            arrowImage = pygame.transform.scale(pygame.image.load\
            ('ddrarrow.png').convert_alpha(),(r, r))
            screen.blit(pygame.transform.rotate(arrowImage, 45), \
            (xc - r, yc - r)) 
            screen.blit(pygame.transform.rotate(arrowImage, 135), \
            (xc - r, yc + r)) 
            screen.blit(pygame.transform.rotate(arrowImage, -45), \
            (xc + r, yc - r)) 
            screen.blit(pygame.transform.rotate(arrowImage, -135), \
            (xc + r, yc + r)) 
            
        else:
            
            screen.blit(pygame.transform.rotate(arrowImage, 45), \
            (xc - r, yc - r)) 
            screen.blit(pygame.transform.rotate(arrowImage, 135), \
            (xc - r, yc + r)) 
            screen.blit(pygame.transform.rotate(arrowImage, -45), \
            (xc + r, yc - r)) 
            screen.blit(pygame.transform.rotate(arrowImage, -135), \
            (xc + r, yc + r))
           
            self.drawFractal(screen, xc - 2*r, yc - 2*r, r // 2, level - 1)
            self.drawFractal(screen, xc + 2*r, yc - 2*r, r // 2, level - 1)
            self.drawFractal(screen, xc - 2*r, yc + 2*r, r // 2, level - 1)
            self.drawFractal(screen, xc + 2*r, yc + 2*r, r // 2, level - 1)
        
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        
        # call game-specific initialization
        self.init()
        timerCalls = 0
        playing = True
        while playing:
            time = clock.tick(self.fps)
            timerCalls += 1
            self.timerFired(time, timerCalls)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Class to create new moving arrows
## Arrows ##
class Arrow(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Arrow.arrowImage = pygame.transform.scale(
            pygame.image.load('ddrarrow.png').convert_alpha(),
            (80, 80))
    
    def __init__(self):
        Arrow.init()
        super(Arrow, self).__init__()
        self.type = random.randint(0, 3)
        self.image = self.getImage()
        self.width, self.height = self.image.get_size()
        self.x, self.y = self.getCoordinates()
        self.speed = 5
        self.updateRect()

    def getCoordinates(self):
        margin = 150
        return (margin + self.type*100, 600)
    
    def getImage(self):
        image = None
        if self.type == 0:
            image = pygame.transform.rotate(Arrow.arrowImage, 90)
        elif self.type == 1:
            image = pygame.transform.rotate(Arrow.arrowImage, 180)
        elif self.type == 2:
            image = Arrow.arrowImage
        elif self.type == 3:
            image = pygame.transform.rotate(Arrow.arrowImage, -90)
        return image
            
    def draw(self, screen):
        self.image.draw(screen)
    
    def update(self, screenWidth, screenHeight):
        self.y -= self.speed
        if self.rect.bottom < 0:
            self.y += screenHeight + self.height
        self.updateRect()
    
    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        
#Class for the permanent arrows at the top of the screen
class DefaultArrow(pygame.sprite.Sprite):
    @staticmethod
    def init():
        DefaultArrow.image = pygame.transform.scale(
            pygame.image.load('colorarrow3.png'),
            (80, 80))
    
    def __init__(self, type):
        DefaultArrow.init()
        super(DefaultArrow, self).__init__()
        self.type = type
        self.image = self.getImage()
        self.width, self.height = self.image.get_size()
        self.x, self.y = self.getCoordinates()
        self.speed = 5
        self.updateRect()

    def getCoordinates(self):
        margin = 150
        return (margin + self.type*100, self.height//2)
    
    def getImage(self):
        image = None
        if self.type == 0:
            image = pygame.transform.rotate(DefaultArrow.image, 180)
        elif self.type == 1:
            image = pygame.transform.rotate(DefaultArrow.image, -90)
        elif self.type == 2:
            image = pygame.transform.rotate(DefaultArrow.image, 90)
        elif self.type == 3:
            image = DefaultArrow.image
        return image
            
    def draw(self, screen):
        self.image.draw(screen)
    
    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

  
def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()


