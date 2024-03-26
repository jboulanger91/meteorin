
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind
from extract_positions_convergence_speed import extract_positions_convergence_speed

# Videos have been downsampled to reduce size 
down = 2
# Pixel size
pix_size = 0.637

# Path to the Excel file
path_data = '/Users/jonathanboulanger-weill/Desktop/Projects/meteorin/dfc_tracking/dfc_tracking_data.xlsx'
wt_cp = []; wt_cv=[]; wt_ms=[]
mut_cp = []; mut_cv=[]; mut_ms=[]

# Load individual sheets 
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=0), pix_size * down)
wt_cp.append(wt1_centered_positions); wt_cv.append(wt1_conv_ratio); wt_ms.append(wt1_mig_speed)
wt2_centered_positions, wt2_conv_ratio, wt2_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=1), pix_size * down)
wt_cp.append(wt2_centered_positions); wt_cv.append(wt2_conv_ratio); wt_ms.append(wt2_mig_speed)
wt3_centered_positions, wt3_conv_ratio, wt3_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=2), pix_size * down)
wt_cp.append(wt3_centered_positions); wt_cv.append(wt3_conv_ratio); wt_ms.append(wt3_mig_speed)

mut1_centered_positions, mut1_conv_ratio, mut1_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=3), pix_size * down)
mut_cp.append(mut1_centered_positions); mut_cv.append(mut1_conv_ratio); mut_ms.append(mut1_mig_speed)
mut2_centered_positions, mut2_conv_ratio, mut2_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=4), pix_size * down)
mut_cp.append(mut2_centered_positions); mut_cv.append(mut2_conv_ratio); mut_ms.append(mut2_mig_speed)
mut3_centered_positions, mut3_conv_ratio, mut3_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=5), pix_size * down)
mut_cp.append(mut3_centered_positions); mut_cv.append(mut3_conv_ratio); mut_ms.append(mut3_mig_speed)

#Make figures 
font = {'family': 'Arial','weight': 'normal','size': 12}
plt.rcParams['font.family'] = 'Arial'

# Show trajectories for each video 
#WT
samples = ['wt1_18012024', 'wt2_20022024', 'wt3_14032024']
fig, axs = plt.subplots(1, 3, subplot_kw=dict(box_aspect=1), sharex=True, sharey=True, layout="constrained")
for i, ax in enumerate(axs.flat):
    sample_idx = i   
    for cell_idx in range(wt_cp[sample_idx].shape[0]):
        ax.plot(wt_cp[sample_idx][cell_idx, :, 0], wt_cp[sample_idx][cell_idx, :, 1],
            linewidth=1, color='k')  
    ax.set_xlabel('X position (um)', fontsize=12)
    ax.set_xlabel('Y position (um)', fontsize=12)
    ax.set_xlim(-200, 200)  # Set specific x-axis limits
    ax.set_ylim(0, 400)  # Set specific y-axis limits
    ax.invert_yaxis()
    ax.set_title(samples[i])
plt.savefig('individual_samples_WT.pdf', bbox_inches='tight')
plt.show()

#Mut 
samples = ['mut1_01022024', 'mut2_12032024', 'mut3_21032024']
fig, axs = plt.subplots(1, 3, subplot_kw=dict(box_aspect=1), sharex=True, sharey=True, layout="constrained")
for i, ax in enumerate(axs.flat):
        sample_idx = i
        for cell_idx in range(mut_cp[sample_idx].shape[0]):
            ax.plot(mut_cp[sample_idx][cell_idx, :, 0], mut_cp[sample_idx][cell_idx, :, 1],
                linewidth=1, color='c')
        ax.set_xlabel('X position (um)', fontsize=12)
        ax.set_xlabel('Y position (um)', fontsize=12)
        ax.set_xlim(-200, 200)  # Set specific x-axis limits
        ax.set_ylim(0, 400)  # Set specific y-axis limits
        ax.invert_yaxis()
        ax.set_title(samples[i])
plt.savefig('individual_samples_mut.pdf', bbox_inches='tight')
plt.show()

# Combine all traces 
all_wt = np.concatenate((wt1_centered_positions, wt2_centered_positions, wt3_centered_positions), axis=0)
all_mut = np.concatenate((mut1_centered_positions, mut3_centered_positions, mut3_centered_positions), axis=0)

fig, axs = plt.subplots(1, 3, subplot_kw=dict(box_aspect=1), sharex=True, sharey=True, layout="constrained")

for cell_idx in range(all_wt.shape[0]):
    axs[0].plot(all_wt[cell_idx, :, 0], all_wt[cell_idx, :, 1],
                linewidth=1, color='k')
axs[0].set_xlabel('X position (um)', fontsize=12)
axs[0].set_xlabel('Y position (um)', fontsize=12)
axs[0].set_xlim(-200, 200)  # Set specific x-axis limits
axs[0].set_ylim(0, 400)  # Set specific y-axis limits
axs[0].invert_yaxis()
axs[0].set_title('wt combined')

