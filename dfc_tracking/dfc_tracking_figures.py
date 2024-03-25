
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from extract_positions_convergence_speed import extract_positions_convergence_speed

# Videos have been downsampled to reduce size 
down = 2
# Pixel size
pix_size = 0.637

# Path to the Excel file
path_data = '/Users/jonathanboulanger-weill/Desktop/Projects/meteorin/dfc_tracking/dfc_tracking.xlsx'

# Load individual sheets
wt1 = pd.read_excel(path_data, sheet_name=0) 
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(pd.read_excel(path_data, sheet_name=0) , 'WT 180124', pix_size * down, 'g')

wt2 = pd.read_excel(path_data, sheet_name=1)

wt3 = pd.read_excel(path_data, sheet_name=2)
mut1 = pd.read_excel(path_data, sheet_name=3)
mut2 = pd.read_excel(path_data, sheet_name=4)
mut3 = pd.read_excel(path_data, sheet_name=5)


    # Plot each trajectories
    for cell_idx in range(num_cells):
        plt.plot(centered_positions[cell_idx, :, 0], centered_positions[cell_idx, :, 1],
                 linewidth=1.5, color=plot_color)
    
    plt.legend([title], loc='upper center')
    plt.xlabel('X position (um)',fontsize=14)
    plt.ylabel('Y position (um)',fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    ax.set_box_aspect(1)
    plt.axis([-200, 200, 0, 400])
    plt.gca().invert_yaxis()
    # Set aspect ratio to 'equal' for square plot window
    plt.figure(figsize=(12, 12))
    #plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


# Show trajctories for each video 
plt.subplot(2, 5, 1)
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(wt1, 'WT 180124', pix_size * down, 'g')
plt.subplot(2, 5, 2)
wt1_centered_positions, wt1_conv_ratio, wt1_mig_speed = extract_positions_convergence_speed(wt2, 'WT 180124', pix_size * down, 'g')



