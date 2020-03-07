import json
import numpy as np

""" Level: represents a game level from Roll the Block """

class Level:
    def __init__(self, level_number):
        self.loadLevel('./levels/{}.json'.format(level_number))

    def loadLevel(self, path_to_level):
        self.files = open(path_to_level, "r")
        jsonObj = json.loads(self.files.read())

        self.map =  np.asarray(jsonObj["map"])
        self.level = jsonObj["level"]

        self.size = jsonObj["size"]

        self.start = jsonObj["start"]
        self.start.reverse()

        self.end = jsonObj["end"]
        self.end.reverse()

    def is_tile_available(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size and self.map[y][x] == 1
