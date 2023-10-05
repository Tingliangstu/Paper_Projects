%% Start 
clear; close all; 

%% load train data
loss = load('loss.out');
loss(:, 1) = (1:length(loss))'*100;
fprintf("We have run %d steps!\n", loss(end, 1));
energy_train = load('energy_train.out');
force_train = load('force_train.out');
virial_train = load('virial_train.out');
energy_test = load('energy_test.out');
force_test = load('force_test.out');
virial_test = load('virial_test.out');

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter','latex');  
set(groot, 'defaultAxesTickLabelInterpreter','latex');  
set(groot, 'defaultLegendInterpreter','latex');

%% Figure 1 for Loss
text_font_size = 15;

figure('Position', [100, 100, 500, 500]);
lw = 2.0;
loglog(loss(:,1), loss(:,3), '-', 'LineWidth', lw, 'DisplayName', 'L1');
hold on;
loglog(loss(:,1), loss(:,4), '-', 'LineWidth', lw, 'DisplayName', 'L2');
hold on;
loglog(loss(:,1), loss(:,5), '-', 'LineWidth', lw, 'DisplayName', 'Energy train');
hold on;
loglog(loss(:,1), loss(:,6), '-', 'LineWidth', lw, 'DisplayName', 'Force train');
hold on;
loglog(loss(:,1), loss(:,7), '-', 'LineWidth', lw, 'DisplayName', 'Virial train');
hold on;
xlim([1e2,1e6]);
ylim([1e-3,1e0]);
xlabel('Generation');
ylabel('Loss');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2);
%saveas(gcf, 'Loss.svg');

%% Figure 2 for training energy
figure('Position', [100, 100, 500, 500]);

scatter(energy_train(:,2), energy_train(:,1),'o','filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
scatter(energy_test(:,2), energy_test(:,1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
plot([-12, 0], [-12, 0], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);

text(-8.9, -10.2, sprintf('Train RMSE = %4.1f meV/atom', loss(end, 5)*1000),...
            'FontSize', text_font_size, 'FontName', 'latex');
text(-8.9, -11.0, sprintf('Test RMSE = %4.1f meV/atom', loss(end, 8)*1000),...
            'FontSize', text_font_size, 'FontName', 'latex');

xlim([-12, 0]);
ylim([-12, 0]);
xticks(-12:3:0);
yticks(-12:3:0);

xlabel('DFT energy (eV/atom)');
ylabel('NEP energy (eV/atom)');
axis tight;

legend('Train dataset', 'Test dataset');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%saveas(gcf, 'Energy.svg');
%% Figure 3 for training force
figure('Position', [200, 100, 500, 500]);

% Reshape force data
DFT_force_train = [force_train(:, 4); force_train(:, 5); force_train(:, 6)];
NEP_force_train = [force_train(:, 1); force_train(:, 2); force_train(:, 3)];

DFT_force_test = [force_test(:, 4); force_test(:, 5); force_test(:, 6)];
NEP_force_test = [force_test(:, 1); force_test(:, 2); force_test(:, 3)];

% Plot
scatter(DFT_force_train, NEP_force_train, 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
scatter(DFT_force_test, NEP_force_test, 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;

text(-22.0, -32.0, sprintf('Train RMSE = %4.1f meV/{\\AA}', loss(end, 6)*1000), 'FontSize', text_font_size, 'FontName', 'latex');
text(-22.0, -38.0, sprintf('Test RMSE = %4.1f meV/{\\AA}', loss(end, 9)*1000), 'FontSize', text_font_size, 'FontName', 'latex');

plot([-45, 45], [-45, 45], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);
xlim([-45, 45]);
ylim([-45, 45]);

xlabel('DFT force (eV/{\AA})');
ylabel('NEP force (eV/{\AA})');

legend('Train dataset', 'Test dataset');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%print('filename.svg','-dsvg','-r1000');

%% Figure 4 for training Virial
figure('Position', [100, 100, 500, 500]);

scatter(virial_train(:,2), virial_train(:,1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
scatter(virial_test(:,2), virial_test(:,1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);

plot([-4,7], [-4,7], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);

text(-1.5, -2.5, sprintf('Train RMSE  = %4.1f meV/atom', loss(end, 7)*1000), 'FontSize', text_font_size, 'FontName', 'latex');
text(-1.5, -3.3, sprintf('Test RMSE = %4.1f meV/atom', loss(end, 10)*1000), 'FontSize', text_font_size, 'FontName', 'latex');

xlim([-4, 7]);
ylim([-4, 7]);

xlabel('DFT virial (eV/atom)');
ylabel('NEP virial (eV/atom)');
legend('Train dataset', 'Test dataset');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');
%saveas(gcf, 'virial.svg');


