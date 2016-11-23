#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   List of decision classes
#

from collections import defaultdict
from enums import Direction
import pygame
import sys


class Basic(object):
    """ Base class for all decision classes """

    def turnLeft(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.LEFT)

    def turnRight(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.RIGHT)

    def turnUp(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.UP)

    def turnDown(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.DOWN)

    def noTurn(self, currentPosition):
        """ No turn associated with that decision """
        return

    def waitForDecision(self, currentPosition):
        """ DEFAULT: Do nothing """
        return


class Stationary(Basic):
    """ Decision class for a Stationary player """

    def turn(self, currentPosition):
        return



class KeyInput(Basic):
    """ Decision class for keyboard inputs

    Attributes:
        directions: Map of key inputs to methods

    @TODO: Simply using getch.getch() blocks the other 
        thread until a keyboard until a character is read.
    """

    def __init__(   self, 
                    upKey       = pygame.K_UP, 
                    downKey     = pygame.K_DOWN,
                    leftKey     = pygame.K_LEFT, 
                    rightKey    = pygame.K_RIGHT):

        self.__directions   = defaultdict(
            lambda: self.noTurn,
            {
                leftKey  : self.turnLeft,
                rightKey : self.turnRight,
                upKey    : self.turnUp,
                downKey  : self.turnDown
            }
        )

    def waitForDecision(self, currentPosition):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.turn(currentPosition, event.key)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            """ 20 frames per second """
            clock.tick(20)
                

    def turn(self, currentPosition, keyPressed):
        return self.__directions[keyPressed](currentPosition)


class MouseInput(Basic):
    """ Decision class for mouse input

     Attributes:
        directions: Map of tuples to decision methods
            (colIsLarger, isPositive) is the pattern
                Ex: Turn left if the column difference is larger 
                    AND its negative
    """

    def __init__(self):
        self.__directions   = defaultdict(
            lambda: self.noTurn,
            {
                (1, 0)  : self.turnLeft,
                (1, 1)  : self.turnRight,
                (0, 0)  : self.turnUp,
                (0, 1)  : self.turnDown
            }
        )

    def waitForDecision(self, currentPosition):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.turn(currentPosition, event.pos)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            """ 20 frames per second """
            clock.tick(20)       

    def turn(self, currentPosition, mousePosition):
        (col, row) = currentPosition.getCenter()
        (mouseCol, mouseRow) = mousePosition

        colLarger = (abs(mouseCol - col)) > (abs(mouseRow - row))
        if colLarger:
            return self.__directions[(1, mouseCol - col > 0)](currentPosition)

        return self.__directions[(0, mouseRow - row > 0)](currentPosition)




class AIInput(Basic):
    """ Decision class for AI input (auto-move) """

    def turn(self, currentPosition):
        print("ai move")