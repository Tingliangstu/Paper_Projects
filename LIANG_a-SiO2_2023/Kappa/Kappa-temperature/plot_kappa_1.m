%% Start
clear; close all;

%% Load data from Excel file
filename = 'kappa_T_data.xlsx';
Tem = xlsread(filename, 'Sheet1', 'A2:A20');
kappa_nomal = xlsread(filename, 'Sheet1', 'B2:B20');
error_nomal = xlsread(filename, 'Sheet1', 'C2:C20');

kappa_quantum = xlsread(filename, 'Sheet1', 'D2:D20');
error_quantum = xlsread(filename, 'Sheet1', 'E2:E20');

%% Load expt. data
load exp_data\Cahill_Pohl_1988.data;
load exp_data\Cahill_1990.data;
load exp_data\Wray_Thomas_for_high_T.data;

%% load WTE
load exp_data\Michele_2022_rWTE_GAP.data;
load exp_data\Yang_2022_WTE_anharmonic.data;


%% Plot figure
color_1 = [1, 0.5, 0.78];  
color_2 = [0.49, 0.18, 0.56]; 
color_3 = [0.64, 0.08, 0.18]; 
color_4 = [0.87, 0.49, 0.0]; 
color_5 = [0.93, 0.69, 0.15]; 
color_7 = [0.47, 0.67, 0.19];
color_8 = [0.31, 0.31, 0.31];

%% Enable settings about latex interpreter
set(groot,'defaulttextinterpreter','latex');
set(groot, 'defaultAxesTickLabelInterpreter','latex');
set(groot, 'defaultLegendInterpreter','latex');

%% Plot expt. data
figure('Position', [200, 100, 900, 600]);

h1 = loglog(Cahill_1990(:, 1), Cahill_1990(:, 2), 'x', 'MarkerSize', 13.0, 'linewidth', 2.0, 'Color', color_1);
hold on;
h2 = loglog(Cahill_Pohl_1988(:, 1), Cahill_Pohl_1988(:, 2)*100, 'x', 'MarkerSize', 13.0, 'linewidth', 2.0, 'Color', color_1);
hold on;
h3 = loglog(Wray_Thomas_for_high_T(:, 1), Wray_Thomas_for_high_T(:, 2), 'd', 'MarkerSize', 13.0, 'linewidth', 2.0, 'Color', color_5);
hold on;

%% plot other WTE

%% plot MD data
h6 = errorbar(Tem, kappa_nomal, error_nomal, 's', 'MarkerSize', 13.0,...
        'linewidth', 2.0, 'CapSize', 18.0, 'Color', color_3);
hold on;


%% label

xlabel('$T$ (K)', 'interpreter', 'latex');
ylabel('$\kappa$ (W m${^{-1}}$K${^{-1}}$)', 'interpreter', 'Latex');

xlim([15, 2000]);
ylim([0.03, 3]);
%title('Amorphous SiO$_2$');

%yticks(1:5:2);
h_legend = legend([h6, h1, h3], 'This work (Classical $\kappa$)', ...
    'Cahill $et$ $al.$ (Expt.)', 'Wray $et$ $al.$ (Expt.)', 'location', 'best', 'NumColumns', 1, 'Box', 'off');

set(gca,'fontsize', 25, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Save figure
% print('Compare_Kappa_quantum_T.svg', '-dsvg', '-painters');

