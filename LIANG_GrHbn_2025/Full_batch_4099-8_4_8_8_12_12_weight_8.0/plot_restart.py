from pylab import *

import numpy as np


restart = np.loadtxt('nep.restart')

subplot(1,2,1)

hist(restart[:, 0], bins = 100)
ylabel('First column')

subplot(1,2,2)

hist(restart[:, 1], bins = 100)

ylabel('Second column')

gcf().set_size_inches(9, 3)
subplots_adjust(wspace=0.35, hspace=0.3)
savefig("restart.png", bbox_inches='tight')
#show()
