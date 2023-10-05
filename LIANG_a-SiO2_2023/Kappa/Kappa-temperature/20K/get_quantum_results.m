%% Get file from folder
clear; close all; font_size = 12;

%% Get T
path = pwd;
[~, foldername, ~] = fileparts(path);
digits = regexp(foldername, '\d+', 'match');
T = str2double(digits{1});                     %% K

%% run plot_shc.m files
runs = 5;
nu_container = [];
kappa_container = [];
kappa_quan_container = [];
trapz_kappa = [];
trapz_kappa_quan = [];

for i=1:runs

    copyfile('plot_shc.m', ['run_',num2str(i)], 'f');
    cd(['run_',num2str(i)]); 
    
    [nu, kappa, kappa_quan] = plot_shc(T);

    trapz_kappa = [trapz_kappa, trapz(nu, kappa)];
    trapz_kappa_quan = [trapz_kappa_quan, trapz(nu, kappa_quan)];

    nu_container = [nu_container, nu];
    kappa_container = [kappa_container, kappa];
    kappa_quan_container = [kappa_quan_container, kappa_quan];
    cd ..;

end

%% Report results

disp(['\nkappa_ave_from_SHC = (', num2str(mean(trapz_kappa)), ' +- ', num2str(std(trapz_kappa)), ') W/mK']);
disp(['kappa_quan_ave_from_SHC = (', num2str(mean(trapz_kappa_quan)), ' +- ', num2str(std(trapz_kappa_quan)), ') W/mK']);

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');
%% Average the kappa and kappa_qaun from SHC

kappa_classical_aver = mean(kappa_container, 2);
kappa_quantum_aver = mean(kappa_quan_container, 2);
error_classical = std(kappa_container, [], 2);
error_quantum = std(kappa_quan_container, [], 2);

%% Plot figures
color_1 = [0.64, 0.08, 0.18];
color_2 = [0.47, 0.67, 0.19];

figure('Position', [100, 100, 500, 400]);

%% Plot shade
plot_option = '';
shade_color = [0.86 0.86 0.86];

% Plot the error region using fill
errorshade2(nu, kappa_classical_aver, 0, error_classical, plot_option, shade_color);
hold on;

errorshade2(nu, kappa_quantum_aver, 0, error_quantum, plot_option, shade_color);
hold on;

%% Plot line
h1 = plot(nu, kappa_classical_aver, '-', 'linewidth', 2.5, 'Color', color_1);
hold on;
h2 = plot(nu, kappa_quantum_aver, '-', 'linewidth', 2.5, 'Color', color_2);
hold off;

xlabel('$\omega$/2$\pi$ (THz)');
ylabel('$\kappa(\omega)$ (W/m/K/THz)');

ylim([-0.01, 0.15]);
xlim([0, 40]);
box on;

legend([h1, h2], ['Classical ', num2str(T),' K'], ['Quantum ', num2str(T),' K'], 'location', 'northeast', 'NumColumns', 1, 'Box', 'off');

set(gca,'fontsize', 20, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

%print('kappa_classical_vs_quantum.svg', '-dsvg', '-painters');





