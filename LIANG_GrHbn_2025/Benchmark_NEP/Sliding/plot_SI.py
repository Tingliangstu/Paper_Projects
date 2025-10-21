from pylab import *
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable

grgr_dft = np.load("gr_gr_dft.npy")
grgr_nep = np.load("gr_gr_nep.npy")

bnbn_dft = np.load("hBN_hBN_dft.npy")
bnbn_nep = np.load("hBN_hBN_nep.npy")

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.65, "xtick.major.width": 0.65, "ytick.major.width": 0.65, 
	              "axes.labelsize": 15, "xtick.labelsize": 13.0, "ytick.labelsize": 13.0})
	              	
#*************************** Set Seaborn style ************************* 

ddx = 1
ddy = np.sqrt(3)
xstep = 21
ystep = 21
extent = 0, ddx*xstep, 0, ddy*ystep
x = np.linspace(0, ddx*(xstep-1), xstep)
y = np.linspace(0, ddy*(ystep-1), ystep)
X, Y = np.meshgrid(x, y)

############################# Gr/Gr ############################

# DFT
figure(figsize=(10, 8))
subplot(2, 3, 1)

grgr_dft_map = grgr_dft.reshape((21, 21), order="F")

#print(np.max(grgr_dft_map)) 

im1 = imshow(grgr_dft_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',              
             origin='lower',
             vmin=0,
             vmax=4.0)
              
C = contour(grgr_dft_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)
             
## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

#xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

title("PBE+MBD", fontsize=16)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 4.0, 5))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

#NEP
subplot(2, 3, 2)
grgr_nep_map = grgr_nep.reshape((21, 21), order="F")
              
#print(np.max(grgr_nep_map)) 

im1 = imshow(grgr_nep_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=4.0)

C = contour(grgr_nep_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

#xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
#ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

title("NEP", fontsize=16)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 4.0, 5))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length


###
subplot(2, 3, 3)

#print(np.max(grgr_nep_map - grgr_dft_map)) 

im1 = imshow(grgr_nep_map - grgr_dft_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=0.3)

levels = np.linspace(0, 0.3, 3) 
C = contour(grgr_nep_map - grgr_dft_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4, levels=levels)        

#xlabel(r'$x$ Shift ($\mathrm{\AA}$)')

title("Differences", fontsize=16) 

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 0.3, 4))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

cbar1.set_label('Energy (meV/atom)', fontsize=14)

####################################### hbn-Hbn ##################################

subplot(2, 3, 4)

bnbn_dft_map = bnbn_dft.reshape((21, 21), order="F")

#print(np.max(bnbn_dft_map)) 

im1 = imshow(bnbn_dft_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',              
             origin='lower',
             vmin=0,
             vmax=5.0)
              
C = contour(bnbn_dft_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)
             
## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

#title("PBE+MBD", fontsize=16)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 5.0, 6))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

#NEP
subplot(2, 3, 5)
bnbn_nep_map = bnbn_nep.reshape((21, 21), order="F")
              
print(np.max(bnbn_nep_map)) 

im1 = imshow(bnbn_nep_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=4.4)

C = contour(bnbn_nep_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
#ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

#title("NEP", fontsize=16)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 4.0, 5))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length


###
subplot(2, 3, 6)

#print(np.max(bnbn_dft_map- bnbn_nep_map)) 

im1 = imshow(bnbn_dft_map- bnbn_nep_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=0.6)

C = contour(bnbn_nep_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)             

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')

#title("Differences", fontsize=16) 

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 0.6, 4))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

cbar1.set_label('Energy (meV/atom)', fontsize=14)

subplots_adjust(left=0.1, right=0.98, bottom=0.1, top=0.95, wspace=0.35, hspace=0.25)


savefig("Gr_Gr_Hbn_Hbn.svg", bbox_inches='tight')

show()

print("***** ALL Done !!! *****")
