"""
Represents a Concept2 Ergometer 'split' - the time in minutes and seconds
needed to row 500m. The power in watts needed to achieve the split is calculated.
An instance can be constructed from either a display string in the form 'MM:SS.n'
or a value in seconds (rounded to one decimal place).
Ref. https://www.concept2.co.uk/training/watts-calculator.
The class optionally accepts a list of total distances and calculates the total
times when rowing at the split rate.
"""

import re

class Split(object):
    COLUMN_WIDTH = 13     # display tabulation
    SPLIT_DISTANCE = 500  # meters i.e. the split is time per 500m
    SPLIT_DISPLAY_REGEX = '^(\\d)+:(\\d){1,2}(\\.)?(\\d)?$' # e.g. '1:45.1'

    def __init__(self, split:float, distances):
        self.split = split
        self.split_display = self._seconds_to_display_string(self.split)
        self.watts = self.calculate_watts()

        #Split.verify_distances(distances)
        if distances:
            self.distances = list(map(int, distances))
        else:
            self.distances = []

    @classmethod
    def seconds(cls, seconds:float, distances = None):
        return cls(seconds, distances)

    @classmethod
    def display(cls, display:str, distances = None):
        Split.verify_split(display)
        return cls(cls.split_display_string_to_seconds(display), distances)

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

        # distance column(s)
        for d in self.distances:
            time_seconds = self.split * (d / Split.SPLIT_DISTANCE)
            time_string = self._seconds_to_display_string(time_seconds)
            fmt_values.append(time_string.center(Split.COLUMN_WIDTH))
            fmt_template += '%s'

        return fmt_template % tuple(fmt_values)

    @staticmethod
    def get_header_row(distances = None):
        header_cols = []

        # split column
        fmt_template = '%s'
        header_cols.append('Split'.center(Split.COLUMN_WIDTH))

        # wattage column
        fmt_template += '%s'
        header_cols.append('Watts'.center(Split.COLUMN_WIDTH))

        # distance column(s)
        for d in distances:
            fmt_template += '%s'
            col = '%sm' % d
            header_cols.append(col.center(Split.COLUMN_WIDTH))

        return fmt_template % tuple(header_cols)

    @staticmethod
    def _seconds_to_display_string(split):
        minutes, seconds = divmod(split, 60)
        display_string = '%d:%04.1f' % (int(minutes), float(seconds))
        return display_string
