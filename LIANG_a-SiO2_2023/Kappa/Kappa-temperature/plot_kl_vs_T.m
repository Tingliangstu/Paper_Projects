%% Start
clear; close all;

%% Load expt. data
load exp_data\Lee_Cahill_1997_kl.data;

%% Load simulation data from file

file_T = [40, 60, 80, 100, 150, 200, 250, 300, 350, 500, 750, 1000, 1250, 1500, 1750, 2000];

data_k_L_quan = [];
data_error_k_L_quan = [];

data_k_L_compare = [];
data_error_k_compare = [];
data_k_L_quan_compare = [];
data_error_k_L_quan_compare = [];

for i=1:length(file_T)

    load([num2str(file_T(i)), 'K', '\Kq_vs_L_T.mat']); 
    data_k_L_quan = [data_k_L_quan, ave_k_L_quan];
    data_error_k_L_quan = [data_error_k_L_quan, error_k_L_quan];

    load([num2str(file_T(i)), 'K', '\K_for_compare_vs_L_T.mat']); 
	data_k_L_compare = [data_k_L_compare, ave_k_L_for_compare];
    data_error_k_compare = [data_error_k_compare, error_k_L_for_compare];

	load([num2str(file_T(i)), 'K', '\Kq_for_compare_vs_L_T.mat']); 
	data_k_L_quan_compare = [data_k_L_quan_compare, ave_k_L_quan_for_compare];
    data_error_k_L_quan_compare = [data_error_k_L_quan_compare, error_k_L_quan_for_compare];
	
end

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% For Kq(L) vs Tem
Tem_plot = [2, 4, 6, 8, 14];
% for K(L)
len = 10.^(0.01:0.1:6);                                    % consider length from 10 nm to 1 mm
len_1 = 0.0001:0.1:1;
len = [len_1, len];
h=[];

figure('Position', [200, 100, 500, 400]);
colors = {[0,0.45,0.74], [0.85,0.33,0.1], [0.93,0.69,0.13], [0.49,0.18,0.56], [0.47,0.67,0.19]};

for i = 1:length(Tem_plot)

    h(i) = semilogx(len/1000, data_k_L_quan(:, Tem_plot(i)), '-', 'linewidth', 2.5, 'Color', colors{i});
    hold on;
    semilogx(len/1000, data_k_L_quan(:, Tem_plot(i))+data_error_k_L_quan(:, Tem_plot(i)), '--', 'linewidth', 1.5, 'Color', colors{i});
    hold on;
    semilogx(len/1000, data_k_L_quan(:, Tem_plot(i))-data_error_k_L_quan(:, Tem_plot(i)), '--', 'linewidth', 1.5, 'Color', colors{i});
    hold on;
 
end

xlabel('$L$ ($\mu$m)');
ylabel('$\kappa^q$($L$) (W/m/K)');
legend(h, '60 K', '100 K', '200 K', '300 K', '1250 K', 'location', 'best', 'NumColumns', 1, 'Box', 'off');

ylim([0, 2]);
xlim([1.0e-4, 10]);
xticklabels({'10$^{-4}$', '10$^{-3}$', '10$^{-2}$', '10$^{-1}$', '10$^{0}$', '10$^{1}$'});

set(gca,'fontsize', 19, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('Kq_vs_T.svg', '-dsvg', '-painters');

%% plot k_L_quan_compare vs Expt.
figure('Position', [200, 100, 900, 700]);
% Color
color_1 = [1, 0.5, 0.78];  
color_2 = [0.49, 0.18, 0.56]; 
color_3 = [0.64, 0.08, 0.18]; 
color_4 = [0.87, 0.49, 0.0]; 
color_5 = [0.93, 0.69, 0.15]; 
color_7 = [0.47, 0.67, 0.19];
color_8 = [0.31, 0.31, 0.31];

% Plot last 18 data, for the expt. data for 190 nm length
h1 = loglog(Lee_Cahill_1997_kl(72-17:end, 1), Lee_Cahill_1997_kl(72-17:end, 2), 'x', 'MarkerSize', 13.0, 'linewidth', 2.0, 'Color', color_1); 
hold on;

h2 = errorbar(file_T, data_k_L_compare(4, :), data_error_k_compare(4, :), 's', 'MarkerSize', 13.0, ...
        'linewidth', 2.0, 'CapSize', 18.0, 'Color', color_3);
hold on;

h3 = errorbar(file_T, data_k_L_quan_compare(4, :), data_error_k_L_quan_compare(4, :), 'o', 'MarkerSize', 13.0,...
        'linewidth', 2.0, 'CapSize', 18.0, 'Color', color_7);
hold off;

%% label

xlabel('$T$ (K)', 'interpreter', 'latex');
ylabel('$\kappa$ (W m${^{-1}}$K${^{-1}}$)', 'interpreter', 'Latex');

xlim([30, 2000]);
ylim([0.1, 2]);

h_legend = legend([h2, h3, h1], 'This work (Classical $\kappa$, $L$=190 nm)', ...
                                'This work (Quantum $\kappa^q$, $L$=190 nm)', 'Lee $et$ $al.$ (Expt., $L$=190 nm)', ...
                                'location', 'best', 'NumColumns', 1, 'Box', 'off');

set(gca,'fontsize', 25, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('Kl_vs_T.svg', '-dsvg', '-painters');
%% For small range (plot k_L_quan_compare vs Expt.)
figure('Position', [200, 100, 900, 700]);

% Plot last 18 data, for the expt. data for 190 nm length
h1 = loglog(Lee_Cahill_1997_kl(72-17:end, 1), Lee_Cahill_1997_kl(72-17:end, 2), 'x', 'MarkerSize', 13.0, 'linewidth', 2.0, 'Color', color_1); 
hold on;

h2 = errorbar(file_T, data_k_L_compare(4, :), data_error_k_compare(4, :), 's', 'MarkerSize', 13.0, ...
        'linewidth', 2.0, 'CapSize', 18.0, 'Color', color_3);
hold on;

h3 = errorbar(file_T, data_k_L_quan_compare(4, :), data_error_k_L_quan_compare(4, :), 'o', 'MarkerSize', 13.0,...
        'linewidth', 2.0, 'CapSize', 18.0, 'Color', color_7);
hold off;

%% label

xlabel('$T$ (K)', 'interpreter', 'latex');
ylabel('$\kappa$ (W m${^{-1}}$K${^{-1}}$)', 'interpreter', 'Latex');

xlim([50, 500]);
ylim([0.2, 2]);

h_legend = legend([h2, h3, h1], 'This work (Classical $\kappa$, $L$=190 nm)', ...
                                'This work (Quantum $\kappa^q$, $L$=190 nm)', 'Lee $et$ $al.$ (Expt., $L$=190 nm)', ...
                                'location', 'best', 'NumColumns', 1, 'Box', 'off');

set(gca,'fontsize', 25, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);


