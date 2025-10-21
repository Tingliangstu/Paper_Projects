%% Get file from folder
clear;  close all; 
font_size = 15; 

load compute.out;  
temperature=compute;

%% Some parameters from MD
dt = 0.0005;                         % ps
Ns = 1000;                           % sample interval  (1000 timestep ---->>> 10*100)
run_step = 5000000;

every_data_column = run_step / Ns;
N_temp = size(temperature, 1);
Total_Ns = N_temp/every_data_column;

%% data block
temp_total = zeros(every_data_column, size(temperature, 2), Total_Ns);

for i = 1:Total_Ns

    index = every_data_column * (i-1) + 1;
    index_1 = every_data_column * i;
    temp_total(:, :, i) =  temperature(index : index_1, :);

end

temp_difference = zeros(1, Total_Ns);

for j = 1:Total_Ns

    temp = temp_total(:, :, j);
    temp_ave = mean(temp(end/2+1:end, 2:end-2));
    temp_difference(:, j) = temp_ave(12) - temp_ave(11);

end

save('temp_difference', 'temp_difference');   % will be used in the plot_shc_NEMD.m file
save('temp_ave', 'temp_ave');   % will be used in the plot_shc_NEMD.m file

%% Model parameters 
load thermo.out
lx = thermo(end, end-2);
ly = thermo(end, end-1);
A = lx * ly / 100;                            % nm^2

%% Temperature profile
for i = 1:Total_Ns

    temperature = temp_total(:, :, i);
    figure;
    
    plot(mean(temperature(end/2+1:end, 2:end-2)), 'bo-', 'linewidth', 2);
    xlabel('group index', 'fontsize', font_size);
    ylabel('T (K)', 'fontsize', font_size);
    set(gca,'fontsize', font_size);
    title('(a)');

    %% Energy exchange between the system and the thermostats
    figure;
    t = dt*(1:N_temp/Total_Ns) * Ns / 1000;  % ns

    % plot from half data, since the initial process not convergence

    energy_source = (temperature(end/2+1:end, end-1) - temperature(end/2+1, end-1))/1000;  % KeV
    energy_sink = (temperature(end/2+1:end, end) - temperature(end/2+1, end))/1000;        % KeV

    plot(t(1:end/2), energy_source, 'r-', 'linewidth', 2);
    hold on;
    plot(t(1:end/2), energy_sink, 'b--', 'linewidth', 2);
    hold on;

    xlabel('t (ns)', 'fontsize', font_size);
    ylabel('Heat (KeV)', 'fontsize', font_size);
    set(gca,'fontsize', font_size);
    legend('source', 'sink');
    title('(b)');

    %%  Heat flux calculated from the thermostats
    Q1 = (temperature(end/2, end-1)-temperature(end, end-1))/(every_data_column/2)/dt/Ns;
    Q2 = (temperature(end, end)-temperature(end/2, end))/(every_data_column/2)/dt/Ns;

    Q = (Q1+Q2)/2;                                       %% eV/ps

    %% Classical ballistic conductance
    G(:, i) = 160*Q/A/temp_difference(:, i) * 1000       %% GW/m^2K   (using 160 for unit conversion)

    %% Get thermal conductivity in NEMD calculations

    % length_in_m = system_length * 1.0e-9;                             % m

    % kappa(:, i) = G(:, i) * 1.0e9 * length_in_m;                      % GW --->>> W

end

%ave_kappa = mean(kappa);
%disp(['The thermal conductivity of the system is   ', num2str(ave_kappa), '   W/mK'])




