%% Start 
clear; close all; font_size = 13;

load bilayer_Gr_AB_stacking_exfoliation_curve.data;

data = bilayer_Gr_AB_stacking_exfoliation_curve;

relative_energies = data(:, 3) - data(47, 3);

plot(data(:, 2), relative_energies*1000, 'linewidth', 2);       % from ev to meV
xlabel('Distance (A)','fontsize',font_size);
ylabel('Energy (meV/atom)','fontsize',font_size);
xlim([2.5,12]);
ylim([-30,90]);
set(gca,'fontsize',font_size,'linewidth',1,'ticklength',get(gca,'ticklength')*2);
legend('DFT');   %
title('Gr-AB-stacking-exfoliation-curve DFT');
