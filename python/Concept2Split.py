"""
Represents a Concept2 Ergometer 'split' - a fixed time in seconds to row 500m.
The power in watts needed to achieve the split is calculated. A instance
can be constructed from either a display string in the form 'MM:SS.n' or
a value in seconds (rounded to one decimal place).
Ref. https://www.concept2.co.uk/training/watts-calculator.
"""

import re

class Split(object):
    COLUMN_WIDTH = 13     # display tabulation
    SPLIT_DISTANCE = 500  # meters i.e. the split is time per 500m
    SPLIT_DISPLAY_REGEX = '^(\\d)+:(\\d){1,2}(\\.)?(\\d)?$' # e.g. '1:45.1'

    def __init__(self, split:float):
        self.split = split
        self.split_display = self._split_seconds_to_display_string(self.split)
        self.watts = self.calculate_watts()

    @classmethod
    def seconds(cls, seconds:float):
        return cls(seconds)

    @classmethod
    def display(cls, display:str):
        Split.verify_split(display)
        return cls(cls.split_display_string_to_seconds(display))

    def __repr__(self):
        return 'A %dm split of %s (%d seconds) requires a power output of %0.1f watts' % (self.SPLIT_DISTANCE, self.split_display, self.split, self.watts)

    @staticmethod
    def verify_split(split):
        compiled_pattern = re.compile(Split.SPLIT_DISPLAY_REGEX)
        if not re.match(compiled_pattern, split):
            raise ValueError('The string "%s" is not a valid format for a split' % split)

    @staticmethod
    def verify_increment(increment):
        if increment < 0.1:
            raise ValueError('The increment must be at least 0.1; %s is invalid' % str(increment))

    @staticmethod
    def split_display_string_to_seconds(split):
        minutes = int(split.split(':')[0])
        seconds = float(split.split(':')[1])
        return minutes * 60 + seconds

    def calculate_watts(self):
        pace =self.split / self.SPLIT_DISTANCE

        watts = 2.8 / pace ** 3

        return round(watts, 1)

    def get_row(self):
        # split column
        fmt_template = '%s'
        fmt_values = [self.split_display.center(Split.COLUMN_WIDTH)]

        # wattage column
        fmt_template += '%s'
        fmt_values.append(str(self.watts).center(Split.COLUMN_WIDTH))

        return fmt_template % tuple(fmt_values)

    @staticmethod
    def get_header_row():
        header_cols = []

        # split column
        fmt_template = '%s'
        header_cols.append('Split'.center(Split.COLUMN_WIDTH))

        # wattage column
        fmt_template += '%s'
        header_cols.append('Watts'.center(Split.COLUMN_WIDTH))

        return fmt_template % tuple(header_cols)

    @staticmethod
    def _split_seconds_to_display_string(split):
        minutes, seconds = divmod(split, 60)
        display_string = '%d:%04.1f' % (int(minutes), float(seconds))
        return display_string
