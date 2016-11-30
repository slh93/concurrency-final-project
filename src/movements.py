#!/usr/bin/env python

#   movements.py
#
#   Sam Heilbron
#   Last Updated: November 30, 2016
#
#   List of movement classes

from enums import Direction, Color
import threading
import pygame

class _Circle(object):
    """A Circle. Class for circle positions.

    Attributes:
        pixels: List of pixel coordinates.
        size: The size of the sphere.
    """

    def __init__(self, initialCenter, initialRadius = 1):
        self.__center           = initialCenter
        self.__radius           = initialRadius
        self.__direction        = Direction.STAY
        self.__directionMutex   = threading.Lock()

        self.__directions       = dict(
            {
                Direction.LEFT  : self.goLeft,
                Direction.RIGHT : self.goRight,
                Direction.UP    : self.goUp,
                Direction.DOWN  : self.goDown,
                Direction.STAY  : self.stayInPlace
            })


    ##########################   GETTERS   ##########################

    def getCenter(self):
        return self.__center

    def getRadius(self):
        return self.__radius

    def getCurrentDirection(self):
        with self.__directionMutex:
            direction = self.__direction
        return direction


    ##########################   SETTERS   ##########################

    def setCurrentDirection(self, direction):
        with self.__directionMutex:
            self.__direction = direction


##
##  Change how the movemnt is handled
##  Shouldn't be able to move if ANY of the pixels will go 
##  less than 0 or greater than max
##
    def move(self, gameboard):
        self.__directions[self.getCurrentDirection()](gameboard)
        self.checkCollisions(gameboard)

    def draw(self, color):  
        pygame.draw.circle(
            pygame.display.get_surface(), 
            color, 
            self.__center, 
            self.__radius)

    def goLeft(self, gameboard):
        """ Move left """
        (col, row) = self.__center
        gameboard.getLocks()[row][col].release()
        if (col - (self.__radius + 1)) >= 0:
            self.__center = (col - 1, row)
        else:
            self.__center = (col, row) 
        (col, row) = self.__center
        gameboard.getLocks()[row][col].acquire()

    def goRight(self, gameboard):
        """ Move right """
        (col, row) = self.__center
        gameboard.getLocks()[row][col].release()
        self.__center = (col + 1, row)
        (col, row) = self.__center
        gameboard.getLocks()[row][col].acquire()

    def goUp(self, gameboard):
        """ Move up """
        (col, row) = self.__center
        gameboard.getLocks()[row][col].release()
        if (row - (self.__radius + 1)) >= 0:
            self.__center = (col, row - 1)
        else:
            self.__center = (col, row)
        (col, row) = self.__center
        gameboard.getLocks()[row][col].acquire()

    def goDown(self, gameboard):
        """ Move down """
        (col, row) = self.__center
        gameboard.getLocks()[row][col].release()
        self.__center = (col, row + 1)
        (col, row) = self.__center
        gameboard.getLocks()[row][col].acquire()

    def stayInPlace(self, gameboard):
        """ Stay in place """
        return

    def checkCollisions(self, gameboard):
        """ Go through all pixels in player's radius and check for a collision """
        (centerCol, centerRow) = self.__center
        (width, height) = gameboard.getDimensions()
        for col in range(centerCol - self.__radius, centerCol + self.__radius):
            if col < 0 or col > height:
                continue
            for row in range(centerRow - self.__radius, centerRow + self.__radius):
                if row < 0 or row > width:
                    continue
                elif gameboard.getLocks()[row][col].locked() and (col, row) != self.__center:
                    print "Collision occured at", col, row


###
###self.__pixels =[(max(0,row-1),col) for (row,col) in self.__pixels]
###


