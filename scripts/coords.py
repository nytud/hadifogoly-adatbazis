"""
Add coordinates to cities (field #9 and #16)
according to the geonames database.
Result: 4 additional fields, i.e.
long of #9, lat of #9, long of #16, lat of #16.
"""

import argparse
import glob
import sys

from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import log2, log10
import numpy as np

from transcribe import AS_FALLBACK, FROM_STRICT # !

# field indices
# fields containing citynames to process
BIRTH_CITY = 8
CAPTURE_CITY = 15
# capture date
CAPTURE_DATE = 20

GEONAMES_DATA_DIR = 'data/geonames'


def load_geonames_data():
    """
    Load geonames data.
    Returns a dict {city: (latitude, longitude)}.
    """
    filepath = f'{GEONAMES_DATA_DIR}/??.txt'
    filenames = glob.glob(filepath)

    geonames = defaultdict(lambda: ('', ''))

    for filename in filenames:
        f = open(filename, 'r')

        for line in f:
            fields = line.split('\t')
            mainname, altnames, lati, lngi, feature, popul = \
                [fields[i] for i in [1, 3, 4, 5, 6, 14]]

            # only inhabited ('P') with population > 0
            if not(feature == 'P' and int(popul) >= 1):
                continue

            for name in [mainname] + altnames.split(','):
                # XXX no check for conflict
                #     = same city name with different coords
                # XXX no check whether
                #     there are several cities with the same name
                if len(name) > 0:
                    geonames[name] = (lati, lngi)

                #print('\t'.join([name, lati, lngi]))
 
    return geonames


def front_plot(front_db):
    """
    Plot "front line" as an animated scatter plot
    based on location of war prisoners being captured.
    """

    MIN_CAPTURED = 1 # per day per location
    MIN_LOCATION = 1 # per day

    def data_stream():
        """Generating data day by day."""
        ordered_days = sorted(front_db.items())
    
        for day, one_day_data in ordered_days:
            print(day, one_day_data)
            x, y, s = [], [], []
    
            for (lati, lngi), val in one_day_data.items():
                print(lati, lngi, val)
                if val >= MIN_CAPTURED:
                    x.append(float(lngi))
                    y.append(float(lati))
                    s.append(log10(val + 1)*100) # log(1) would be 0...

            if len(x) >= MIN_LOCATION:
                yield np.array(x), np.array(y), np.array(s), day
    
    def update(i):
        """Update the scatter plot."""
        x, y, s, title = next(stream)
    
        scat.set_offsets(np.array([x,y]).T) # x and y
        scat.set_sizes(s) # sizes
    
        fig.suptitle(title)
    
        return [scat]
    
    
    stream = data_stream()
    x, y, s, title = next(stream)
    
    fig, ax = plt.subplots()
    scat = ax.scatter(x, y, s=s, color='black', alpha=0.5)
    fig.suptitle(title)
    ax.axis([5, 35, 44, 50]) # longitude / from, to; latitude / from, to
    
    # XXX set frames properly
    #     now it is too large -> causes StopIteration in update()
    ani = animation.FuncAnimation(fig, update,
        frames=2000, interval=200)
    ani.save('front.mp4')


def splitandwhich(string, sep, n):
    """
    Split by sep and return nth piece.
    If sep not present return the whole string.
    """
    if sep in string:
        string = string.split(sep)[n]
    return string


def main():
    """Do the thing."""
    args = get_args()

    coord_dict = load_geonames_data()

    front_db = defaultdict(lambda: defaultdict(int))

    for line in sys.stdin:
        orig_line = line.strip()
        fields = orig_line.split('\t')
        for field_id in [BIRTH_CITY, CAPTURE_CITY]:
            field = fields[field_id]

            # extract the city name
            if field[-2:] == AS_FALLBACK: field = ''
            field = field[0:-2] # 2-char "mark" removed from the end
            field = splitandwhich(field, FROM_STRICT, 1) # handle '/D'
            items = [splitandwhich(item, '[', 0)
                     for item in field.split(';')]
            city = items[0] # always take the 1st one
            lati, lngi = coord_dict[city]
            fields.extend([lati, lngi])

        # print the whole database coords added
        print('\t'.join(fields))

        # collect data for war front line:
        # capture date + coord of city of capture
        if len(lati) > 0 and len(lngi) > 0:
            try:
                # check date input format: dd.mm.yyyy
                date_obj = datetime.datetime.strptime(
                    fields[CAPTURE_DATE], '%d.%m.%Y')
                front_db[date_obj.date()][(lati, lngi)] += 1
            except ValueError:
                pass

    # visualise war front line
    front_plot(front_db)


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
