import numpy as np

# Example data
data = [1, 2, 0, -3, 5]

# Check for non-positive values
data = [x for x in data if x > 0]

# Now you can safely compute log
log_data = np.log(data)

import matplotlib.pyplot as plt
import numpy as np

# Example data
data = [0.1, 1, 10, 100]

plt.plot(data)
plt.yscale('log')  # Set y-axis to log scale
plt.show()
