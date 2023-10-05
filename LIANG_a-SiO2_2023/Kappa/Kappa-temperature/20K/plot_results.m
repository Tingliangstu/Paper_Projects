%% Start
clear; close all; 

%% Get T
path = pwd;
[~, foldername, ~] = fileparts(path);
digits = regexp(foldername, '\d+', 'match');
T = str2double(digits{1});                     %% K

%% Deal data
repeat_run = 5;
kappa_container = [];

for i=1:repeat_run 

	load(['run_',num2str(i), '\kappa.out']); 
	kappa_container = [kappa_container; kappa];
	
end
kappa = kappa_container;

%%  MD parameters
time_step = 1;                    % 1 fs
Total_step = 4e6;                 % Total step used in HNEMD run
ave_step = 1000*time_step;        % The conductivity data will be averaged for each 1000 steps before written out
N=Total_step*time_step/ave_step;  % number of data for each run

Ns=size(kappa, 1)/N;              % number of independent runs

%% Time parameters
dt = ave_step;                           % fs
dt_in_ps = dt/1000;                      % ps
time_in_ps = (dt_in_ps:dt_in_ps:N);      % time

%% Running average of the thermal conductivity
k_x_in = cumsum(reshape(kappa(:, 1), N, Ns)) ./ ((1:N).'*ones(1, Ns));
k_x_out = cumsum(reshape(kappa(:, 2), N, Ns)) ./ ((1:N).'*ones(1, Ns));

k_y_in = cumsum(reshape(kappa(:, 3), N, Ns)) ./ ((1:N).'*ones(1, Ns));
k_y_out = cumsum(reshape(kappa(:, 4), N, Ns)) ./ ((1:N).'*ones(1, Ns));

k_z_tot = cumsum(reshape(kappa(:, 5), N, Ns)) ./ ((1:N).'*ones(1, Ns));

% For 1-D transport direction (z-direction)

error = std(k_z_tot(end, :))/sqrt(Ns);              % only for plotting
disp(['k_tot_less_data = (', num2str(mean(k_z_tot(end, :))), ' +- ', num2str(error), ') W/mK']);

%% For new error report method
block_sizes = 200;
num_blocks = length(kappa(:, 5)) / block_sizes;
kappa_blocks = reshape(kappa(:, 5), block_sizes, num_blocks);

kappa_ave_all_data = mean(kappa(:, 5));

error_for_report = std(mean(kappa_blocks))/sqrt(num_blocks);  % only for plotting

disp(['kappa_ave_all_data = (', num2str(kappa_ave_all_data), ' +- ', num2str(error_for_report), ') W/mK']);

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% Plot 
figure;
axes('ColorOrder', tab10(21), 'NextPlot', 'replacechildren')        

%% multi-line
sub = plot(time_in_ps/1000, k_z_tot, '-', 'linewidth', 0.5);

%% transparent
for i=1:length(sub)
		sub(i, 1).Color(4) = 0.2;
end
hold on;

%% ave
color_1 = addcolorplus(134);    
color_2 = addcolorplus(2); % color 136
plot(time_in_ps/1000, mean(k_z_tot, 2), 'linewidth', 2.0, 'LineStyle', '-', 'Color', color_1);
hold on;

%% error 
plot(time_in_ps/1000, mean(k_z_tot, 2)+error,  'linewidth', 1.0, 'LineStyle', '--', 'Color', 'k');
hold on;
plot(time_in_ps/1000, mean(k_z_tot, 2)-error,  'linewidth', 1.0, 'LineStyle', '--', 'Color', 'k');

%% setting
xlim([0, max(time_in_ps/1000)]);
ylim([0 3]);
box on;
% word
xlabel('Time (ns)', 'interpreter', 'Latex');
ylabel('$\kappa$ (W m${^{-1}}$K${^{-1}}$)', 'interpreter', 'Latex');
title(['Temperature = ', num2str(T),' K']);
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Save
%saveas(gcf, 'figure.svg')


