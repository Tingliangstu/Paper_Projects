from pylab import *

##set figure properties
aw = 1.5
fs = 16
lw = 2.0
font = {'size'   : fs}
matplotlib.rc('font', **font)
matplotlib.rc('axes' , lw=aw)

def set_fig_properties(ax_list):
    tl = 6
    tw = 1.5
    tlm = 3
    
    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='out', right=False, top=False)


loss = loadtxt('loss.out')
loss[:,0] = np.arange(1, len(loss) + 1)*100
print("We have run %s steps!"%loss[-1, 0])
energy_train = loadtxt('energy_train.out')
force_train = loadtxt('force_train.out')
virial_train = loadtxt('virial_train.out')
#energy_test = loadtxt('energy_test.out')
#force_test = loadtxt('force_test.out')
#virial_test = loadtxt('virial_test.out')

figure(figsize=(14, 10))
subplot(2, 2, 1)
set_fig_properties([gca()])
loglog(loss[:, 0], loss[:, 1],  ls="-", lw=lw, c = "C1", label="Total")
loglog(loss[:, 0], loss[:, 2],  ls="-", lw=lw, c = "C4", label=r"$L_{1}$")
loglog(loss[:, 0], loss[:, 3],  ls="-", lw=lw, c = "C5", label=r"$L_{2}$")
loglog(loss[:, 0], loss[:, 4],  ls="-", lw=lw, c = "C0", label="Energy_train")
loglog(loss[:, 0], loss[:, 5],  ls="-", lw=lw, c = "C2", label="Force_train")
loglog(loss[:, 0], loss[:, 6],  ls="-", lw=lw, c = "C3", label="Virial_train")
xlim([1e2, 7e5])
ylim([0.65e-3, 5e0])
xlabel('Generation')
ylabel('Loss')
legend(loc="lower left",  
        ncol = 2, 
        fontsize = 14, 
        frameon = False,
        columnspacing = 0.2)


subplot(2, 2, 2)
set_fig_properties([gca()])
plot(energy_train[:, 1], energy_train[:, 0], 'o', c="C0", ms = 5, label="Train dataset")
#plot(energy_test[:, 1], energy_test[:, 0], 'o', c="C6", ms = 5, label="Test dataset")
plot([-12, 0], [-12, 0], c = "grey", lw = 1)
text(-8.7, -9.2, 'RMSE = {0:4.2f} mev/atom'.format(loss[-1, 4]*1000), fontsize=13)
xlim([-9.5, -7.5])
ylim([-9.5, -7.5])
xlabel('DFT energy (eV/atom)')
ylabel('NEP energy (eV/atom)')
legend(loc="upper left")


subplot(2, 2, 3)
set_fig_properties([gca()])
plot(force_train[:, 3], force_train[:, 0], 'o', c="C2", ms = 5, label="Train dataset")
plot(force_train[:, 4:6], force_train[:, 1:3], 'o', c="C2", ms = 5)
#plot(force_test[:, 3], force_test[:, 0], 'o', c="C7", ms = 5, label="Test dataset")
#plot(force_test[:, 4:6], force_test[:, 1:3], 'o', c="C7", ms = 5)
text(-4, -20, 'RMSE = {0:4.2f} mev/A'.format(loss[-1, 5]*1000), fontsize=13)
plot([-40, 40], [-40, 40], c = "grey", lw = 1)
xlim([-40, 40])
ylim([-40, 40])
xlabel(r'DFT force (eV/$\rm{\AA}$)')
ylabel(r'NEP force (eV/$\rm{\AA}$)')
legend(loc="upper left")


subplot(2, 2, 4)
set_fig_properties([gca()])
plot(virial_train[:, 6], virial_train[:, 0], 'o', c="C3", ms = 5, label="Train dataset")
plot(virial_train[:, 7:12], virial_train[:, 1:6], 'o', c="C3", ms = 5)
#plot(virial_test[:, 1], virial_test[:, 0],  'o', c="C8", ms = 5, label="Test dataset")
plot([-10, 10], [-10, 10], c = "grey", lw = 1)
text(2, 0, 'RMSE = {0:4.2f} mev/atom'.format(loss[-1, 6]*1000), fontsize=13)
xlim([-2, 7])
ylim([-2, 7])
xlabel('DFT virial (eV/atom)')
ylabel('NEP virial (eV/atom)')
legend(loc="upper left")

subplots_adjust(wspace=0.35, hspace=0.3)
savefig("RMSE.png", bbox_inches='tight')
