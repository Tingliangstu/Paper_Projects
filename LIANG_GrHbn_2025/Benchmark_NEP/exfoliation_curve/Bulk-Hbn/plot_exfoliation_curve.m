%% Start 
clear; close all; font_size = 13;

load result_ener_dist_exfoliation_curve.data;

data = result_ener_dist_exfoliation_curve;

relative_energies = data(:, 3) - data(50, 3);

plot(data(:, 2), relative_energies*1000, 'linewidth', 2);      % from ev to meV
xlabel('c lattice parameters (A)','fontsize',font_size);
ylabel('Binding energy (meV/atom)','fontsize',font_size);
xlim([4,16]);
ylim([-60,120]);
set(gca,'fontsize',font_size,'linewidth',1,'ticklength',get(gca,'ticklength')*2);
legend('DFT')   %
title('Graphite DFT');