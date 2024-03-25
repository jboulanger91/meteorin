
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from extract_positions_convergence_speed import extract_positions_convergence_speed

# Videos have been downsampled to reduce size 
down = 2
# Pixel size
pix_size = 0.637

# Path to the Excel file
path_data = '/Users/jonathanboulanger-weill/Desktop/Projects/meteorin/dfc_tracking/dfc_tracking_data.xlsx'

# Load individual sheets 
wt1 = pd.read_excel(path_data, sheet_name=0) 
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(wt1, pix_size * down)
wt2 = pd.read_excel(path_data, sheet_name=1)
wt2_centered_positions, wt2_conv_ratio, wt2_mig_speed = extract_positions_convergence_speed(wt2, pix_size * down)
wt3 = pd.read_excel(path_data, sheet_name=2)
wt2_centered_positions, wt3_conv_ratio, wt3_mig_speed = extract_positions_convergence_speed(wt3, pix_size * down)

mut1 = pd.read_excel(path_data, sheet_name=3)
mut1_centered_positions, mut1_conv_ratio, mut1_mig_speed = extract_positions_convergence_speed(mut1, pix_size * down)
mut2 = pd.read_excel(path_data, sheet_name=4)
mut2_centered_positions, mut2_conv_ratio, mut2_mig_speed = extract_positions_convergence_speed(mut2, pix_size * down)
mut3 = pd.read_excel(path_data, sheet_name=5)
mut3_centered_positions, mut3_conv_ratio, mut3_mig_speed = extract_positions_convergence_speed(mut3, pix_size * down)

#Make figures 

# Show trajctories for each video 
fig, axs = plt.subplots(2, 3, subplot_kw=dict(box_aspect=1),
                         sharex=True, sharey=True, layout="constrained")

for i, ax in enumerate(axs.flat):
    ax.scatter(i % 3, -((i // 3) - 0.5)*200, c=[plt.cm.hsv(i / 6)], s=300)
plt.show()



plt.subplot(2, 5, 1)
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(wt1, 'WT 180124', pix_size * down, 'g')
plt.subplot(2, 5, 2)
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(wt2, 'WT 180124', pix_size * down, 'g')



