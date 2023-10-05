%% Plotting script for dynamic quantites from dynasor output file.
clear all;
close all;
clc;

% Conversion factors
hbar = 1.05457173*1e-34; % m2 kg / s
J2ev = 6.24150934e18;

% Load dynasor output
dynasor_T300_dynamical;
w=hbar*w*J2ev*1000*1e15*0.242;   % from meV to THz
t = t/1000;                      % From fs to ps

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% Plot partial intermediate scattering function (Normalized)
q_1 = 3;                % Two k-values
q_2 = 5;

figure('Position', [400, 100, 1000, 600]);
lw = 2;
xmax = 40;  %% ps

%% Figure 1
subplot(1, 2, 1);
plot(t, F_q_t_0_0(:, q_1)/max(F_q_t_0_0(:, q_1)), 'r-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'));

xlim([0, xmax]);
xlabel('Time (ps)');
ylabel('$F$($q$,$t$) (Normalized)');

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Figure 2
subplot(1, 2, 2);
plot(t, F_q_t_0_0(:, q_2)/max(F_q_t_0_0(:, q_2)), 'b-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, xmax]);
xlabel('Time (ps)');
ylabel('$F$($q$,$t$) (Normalized)');

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Partial dynamical structure factor 
figure('Position', [400, 150, 600, 450]);

plot(w(2:end), S_q_w_0_0(2:end, q_1), 'r-', 'LineWidth', lw);
hold on;
plot(w(2:end), S_q_w_0_0(2:end, q_2), 'b-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'), strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, 15]);
xlabel('Frequency (THz)');
ylabel('$S$($q$,$\omega$)');
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% Longitudinal and transversal partial current correlations Cl(q,t), Ct(q,t)
figure('Position', [400, 100, 1000, 600]);
subplot(1, 2, 1);
plot(t, Cl_q_t_0_0(:, q_1)/max(Cl_q_t_0_0(:, q_1)), 'r-', 'LineWidth', lw);
hold on;
plot(t, Cl_q_t_0_0(:, q_2)/max(Cl_q_t_0_0(:, q_2)), 'b-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'), strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, xmax]);
xlabel('Time (ps)');
ylabel('$C_{l}$($q$,$t$) (Normalized)');
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

% transversal 
subplot(1, 2, 2);
plot(t, Ct_q_t_0_0(:, q_1)/max(Ct_q_t_0_0(:, q_1)), 'r-', 'LineWidth', lw);
hold on;
plot(t, Ct_q_t_0_0(:, q_2)/max(Ct_q_t_0_0(:, q_2)), 'b-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'), strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, xmax]);
xlabel('Time (ps)');
ylabel('$C_{t}$($q$,$t$) (Normalized)');
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%% map of Longitudinal and transversal partial current correlations Cl(k, w) and Ct(k, w)
figure('Position', [400, 100, 800, 500]);

start_q = 1;

subplot(1,2,1);
surf(q(start_q:end), w, Cl_q_w_0_0(:, start_q:end));
shading interp; 
colormap Sky; 

%colorbar; 

xlim([0, 5]);
ylim([0, 5]);
clim([0.000005, 0.0001]);

xlabel('$q$ (nm$^{-1}$)');
ylabel('$\omega$/2$\pi$ (THz)');
title('$C_{l}$($q$, $\omega$)');
view([0 90]);

set(gca, 'xtick', 1*(0:1:5), 'ytick', 1*(0:1:5));
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*0.01, 'linewidth', 0.01);

% Ct
subplot(1,2,2);
surf(q(start_q:end), w, Ct_q_w_0_0(:, start_q:end));
shading interp; 
colormap Sky; 
%colorbar; 

xlim([0, 5]);
ylim([0, 5]);
clim([0.000005, 0.0001]);
box off;

xlabel('$q$ (nm$^{-1}$)');
ylabel('$\omega$/2$\pi$ (THz)');
title('$C_{t}$($q$, $\omega$)');
view([0 90]);

set(gca, 'xtick', 1*(0:1:5), 'ytick', 1*(0:1:5));
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*0.01, 'linewidth', 0.01);
%print('Current_Cl_Ct.svg', '-dsvg', '-painters');

%% Plot Sq-Transverse and Sq-longitudinal part
figure('Position', [400, 100, 1000, 600]);

for i = 1:length(q)
   for j = 1:length(w)

       Sq_L(j, i) = Cl_q_w_0_0(j, i)*(q(i)^2)/(w(j)^2);
       Sq_T(j, i) = Ct_q_w_0_0(j, i)*(q(i)^2)/(w(j)^2);

   end
end

% transversal 
subplot(1, 2, 1);
plot(w(1:end), Ct_q_w_0_0(1:end, q_1), 'o-', 'LineWidth', lw);
hold on;
plot(w(1:end), Ct_q_w_0_0(1:end, q_2), 'o-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'), strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, 2]);
ylim([0, 0.0005]);
xlabel('$\omega$/2$\pi$ (THz)');
ylabel('$C_{T}$($q$, $\omega$)');
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

% longitudinal part
subplot(1, 2, 2);
plot(w(1:end), Cl_q_w_0_0(1:end, q_1), 'o-', 'LineWidth', lw);
hold on;
plot(w(1:end), Cl_q_w_0_0(1:end, q_2), 'o-', 'LineWidth', lw);

h=legend(strcat('$k$ = ', num2str(q(q_1)), ' nm$^{-1}$'), strcat('$k$ = ', num2str(q(q_2)), ' nm$^{-1}$'));

xlim([0, 2]);
ylim([0, 0.0004]);
xlabel('$\omega$/2$\pi$ (THz)');
ylabel('$C_{L}$($q$, $\omega$)');
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

% %% smooth map of Ct(k,w) and Cl(k,w)
% ave = 20;
% smooth_CL = zeros(length(w), length(q(start_q:end)));
% smooth_CT = zeros(length(w), length(q(start_q:end)));
% 
% for i=1:length(q)
%     smooth_CL(:, i) = smooth(Cl_q_w_0_0(:, i), ave, 'lowess');
%     smooth_CT(:, i) = smooth(Ct_q_w_0_0(:, i), ave, 'lowess');
% end
% 
% %% Plot smoothed 
% figure('Position', [400, 100, 1000, 600]);
% 
% subplot(1,2,1);
% surf(q(start_q:end), w, smooth_CL(:, start_q:end));
% shading interp; 
% colormap Sky; 
% %colorbar; 
% 
% xlim([0, 6]);
% ylim([0, 5]);
% clim([0.000005, 0.00005]);
% 
% ylabel('$\omega$ (THz)');
% xlabel('$q$ (nm$^{-1}$)');
% title('Smooth $C_{l}$($q$, $\omega$)');
% view([0 90])
% set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);
% 
% % Ct
% subplot(1,2,2);
% surf(q(start_q:end), w, smooth_CT(:, start_q:end));
% shading interp; 
% colormap Sky; 
% %colorbar; 
% 
% xlim([0, 6]);
% ylim([0, 5]);
% clim([0.000005, 0.00005]);
% 
% ylabel('$\omega$ (THz)');
% xlabel('$q$ (nm$^{-1}$)');
% title('Smooth $C_{t}$($q$, $\omega$)');
% view([0 90]);
% set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

