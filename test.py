import numpy as np
import matplotlib.pyplot as plt

def extract_positions(rec, title, pix_size, flip_traj, drift_dir):
    # Number of cells per recording
    num_cells = int(rec.shape[1] / 3) - 1
    num_times = rec.shape[0]

    # Initialize arrays to store cell positions
    traj = {'cell_posx': np.zeros((num_cells, num_times)),
            'cell_posy': np.zeros((num_cells, num_times))}

    # Now compute each normalized position
    for idx_cell in range(num_cells - 1):
        for idx_time in range(num_times):
            # Extract vegetal pole position for drift canceling
            if drift_dir == 'x':
                ref_drift = rec[idx_time, num_cells * 3]
            elif drift_dir == 'y':
                ref_drift = rec[idx_time, num_cells * 3 + 1]
            else:
                ref_drift = 0

            # Extract individual cell, times positions
            traj['cell_posx'][idx_cell, idx_time] = rec[idx_time, idx_cell * 3] - ref_drift
            traj['cell_posy'][idx_cell, idx_time] = rec[idx_time, idx_cell * 3 + 1] - ref_drift

    # Z position is not taken into account
    cells_pos = np.zeros((num_cells - 1, 2, num_times))

    for idx_cell in range(num_cells - 1):
        cells_pos[idx_cell, 0, :] = traj['cell_posx'][idx_cell, :] * pix_size
        cells_pos[idx_cell, 1, :] = traj['cell_posy'][idx_cell, :] * pix_size

        if flip_traj == 1:
            cells_pos[idx_cell, [0, 1], :] = cells_pos[idx_cell, [1, 0], :]

    # Starting point should by 0 in y and mean(x) in x, to center
    temp_xval = np.zeros(num_cells - 1)
    temp_yval = np.zeros(num_cells - 1)

    for idx_cell in range(num_cells - 1):
        temp_xval[idx_cell] = cells_pos[idx_cell, 0, 0]
        temp_yval[idx_cell] = cells_pos[idx_cell, 1, 0]

    start_xval = np.mean(temp_xval)
    start_yval = np.min(temp_yval)

    cells_pos_corrected = cells_pos.copy()

    # Subtract from cell position
    for idx_cell in range(num_cells - 1):
        cells_pos_corrected[idx_cell, 0, :] -= np.mean(temp_xval)
        cells_pos_corrected[idx_cell, 1, :] -= np.min(temp_yval)

    # Plot each trajectory
    for cell_idx in range(num_cells - 1):
        plt.plot(cells_pos_corrected[cell_idx, 0, :], cells_pos_corrected[cell_idx, 1, :], linewidth=2)
        plt.xlabel('Distance (um)')
        plt.ylabel('Distance (um)')
        plt.legend([title], loc='upper left')

    plt.legend([title], loc='upper left')
    plt.xlabel('Distance (um)')
    plt.ylabel('Distance (um)')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.axis('tight')
    plt.show()

# Example usage
# Assuming rec is your data, title is the title of the plot,
# pix_size is the pixel size, flip_traj is the flag for flipping the trajectory,
# and drift_dir is the drift direction.
# You need to provide these variables before calling the function.

# extract_positions(rec, title, pix_size, flip_traj, drift_dir)
