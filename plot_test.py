import glob
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt

filenames = sorted(glob.glob('test*.gdat'))
filenames = filenames[0:3]


for filename in filenames:
    print(filename)
    data = np.loadtxt(fname=filename)
    # Delete 1st column from the 2D NumPy Array
    # passing index as 1 and setting axis=0
    data_new = np.delete(data,0,1)
    
    plt.xlabel("Iterations")
    plt.ylabel("Molecule count")
    plt.title("A+B->C")
    
    plt.plot(data_new)

plt.savefig("high_res.png",dpi=500)
plt.show()
