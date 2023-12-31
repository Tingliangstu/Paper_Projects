from pylab import *

import numpy as np

nep = np.loadtxt('nep.txt', skiprows = 6)

subplot(1,2,1)

hist(np.log(np.abs(nep)), bins = 100)

subplot(1,2,2)

scatter(range(len(nep)), nep, s=0.8)
gcf().set_size_inches(9, 3)
savefig("nep.png", bbox_inches='tight')
show()