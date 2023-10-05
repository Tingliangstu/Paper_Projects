%% Start 
clear; close all;

%% Load NEP test data (NEP_test_Full_Batch_6_4_2348_v-0.1_neu-80 -- test-dataset-261)
nep_energy_test = load('energy_test.out');
nep_force_test = load('force_test.out');
nep_virial_test = load('virial_test.out');

%% Load GaP test data (https://doi.org/10.1038/s41524-022-00768-w)
gap_energy_comparison = load('energy_comparison.txt');
gap_force_comparison = load('force_comparison.txt');
gap_virial_comparison = load('virial_comparison.txt');

%% Calculate RMSE from NEP
nep_energy_test_rmse = get_rmse(nep_energy_test(:, 1), nep_energy_test(:, 2));           % eV
nep_force_test_rmse = get_rmse(reshape(nep_force_test(:, 1:3), [], 1), reshape(nep_force_test(:, 4:6), [], 1)); % ev/A

%% Call get_true_virial_of_nep function
[new_nep_virial_nep, new_nep_virial_dft] = get_true_virial_of_nep(nep_virial_test, 5);
nep_virial_test_rmse = get_rmse(new_nep_virial_nep, new_nep_virial_dft);

%% Calculate RMSE from GAP
gap_energy_rmse = get_rmse(gap_energy_comparison(:, 1), gap_energy_comparison(:, 2));    % eV
gap_force_rmse = get_rmse(reshape(gap_force_comparison(:, 1:3), [], 1), reshape(gap_force_comparison(:, 4:6), [], 1)); % ev/A

%% gap_virial_rmse = get_rmse(new_gap_virial_gap, new_gap_virial_dft);
gap_virial_rmse = get_rmse(gap_virial_comparison(:, 1), -gap_virial_comparison(:, 2));

%% Enable setings about latex interpreter
set(groot,'defaulttextinterpreter','latex');  
set(groot, 'defaultAxesTickLabelInterpreter','latex');  
set(groot, 'defaultLegendInterpreter','latex');

%% Plot Energy figure
figure('Position', [100, 100, 1200, 500]);
text_font_size = 11;

subplot(1, 3, 1);

scatter(gap_energy_comparison(:, 2), gap_energy_comparison(:, 1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
scatter(nep_energy_test(:, 2), nep_energy_test(:, 1),'o','filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;

plot([-12, 0], [-12, 0], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);

text(-9.7, -11.3, sprintf('GAP RMSE = %4.1f meV/atom', gap_energy_rmse*1000),...
            'FontSize', text_font_size, 'FontName', 'latex');
text(-9.7, -10.5, sprintf('NEP RMSE = %4.1f meV/atom', nep_energy_test_rmse*1000),...
            'FontSize', text_font_size, 'FontName', 'latex');

xlim([-12, 0]);
ylim([-12, 0]);
xticks(-12:3:0);
yticks(-12:3:0);

xlabel('DFT energy (eV/atom)')
ylabel('Predicted energy (eV/atom)')

legend('GAP prediction', 'NEP prediction');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%% Plot force figure
subplot(1, 3, 2);

% Reshape force data
DFT_force_nep = [nep_force_test(:, 4); nep_force_test(:, 5); nep_force_test(:, 6)];
NEP_force = [nep_force_test(:, 1); nep_force_test(:, 2); nep_force_test(:, 3)];

DFT_force_Gap = [gap_force_comparison(:, 4); gap_force_comparison(:, 5); gap_force_comparison(:, 6)];
Gap_force = [gap_force_comparison(:, 1); gap_force_comparison(:, 2); gap_force_comparison(:, 3)];

% plot

scatter(DFT_force_Gap, Gap_force, 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;

scatter(DFT_force_nep, NEP_force, 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;

text(-27.0, -39.0, sprintf('GAP RMSE = %4.1f meV/{\\AA}', gap_force_rmse*1000), 'FontSize', text_font_size, 'FontName', 'latex');
text(-27.0, -33.0, sprintf('NEP RMSE = %4.1f meV/{\\AA}', nep_force_test_rmse*1000), 'FontSize', text_font_size, 'FontName', 'latex');

plot([-45, 45], [-45, 45], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);
xlim([-45, 45]);
ylim([-45, 45]);

xlabel('DFT force (eV/{\AA})');
ylabel('Predicted force (eV/{\AA})');

legend('GAP prediction', 'NEP prediction');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%% Plot virial figure
subplot(1, 3, 3);

scatter(gap_virial_comparison(:,2), -gap_virial_comparison(:,1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;
scatter(nep_virial_test(:,2), nep_virial_test(:,1), 'o', 'filled', 'SizeData', 100, 'MarkerFaceAlpha', 0.4);
hold on;

plot([-4,7], [-4,7], '--', 'Color', [0.5 0.5 0.5], 'LineWidth', 2);

text(-2.1, -3.5, sprintf('GAP RMSE = %4.1f meV/atom', gap_virial_rmse*1000), 'FontSize', text_font_size, 'FontName', 'latex');
text(-2.0, -2.8, sprintf('NEP RMSE  = %4.1f meV/atom', nep_virial_test_rmse*1000), 'FontSize', text_font_size, 'FontName', 'latex');

xlim([-4, 7]);
ylim([-4, 7]);

xlabel('DFT virial (eV/atom)');
ylabel('Predicted virial (eV/atom)');

legend('GAP prediction', 'NEP prediction');
legend boxoff;

set(gca,'fontsize', 18, 'ticklength', get(gca,'ticklength')*2, 'linewidth', 2, 'Box', 'on');

%print('Compare_NEP_GAP.svg', '-dsvg', '-painters');


%% %%%%%%%%%%%%%%%%%%%%%%%%% The following is the sub-function  %%%%%%%%%%%%%%%%%%%%%%%%
%% Calculte rmse
function [rmse] = get_rmse(predicted_data, dft_data)
  squared_error = [];
  for i = 1:length(predicted_data)
    squared_error(end+1) = (predicted_data(i)-dft_data(i))^2;
  end
  rmse = sqrt(sum(squared_error) / length(squared_error));
end

%% Removed virial without ref
function [new_nep_virial_nep, new_nep_virial_dft] = get_true_virial_of_nep(virial_data, diff_tol)
  new_nep_virial_nep = [];
  new_nep_virial_dft = [];
  for i = 1:length(virial_data(:,1))
      if abs(virial_data(i, 1) - virial_data(i, 2)) < diff_tol
        new_nep_virial_nep(end+1) = virial_data(i, 1);
        new_nep_virial_dft(end+1) = virial_data(i, 2);
      end
  end

end