%% Get file from folder
clear; close all; font_size = 10; 
load shc.out; 
load temp_difference.mat; 

%% Parameters from compute_shc (check your run.in file)
Nc = 500;                         % second parameter
Nw = 1000;                        % fourth parameter
DT = temp_difference;             % Temperature difference (K) from checking compute.out

%% Parameters from model (check your xyz.in file)
Lz_system_length = 8;             % length in transport direction for the chosen group (A)
Lx = 103.716;                     % A
Ly = 103.716;                     % A

V = Lx*Ly*Lz_system_length;       % volume of the chosen group (A^3)

%% Calculated parameters and results
% Ref. [1]:  Z. Fan et al., PRB 99, 064308 (2019)

Nt = Nc*2-1;
Ns=size(shc, 1) / (Nt + Nw);                    % number of independent run
time_in_ps = shc(1:Nt, 1);                        % correlation time t (ps)

data =reshape((sum(shc(:, 2:3), 2)), Nt+Nw, Ns);     % Eq. (18) in Ref. [1] divided by length (eV/ps)
nu=shc(Nt+1:(Nt + Nw), 1)/2/pi;                             % frequency (THz)

for i = 1:Ns
        
        shc = data(:, i);
        K = data(1:Nt, i) / Lz_system_length;                         % Eq. (18) in Ref. [1] divided by length (eV/ps)
        J = data(Nt+1:end, i);                                        % left part of Eq. (20) in Ref. [1] (A*eV/ps/THz)   
        Gc(:, i) = 1.6e4*J/V/DT(i);                                   % spectral thermal conductance (GW/m^2/K/THz)

        %% Plot results
        figure;
        subplot(1, 2, 1);
        plot(time_in_ps, K, 'b-', 'linewidth', 2);
        set(gca, 'fontsize', font_size);
        xlabel('Correlation time (ps)', 'fontsize', font_size);
        ylabel('K (eV/ps)', 'fontsize', font_size);
        title('(a)');

        subplot(1,2,2);
        plot(nu, Gc(:, i), 'b-', 'linewidth', 1.5);
        set(gca, 'fontsize', font_size);
        xlabel('$\omega$/2$\pi$ (THz)','fontsize', font_size);
        ylabel('G($\omega$) (GW/m$^2$/K/THz)','fontsize', font_size);
        xlim([0, 60]);
        set(gca,'ticklength',get(gca,'ticklength')*3,'xtick', 0:10:50);
        title('(b)');

        % Check consistency
        sum(Gc(:, i), 1) * (nu(2)-nu(1))   

end

%% save files

Gc = mean(Gc, 2);
save('nu_Gc',  'nu', 'Gc');                           % will be used in the diffusive/plot_shc.m file

