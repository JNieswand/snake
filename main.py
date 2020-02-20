#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:33:25 2020

@author: jacob
"""
import numpy as np
import copy
import time
import matplotlib.pyplot as plt
global SIZE_X, SIZE_Y
SIZE_X = 20
SIZE_Y = 20

def is_direction_valid(new_direction, old_direction):
    if (new_direction =="up" and old_direction == "down" 
        or new_direction =="down" and old_direction== "up"
        or new_direction =="left" and old_direction == "right" 
        or new_direction =="right" and old_direction == "left" ):
        return False
    else: 
        return True

class Coordinate:
    def __init__(self,x, y):
        self.x = x
        self.y = y
    def is_equal(self, coordinate):
        return self.x == coordinate.x and self.y == coordinate.y
class Board:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.array = np.array((size_x, size_y))

class Snake:
    def __init__(self, length, position):
        self.length = length
        self.coordinates = self.initiate_coordinates(position)
        self.growing_next_move = False
    def initiate_coordinates(self, position):
        return np.array([Coordinate(position.x, position.y + k) for k in np.arange(self.length)])
    def move(self, direction):
        new_coordinate = copy.deepcopy(self.coordinates[0])
        if direction == "up":
            new_coordinate.y -= 1
        elif direction == "down":
            new_coordinate.y += 1
        elif direction == "left":
            new_coordinate.x -= 1
        elif direction == "right":
            new_coordinate.x += 1
        else:
            print("unknown direction Parameter")
            return False
        if new_coordinate.is_equal(self.coordinates[1]):
            print("Cannot go backwards!")
            return False
        
        new_coordinate.x = new_coordinate.x % SIZE_X
        new_coordinate.y = new_coordinate.y % SIZE_Y
        if not self.growing_next_move:
            self.coordinates = np.delete(self.coordinates, -1)
        else:
            self.growing_next_move = False
        self.coordinates = np.insert(self.coordinates, 0, new_coordinate)
        return True
    def grow(self):
        self.growing_next_move = True
    def is_dead(self):
        for coordinate in self.coordinates[1:]:
            if coordinate.is_equal(self.coordinates[0]):
                return True
        return False
    def collides_with(self,apple):
        for coordinate in self.coordinates:
            if apple.coordinate.is_equal(coordinate):
                return True
        return False
class Apple:
    def __init__(self, coordinate):
        self.coordinate = coordinate
class Drawer:
    def __init__(self, board, snake, apple):
        self.board = board
        self.snake = snake
        self.apple = apple
        self.draw_array = np.zeros((self.board.size_x, self.board.size_y))
        self.fig = plt.figure()
        
        self.ax = self.fig.add_subplot(111)
        self.draw()
    def draw(self):
        self.ax.clear()
        self.draw_array = np.zeros((self.board.size_x, self.board.size_y))
        for coordinate in self.snake.coordinates:
            self.draw_array[coordinate.x, coordinate.y] += 1
        self.draw_array[self.apple.coordinate.x, self.apple.coordinate.y] += 0.6
        self.ax.imshow(np.swapaxes(self.draw_array, 0, 1), cmap = "Reds", vmax = "2")
        plt.show() 
        self.fig.canvas.draw()
    def connect_clickevent(self, onpress):
        self.fig.canvas.mpl_connect('key_press_event', onpress)
    def message_loose(self):
        self.ax.set_title("GAME OVER")
        
class Game:
    def __init__(self):
        self.board = Board(SIZE_X, SIZE_Y)
        self.snake = Snake(6, Coordinate(int(SIZE_X/2), int(SIZE_Y/2))) 
        self.apple = Apple(Coordinate(0,0))
        self.respawn_apple()
        self.drawer = Drawer(self.board, self.snake, self.apple)
        self.drawer.connect_clickevent(self.onpress)
        self.direction = "up"
        self.game_over = False
        self.input_cue = np.array([])
           
    def update(self):
        if(self.snake.collides_with(self.apple)):
            self.snake.grow()
            self.respawn_apple()
        print(self.input_cue)
        if self.input_cue.size > 0:
            self.snake.move(self.input_cue[0])
            self.direction = copy.deepcopy(self.input_cue[0])
            self.input_cue = np.delete(self.input_cue, 0)
        else:
            self.snake.move(self.direction)
        print(self.apple.coordinate.x)
        print(self.apple.coordinate.y)
        self.drawer.draw()
        
    
    def respawn_apple(self):
        while(True):
            self.apple.coordinate = Coordinate(np.random.randint(0, SIZE_X), np.random.randint(0, SIZE_Y))
            if not self.snake.collides_with(self.apple):
                break

    def lost():
        self.drawer.message_loose()
    
    def onpress(self, event):
        direction_to_validate_against = self.direction
        if self.input_cue.size >0:
            direction_to_validate_against = self.input_cue[-1]
        if (is_direction_valid(event.key, direction_to_validate_against)):
            self.input_cue = np.append(self.input_cue, event.key)    
        

if __name__ == "__main__":
    game = Game()
    game.update()
    while (not game.snake.is_dead()):
        plt.pause(0.15)
        game.update()

    game.lost()
   