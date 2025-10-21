%% Start 
clear; close all; font_size=15;
load compute.out;
load thermo.out;
delta_T = compute(:, 1) - compute(:, 2);

Lx = thermo(end, 10);
Ly = thermo(end, 11);
Lz = thermo(end, 12);
%% Some parameters from MD
dt = 0.001;	                                         % timesteps in MD simulation (ps)
sample_interval = 1000;                              % output_interval (For Gr and Hbn)

N_Gr = 12544;				                         % number of atoms in Gr
N_Hbn = 12100;	                                     % number of atoms in Hbn

real_dt = dt * sample_interval;				         % time interval in units of ps (its inverse is roughly the maximum frequency attainable)

%% Get heat_capacity for Gr(call test.m)
Kb = 1.38e-23;                                        % J/K
Cv_Gr = 3 * N_Gr * Kb;
Cv_Hbn = 3 * N_Hbn * Kb;

Cv_total = Cv_Gr*Cv_Hbn/(Cv_Gr + Cv_Hbn);

%% Read heat flux data and Get tau
% fitting point for endding

end_point = 500;
t = transpose((1:1:end_point)*real_dt);				  % ps
delta_T = delta_T(1:end_point);                            

% Fitting and get tau

myfittype = fittype([num2str((delta_T(1))), '*exp((t(1)-t)/tau)'], 'dependent', {'delta_T'}, ...
               'independent', {'t'}, 'coefficients', {'tau'});    %%% cfun(t) = delta_T(1)*exp((t(1)-t)/tau)

[cfun, rsquare] = fit(t, delta_T, myfittype, 'Lower', 0);

tau = coeffvalues(cfun)                                     % ps
tau = tau * 1.0e-12;                                        % ps ---------------->s

%% Get G

A = Lx * Ly * 1e-20;                                % A^2 --> m^2          

G = Cv_total / tau / A / 1e6                        % MW/m^2/K (since J/s = W)

%% plot
figure(1);
plot(cfun, t, delta_T);
% hold on;
% plot((1:1:length(compute(:, 1)))*real_dt, compute(:, 1));
% hold on;
% plot((1:1:length(compute(:, 1)))*real_dt, compute(:, 2));

xlabel('t (ps)','fontsize', font_size);
ylabel('Delta T (K)', 'fontsize', font_size);
set(gca,'fontsize', font_size);

% Save the plot data in a text file
fitted_delta_T = feval(cfun, t); 
save('plot_data.mat', 't', 'delta_T', 'fitted_delta_T');  


