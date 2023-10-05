%% Start 
clear; close all; font_size = 13;

%% Load expt. data
load Exp_Ref_data\gr_neutron_2007_tersoff.data;
load Exp_Ref_data\gr_neutron_2010.data;

%% Load nep data
load (['rate_1', 'e', '11', '\Sq_and_gr\gr_neutrons_smoothed']);
gr_rate_1x11 = gr_neutrons_smoothed;

%% Plot figures
color_1 = addcolorplus(6);    
color_2 = addcolorplus(2);    

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter','latex');  
set(groot, 'defaultAxesTickLabelInterpreter','latex');  
set(groot, 'defaultLegendInterpreter','latex');

%% sort exp data
[gr_neutron_2007_tersoff_x, I] = sort(gr_neutron_2007_tersoff(:, 1));  %% Got from 1983 (Non-Cryst. Solids 58 (1983) 109)
gr_neutron_2007_tersoff_y = gr_neutron_2007_tersoff(I, 2);

[gr_neutron_2010_x, I] = sort(gr_neutron_2010(:, 1));  %% Got from 2008 (PRL)
gr_neutron_2010_y = gr_neutron_2010(I, 2);

%% Plot
figure('Position', [100, 100, 500, 500]);
plot(gr_neutron_2007_tersoff_x, gr_neutron_2007_tersoff_y, 'o', 'MarkerSize', 6.0, 'MarkerEdgeColor', color_1, 'MarkerFaceColor', color_1); 
hold on;
plot(gr_neutron_2010_x, gr_neutron_2010_y, 'x', 'MarkerSize', 6.5,  'MarkerEdgeColor', color_2, 'MarkerFaceColor', color_2); 
hold on;

color_1 = [0.64, 0.08, 0.18];
plot(gr_rate_1x11(:, 1), gr_rate_1x11(:, 2), '-', 'linewidth', 2.0, 'Color', color_1);       
hold on;
      
plot([1.61, 1.61], [0, 4.5], '-.', 'linewidth', 1.0, 'color', [0.5 0.5 0.5]);  % Si-O
hold on;
plot([2.626, 2.626], [0, 2.80], '-.', 'linewidth', 1.0, 'color', [0.5 0.5 0.5]);  % O-O

xlabel('$r$({\AA})', 'interpreter', 'Latex');
ylabel('$g$($r$)','fontsize',font_size);

xlim([0,8]);
ylim([0,5]);

legend('Expt. (1)', 'Expt. (2)', 'NEP (1$\times$10$^{11}$ K/s)', 'location', 'best', 'NumColumns', 1);

legend boxoff;
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('Maintext_quenchRate_gr.svg', '-dsvg', '-painters');

