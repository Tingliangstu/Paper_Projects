%% Start 
clear; close all; font_size = 15;

%% Load expt. data
load Exp_Ref_data\Sq_prl_2007.data;
load Exp_Ref_data\Sq_prb_2008.data;
load Exp_Ref_data\Sq_Gap.data;

%% Load nep data
load (['rate_1', 'e', '11', '\Sq_and_gr\Sq_X_rays_smoothed']);
Sq_rate_1x11 = Sq_X_rays_smoothed;

%% Plot figures
color_1 = addcolorplus(6);    
color_2 = addcolorplus(2);   

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter','latex');  
set(groot, 'defaultAxesTickLabelInterpreter','latex');  
set(groot, 'defaultLegendInterpreter','latex');

%% sort exp data
[Sq_xray_2007_prl_x, I] = sort(Sq_prl_2007(:, 1));
Sq_xray_2007_prl_y = Sq_prl_2007(I, 2);

[Sq_xray_2008_prb_x, I] = sort(Sq_prb_2008(:, 1));
Sq_xray_2008_prb_y = Sq_prb_2008(I, 2);

[Sq_Gap_x, I] = sort(Sq_Gap(:, 1));
Sq_Gap_y = Sq_Gap(I, 2);

%% Plot
figure('Position', [100, 100, 500, 500]);

plot(Sq_xray_2008_prb_x, Sq_xray_2008_prb_y, 'o', 'MarkerSize', 6.0,  'MarkerEdgeColor', color_1, 'MarkerFaceColor', color_1); 
hold on;
plot(Sq_xray_2007_prl_x, Sq_xray_2007_prl_y, 'x', 'MarkerSize', 6.5,  'MarkerEdgeColor', color_2, 'MarkerFaceColor', color_2); 
hold on;

color_1 = [0.64, 0.08, 0.18];
plot(Sq_rate_1x11(:, 1), Sq_rate_1x11(:, 2),'-', 'linewidth', 2, 'Color', color_1);       

xlabel('$q$({\AA}${^{-1}}$)', 'interpreter', 'Latex');
ylabel('$S$($q$)');

xlim([0, 16]);
ylim([0, 2.5]);

legend('Expt. (2)', 'Expt. (3)', 'NEP (1$\times$10$^{11}$ K/s)', 'location', 'best', 'NumColumns', 1);

legend boxoff;
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('Maintext_quenchRate_Sq.svg', '-dsvg', '-painters');


