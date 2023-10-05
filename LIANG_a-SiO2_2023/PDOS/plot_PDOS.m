%% Get file from folder
clear; close all; font_size=10;

%% Load data
repeat_run = 3;
vac_container = [];
dos_container = [];

for i=1:repeat_run 

	load(['run_',num2str(i), '\dos.out']); 
	dos_container = [dos_container; dos];

    load(['run_',num2str(i), '\mvac.out']);
    vac_container = [vac_container; mvac];
	
end

num_atoms=73728;    % from xyz.in
N=500;              % number of correlation steps (from run.in)
M=length(dos_container)/N;   % number of independent functions

%% Load expt. data
load('expt_data\Neutron_scattering.data'); 
% 1 meV = 0.242 THz = 8.066 cm-1;
Neutron_scattering(:, 1) = Neutron_scattering(:, 1) .* 0.242;

%% calculate data
t=mvac(1:N, 1);   % correlation time
nu=dos(1:N,1)/pi/2; % nu = omega/2/pi
vac_x=mean(reshape(vac_container(:, 2), N, M), 2);
vac_y=mean(reshape(vac_container(:, 3), N, M), 2);
vac_z=mean(reshape(vac_container(:, 4), N, M), 2);

%% total
total_dos = (dos_container(:, 2) + dos_container(:, 3) + dos_container(:, 4))/3;
total_dos = reshape(total_dos, N, M);

total_dos(:, 1) = total_dos(:, 1)/max(total_dos(:, 1));
total_dos(:, 2) = total_dos(:, 2)/max(total_dos(:, 2));
total_dos(:, 3) = total_dos(:, 3)/max(total_dos(:, 3));

ave_dos = mean(total_dos, 2);
error_dos = std(total_dos, [], 2);

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% Figure 1
figure('Position', [200, 200, 900, 400]);

% average over x, y, and z
plot(t, (vac_x+vac_y+vac_z)/(vac_x(1)+vac_y(1)+vac_z(1)),'-','linewidth', 3);
xlabel('Correlation time (ps)','fontsize',font_size);
ylabel('VAC (Normalized)','fontsize',font_size);
xlim([0, 1]);
set(gca,'fontsize',font_size);
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Figure 2
color_1 = [0.64, 0.08, 0.18];   
color_2 = addcolorplus(2);   

figure('Position', [200, 200, 500, 400]);

% Plot shade
plot_option = '';
shade_color = [0.86 0.86 0.86];

% Plot the error region using fill
errorshade2(nu, ave_dos, 0, error_dos, plot_option, shade_color);
hold on;

h1 = plot(nu, ave_dos, '-', 'linewidth', 2.5, 'Color', color_1);
hold on;

h2 = scatter(Neutron_scattering(:, 1), Neutron_scattering(:, 2)/max(Neutron_scattering(:, 2)), 70, 'o', 'LineWidth', 2.0, 'MarkerEdgeColor', [0.5,0.5,0.5]); 

xlim([0, 45]);
ylim([0, 1]);

xlabel('$\omega$/2$\pi$ (THz)');
ylabel('VDOS (Normalized)');

legend([h1, h2], 'This work', 'Expt.', 'location', 'best', 'NumColumns', 1);

legend boxoff;

set(gca,'fontsize', 20, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%print('VDOS.svg', '-dsvg', '-painters');

