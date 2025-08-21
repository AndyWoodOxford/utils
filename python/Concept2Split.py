
import logging
import re

class Concept2Split(object):
    def __init__(self, split:float):
        self.split = split
        self.watts = self.calculate_watts()

    def __init__(self, split:str):
        self.__init__(self.split_string_to_seconds(split))

    @staticmethod
    def split_seconds_to_string(split):
        minutes, seconds = divmod(split, 60)
        split_string = '%d:%04.1f' % (int(minutes), float(seconds))
        logging.debug('%0.1f seconds is formatted to %s' % (split, split_string))
        return split_string

    @staticmethod
    def split_string_to_seconds(split):
        minutes = int(split.split(':')[0])
        seconds = float(split.split(':')[1])
        logging.debug('The split "%s" is %.1f seconds' % (split, (minutes * 60 + seconds)))
        return minutes * 60 + seconds

    def calculate_watts(self):
        pace =self.split / SPLIT_DISTANCE
        logging.debug('A split of %0.1f seconds corresponds to a pace of %0.4fs/m' % (self.split, pace))

        self.watts = 2.8 / pace ** 3
        logging.debug('A split of %0.1f seconds corresponds to a wattage of %0.1fw' % (self.split, self.watts))
