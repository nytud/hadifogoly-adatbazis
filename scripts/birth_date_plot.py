
# adat:
# cat data/Kart.csv | cols 5 | grep "^....$" | sstat | sed "s/^ *//" | sort -t ' ' -k2,2 -n | awk '{print $2, $1}' > birth_year.csv

# importing the required module
import matplotlib.pyplot as plt

# x axis values
x = list(range(1700, 2050))
# corresponding y axis values
y = [0] * 350

with open('data/birth_year.csv') as inp_fh:
    for line in inp_fh:
        xval, yval = line.strip().split()
        y[int(xval)-1700] = int(yval)
        #if len(x) > 25:
        #    break

# plotting the points
plt.plot(x, y)
#plt.scatter(x, y)

# naming the x axis
plt.xlabel('születési év')
# naming the y axis
plt.ylabel('előfordulási szám (log)')

# giving a title to my graph
#plt.title('My first graph!')

plt.yscale('log')

# function to show the plot
plt.show()

