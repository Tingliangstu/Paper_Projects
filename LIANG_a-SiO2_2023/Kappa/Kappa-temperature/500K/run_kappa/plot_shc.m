function [nu, kappa, kappa_quan] = plot_shc(T)
%% Get file from folder

font_size = 12;
load shc.out; 

%% parameters from compute_shc (check your run.in file)
Nc=500;                 % second parameter
Nw=1000;                % fourth parameter                                 % (number of omega)
Fe=0.0002;              % driving force parameter (1/A)

%% parameters from model (check your xyz.in file)
load thermo.out;
Lx = thermo(end, 10);
Ly = thermo(end, 11);
Lz = thermo(end, 12);
V = Lx*Ly*Lz;                       % volume of the chosen group (A^3)
%% For temperature
disp(['Now the temperature is ', num2str(T), ' K']);

%% calculated parameters and results
% Ref. [1]:  Z. Fan et al., PRB 99, 064308 (2019)
Nt = Nc*2-1;
time_in_ps = shc(1:Nt, 1);                          % correlation time t (ps)
K = sum(shc(1:Nt, 2:3), 2)/Lz;                      % Eq. (18) in Ref. [1] divided by length (so the unit is eV/ps)
nu = shc(Nt+1:end, 1)/2/pi;                         % frequency (THz)
J = sum(shc(Nt+1:end, 2:3), 2);                     % left part of Eq. (20) in Ref. [1] (A*eV/ps/THz)
kappa = 1.6e3*J/V/T/Fe;                             % left part of Eq. (21) in Ref. [1] (W/m/K/THz)

%% >>> quantum corrected factor >>>>>>>>>>>>>>>>>>>>>>>
hnu = 6.63e-34 * nu * 1.0e12; 
kBT = 1.38e-23 * T;
x = hnu/kBT; 
f = x.*x.*exp(x)./(exp(x)-1).^2;     

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter', 'latex');  
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');  
set(groot, 'defaultLegendInterpreter', 'latex');

%% plot results
figure;
plot(time_in_ps, K, 'b-', 'linewidth', 2);
xlabel('Correlation time (ps)', 'fontsize', font_size);
ylabel('K (eV/ps)','fontsize', font_size);
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);


figure;
plot(nu, kappa, 'k-', 'linewidth', 2); 
hold on;
kappa_quan=kappa.*f;
plot(nu, kappa_quan, 'm-','linewidth', 2);

set(gca,'fontsize', 12, 'ticklength', get(gca,'ticklength')*1, 'linewidth', 1);
xlabel('$\omega$/2$\pi$ (THz)','fontsize', font_size);
ylabel('$\kappa(\omega)$ (W/m/K/THz)','fontsize', font_size);
ylim([-0.01, 0.2]);
xlim([0, 40]);
set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);

save('shc_nu_class_quan', 'nu', 'kappa', 'kappa_quan');

%% disp
disp(['kappa_from_SHC = ', num2str(trapz(nu, kappa)), ' W/mK']);
disp(['kappa_from_SHC_with_quantum = ', num2str(trapz(nu, kappa_quan)), ' W/mK']);

end

