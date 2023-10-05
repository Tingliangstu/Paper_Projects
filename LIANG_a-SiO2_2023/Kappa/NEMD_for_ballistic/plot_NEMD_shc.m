%% Get file from folder
clear; close all; font_size = 12;

%% Deal data
repeat_run = 5;
SHC_container = [];

for i=1:repeat_run 

	load(['run_',num2str(i), '\nu_Gc.mat']); 
	SHC_container = [SHC_container, Gc];
	
end
NEMD_SHC = SHC_container;

%% Average the SHC
ave_NEMD_SHC = mean(NEMD_SHC, 2);
error_NEMD_SHC = std(NEMD_SHC, [], 2);

save('ave_NEMD_SHC.mat',  'ave_NEMD_SHC', 'error_NEMD_SHC');

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% Plot figures
color_1 = [0.64, 0.08, 0.18];
color_2 = [0.47, 0.67, 0.19];

figure('Position', [100, 100, 500, 400]);

%% Plot shade
plot_option = '';
shade_color = [0.86 0.86 0.86];

% Plot the error region using fill
errorshade2(nu, ave_NEMD_SHC, 0, error_NEMD_SHC, plot_option, shade_color);
hold on;

%% Plot line
h1 = plot(nu, ave_NEMD_SHC, '-', 'linewidth', 2.5, 'Color', color_1);

hold off;

xlabel('$\omega$/2$\pi$ (THz)');
ylabel('$G$($\omega$) (GW/m$^2$/K/THz)');

ylim([0, 0.04]);
xlim([0, 40]);
box on;

%legend(h1, 'NEMD SHC', 'location', 'northeast', 'NumColumns', 1, 'Box', 'off');

set(gca,'fontsize', 20, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('NEMD_SHC.svg', '-dsvg', '-painters');