for cell_idx in range(all_mut.shape[0]):
    axs[1].plot(all_mut[cell_idx, :, 0], all_mut[cell_idx, :, 1],
                linewidth=1, color='c')
axs[1].set_xlabel('X position (um)', fontsize=12)
axs[1].set_xlabel('Y position (um)', fontsize=12)
axs[1].set_xlim(-200, 200)  # Set specific x-axis limits
axs[1].set_ylim(0, 400)  # Set specific y-axis limits
axs[1].invert_yaxis()
axs[1].set_title('mut combined')

plt.savefig('combined_samples.pdf', bbox_inches='tight')
plt.show()

## Convergence ratio analysis 
all_wt_cr = [wt1_conv_ratio, wt2_conv_ratio, wt3_conv_ratio]
all_mut_cr = [mut1_conv_ratio, mut2_conv_ratio, mut3_conv_ratio]
mean_group1 = np.mean(all_wt_cr); mean_group2 = np.mean(all_mut_cr)
std_group1 = np.std(all_wt_cr); std_group2 = np.std(all_mut_cr)
t_stat, p_val = ttest_ind(all_wt_cr, all_mut_cr)

# Add jitter to scatter points
jitter = 0.05
group1_x_jittered = np.random.normal(1, jitter, size=len(all_wt_cr))
group2_x_jittered = np.random.normal(2, jitter, size=len(all_mut_cr))

## Speed analysis 
all_wt_ms = np.concatenate((wt1_mig_speed, wt2_mig_speed,wt3_mig_speed), axis=0)
all_mut_ms = np.concatenate((mut1_mig_speed, mut2_mig_speed,mut3_mig_speed), axis=0)
mean_group1_ms = np.mean(all_wt_ms); mean_group2_ms = np.mean(all_mut_ms)
std_group1_ms = np.std(all_wt_ms); std_group2_ms = np.std(all_mut_ms)
t_stat_ms, p_val_ms = ttest_ind(all_wt_ms, all_mut_ms)

# Add jitter to scatter points
group1_x_jittered_ms = np.random.normal(1, jitter, size=len(all_wt_ms))
group2_x_jittered_ms = np.random.normal(2, jitter, size=len(all_mut_ms))

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5), subplot_kw=dict(box_aspect=1))

# Plotting Convergence ratio analysis
axs[0].bar([1, 2], [mean_group1, mean_group2], yerr=[std_group1, std_group2], capsize=5, color=['grey', 'cyan'])
axs[0].scatter(group1_x_jittered, all_wt_cr, color='k', label='WT')
axs[0].scatter(group2_x_jittered, all_mut_cr, color='k', label='Mut')
axs[0].set_xticks([1, 2])
axs[0].set_xticklabels(['WT', 'Mut'], fontsize=12)
axs[0].set_title('Convergence ratio', fontsize=12)
axs[0].legend()
axs[0].text(1.5, max(mean_group1, mean_group2) + 0.5, f'p-value: {p_val:.4f}', ha='center', fontsize=12)

# Plotting Speed analysis
axs[1].bar([1, 2], [mean_group1_ms, mean_group2_ms], yerr=[std_group1_ms, std_group2_ms], capsize=5, color=['grey', 'cyan'])
axs[1].scatter(group1_x_jittered_ms, all_wt_ms, color='k', label='WT')
axs[1].scatter(group2_x_jittered_ms, all_mut_ms, color='k', label='Mut')
axs[1].set_xticks([1, 2])
axs[1].set_xticklabels(['WT', 'Mut'], fontsize=12)
axs[1].set_title('Migration speed', fontsize=12)
axs[1].legend()
axs[1].text(1.5, max(mean_group1_ms, mean_group2_ms) + 55, f'p-value: {p_val_ms:.4f}', ha='center', fontsize=12)

plt.tight_layout()
plt.savefig('convergence_ratio_migration_speed.pdf', bbox_inches='tight')
plt.show()

# Make an excel file with all convergences ratio and migration speed per genotype 
data = pd.DataFrame({'wt': all_wt_cr, 'mut': all_mut_cr})
file_path = 'convergence_ratio.xlsx'
data.to_excel(file_path, index=False)

# Determine the maximum length of the arrays
max_length = max(len(all_wt_ms), len(all_mut_ms))
# Create DataFrames for each dataset
wt_data = pd.DataFrame({'wt': all_wt_ms})
mut_data = pd.DataFrame({'mut': all_mut_ms})
# Add NaN values to align the lengths
if len(all_wt_ms) < max_length:
    wt_data = pd.concat([wt_data, pd.DataFrame({'wt': [np.nan] * (max_length - len(all_wt_ms))})], ignore_index=True)
if len(all_mut_ms) < max_length:
    mut_data = pd.concat([mut_data, pd.DataFrame({'mut': [np.nan] * (max_length - len(all_mut_ms))})], ignore_index=True)
# Concatenate the two DataFrames
combined_data = pd.concat([wt_data, mut_data], axis=1)

# Save to Excel
file_path = 'migration_speed.xlsx'
combined_data.to_excel(file_path, index=False)
