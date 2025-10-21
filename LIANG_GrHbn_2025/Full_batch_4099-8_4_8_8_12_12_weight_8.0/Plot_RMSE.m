%% Start 
clear; close all; 

%% load train data
loss = load('loss.out');
loss(:, 1) = (1:length(loss))'*100;
fprintf("We have run %d steps!\n", loss(end, 1));
energy_train = load('energy_train.out');
force_train = load('force_train.out');
virial_train = load('virial_train.out');

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter','latex');  
set(groot, 'defaultAxesTickLabelInterpreter','latex');  
set(groot, 'defaultLegendInterpreter','latex');

%% Figure 1 for Loss
text_font_size = 15;

Color_1 = [80, 29, 138]/255;
Color_2 = [170, 52, 116]/255;
Color_3 = [210, 140, 120]/255;

figure('Position', [100, 100, 500, 500]);
tran = 0.8;
lw = 1.5;

a=loglog(loss(:,1), loss(:,3), '-', 'LineWidth', lw, 'DisplayName', '$\mathcal{L}_1$');
a.Color(4) = tran; 
hold on;
b=loglog(loss(:,1), loss(:,4), '-', 'LineWidth', lw, 'DisplayName', '$\mathcal{L}_2$');
b.Color(4) = tran; 
hold on;
c=loglog(loss(:,1), loss(:,5), '-', 'LineWidth', lw, 'DisplayName', 'Energy train');
c.Color(4) = 0.6; 
hold on;
d=loglog(loss(:,1), loss(:,6), '-', 'LineWidth', lw, 'DisplayName', 'Force train');
d.Color(4) = tran; 
hold on;
e=loglog(loss(:,1), loss(:,7), '-', 'LineWidth', lw, 'DisplayName', 'Virial train');
e.Color(4) = tran; 
hold on;
xlim([1e2,1.1e6]);
ylim([6e-4,1e0]);
xlabel('Generation');
ylabel('Loss');
legend boxoff;

set(gca,'fontsize', 16, 'ticklength', get(gca,'ticklength')*1.5, 'linewidth', 1.2);
%saveas(gcf, 'Loss.svg');
%print('Loss.svg', '-dsvg', '-painters');

%% Figure 2 for training energy
figure('Position', [100, 100, 500, 500]);

scatter(energy_train(:,2), energy_train(:,1),'o','filled', 'SizeData', 80, 'MarkerFaceAlpha', 0.4);
hold on;

plot([-9.5, -8.0], [-9.5, -8.0], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2.0);

text(-9.18, -9.35, sprintf('Energy RMSE = %4.1f meV/atom', loss(end, 5)*1000),...
            'FontSize', text_font_size, 'FontName', 'latex');

xlim([-9.5, -8.0]);
ylim([-9.5, -8.0]);

xlabel('DFT energy (eV/atom)');
ylabel('NEP energy (eV/atom)');
axis tight;

%legend('Train dataset');
%legend boxoff;

set(gca,'fontsize', 16, 'ticklength', get(gca,'ticklength')*1.5, 'linewidth', 1.2, 'Box', 'on');

%saveas(gcf, 'Energy.svg');
%% Figure 3 for training force
figure('Position', [200, 100, 500, 500]);

% Reshape force data
DFT_force_train = [force_train(:, 4); force_train(:, 5); force_train(:, 6)];
NEP_force_train = [force_train(:, 1); force_train(:, 2); force_train(:, 3)];

% Plot
scatter(DFT_force_train, NEP_force_train, 'o', 'filled', 'MarkerFaceColor', Color_2, 'SizeData', 80, 'MarkerFaceAlpha', 0.4);
hold on;

text(-19.0, -31.0, sprintf('Force RMSE = %4.1f meV/{\\AA}', loss(end, 6)*1000), 'FontSize', text_font_size, 'FontName', 'latex');

plot([-40, 40], [-40, 40], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);
xlim([-40, 40]);
ylim([-40, 40]);

xticks(-40:20:40);
yticks(-40:20:40);

xlabel('DFT force (eV/{\AA})');
ylabel('NEP force (eV/{\AA})');

%legend('Train dataset');
%legend boxoff;

set(gca,'fontsize', 16, 'ticklength', get(gca,'ticklength')*1.5, 'linewidth', 1.2, 'Box', 'on');

%print('filename.svg','-dsvg','-r1000');

%% Figure 4 for training Virial
figure('Position', [100, 100, 500, 500]);

% Reshape virial data
DFT_virial_train = [virial_train(:, 7); virial_train(:, 8); virial_train(:, 9);
                    virial_train(:, 10);virial_train(:, 11); virial_train(:, 12)];
NEP_virial_train = [virial_train(:, 1); virial_train(:, 2); virial_train(:, 3);
                    virial_train(:, 4);virial_train(:, 5); virial_train(:, 6)];

scatter(DFT_virial_train, NEP_virial_train, 'o', 'filled', 'MarkerFaceColor', Color_3, 'SizeData', 80, 'MarkerFaceAlpha', 0.4);
hold on;

plot([-2,6], [-2,6], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);

text(-0, -1.2, sprintf('Virial RMSE  = %4.1f meV/atom', loss(end, 7)*1000), 'FontSize', text_font_size, 'FontName', 'latex');

xlim([-2, 6]);
ylim([-2, 6]);

xticks(-2:2:6);
yticks(-2:2:6);

xlabel('DFT virial (eV/atom)');
ylabel('NEP virial (eV/atom)');

%legend boxoff;

set(gca,'fontsize', 16, 'ticklength', get(gca,'ticklength')*1.5, 'linewidth', 1.2, 'Box', 'on');
%saveas(gcf, 'virial.svg');


