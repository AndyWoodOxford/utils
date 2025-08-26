"""
Represents a Concept2 Ergometer 'split' - a fixed time in seconds to row 500m.
The power in watts needed to achieve the split is calculated. A instance
can be constructed from either a display string in the form 'MM:SS.n' or
a value in seconds (rounded to one decimal place).
Ref. https://www.concept2.co.uk/training/watts-calculator.
"""

import logging

class Concept2Split(object):
    SPLIT_DISTANCE = 500  # meters i.e. the split is time per 500m

    def __init__(self, split:float):
        self.split = split
        self.split_display = self._split_seconds_to_display_string(self.split)
        self.watts = self.calculate_watts()

    @classmethod
    def seconds(cls, seconds:float):
        return cls(seconds)

    @classmethod
    def display(cls, display:str):
        return cls(cls.split_display_string_to_seconds(display))

    def __repr__(self):
        return 'A %dm split of %s (%d seconds) requires a power output of %0.1f watts' % (self.SPLIT_DISTANCE, self.split_display, self.split, self.watts)

    @staticmethod
    def split_display_string_to_seconds(split):
        minutes = int(split.split(':')[0])
        seconds = float(split.split(':')[1])
        logging.debug('The split "%s" is %.1f seconds' % (split, (minutes * 60 + seconds)))
        return minutes * 60 + seconds

    def calculate_watts(self):
        pace =self.split / self.SPLIT_DISTANCE
        logging.debug('A split of %0.1f seconds corresponds to a pace of %0.4fs/m' % (self.split, pace))

        watts = 2.8 / pace ** 3
        logging.debug('A split of %0.1f seconds corresponds to a wattage of %0.1fw' % (self.split, watts))

        return watts

    @staticmethod
    def _split_seconds_to_display_string(split):
        minutes, seconds = divmod(split, 60)
        display_string = '%d:%04.1f' % (int(minutes), float(seconds))
        logging.debug('%0.1f seconds is formatted to %s' % (split, display_string))
        return display_string
