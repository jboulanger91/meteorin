import numpy as np
import matplotlib.pyplot as plt

def extract_positions_convergence_speed(rec, title, pix_size, plot_color):
    # Number of cells per recording
    num_cells = rec.shape[1] // 3
    num_times = rec.shape[0]

    traj = {}
    cells_pos = np.zeros((num_cells, 2, num_times))

    # Extract individual cell 2d positions
    for idx_cell in range(num_cells):
        traj['cell_posx'] = rec[:, idx_cell * 3 - 2]
        traj['cell_posy'] = rec[:, idx_cell * 3 - 1]

        # Z position is not taken into account
        cells_pos[idx_cell, 0, :] = traj['cell_posx'] * pix_size
        cells_pos[idx_cell, 1, :] = traj['cell_posy'] * pix_size

    # Starting point should be 0 in y and mean(x) in x, to center plots
    temp_xval = np.zeros(num_cells)
    temp_yval = np.zeros(num_cells)
    for idx_cell in range(num_cells):
        temp_xval[idx_cell] = cells_pos[idx_cell, 0, 0]
        temp_yval[idx_cell] = cells_pos[idx_cell, 1, 0]
    start_xval = np.mean(temp_xval)
    start_yval = np.min(temp_yval)

    # Subtract to cell position
    cells_pos_corrected = np.zeros_like(cells_pos)
    for idx_cell in range(num_cells):
        cells_pos_corrected[idx_cell, 0, :] = cells_pos[idx_cell, 0, :] - np.mean(temp_xval)
        cells_pos_corrected[idx_cell, 1, :] = cells_pos[idx_cell, 1, :] - np.min(temp_yval)

    # Compute convergence ratio
    x_scattering_init = np.max(cells_pos_corrected[:, 0, 0]) - np.min(cells_pos_corrected[:, 0, 0])
    x_scattering_final = np.max(cells_pos_corrected[:, 0, 12]) - np.min(cells_pos_corrected[:, 0, 12])
    conv_ratio = x_scattering_init / x_scattering_final

    # Compute migration speed
    mig_speed = np.zeros(num_cells)
    for idx_cell in range(num_cells):
        mig_speed[idx_cell] = (cells_pos_corrected[idx_cell, 1, 12] - cells_pos_corrected[idx_cell, 1, 0]) / 3

    # Plot each trajectories
    for cell_idx in range(num_cells):
        plt.plot(cells_pos_corrected[cell_idx, 0, :], cells_pos_corrected[cell_idx, 1, :],
                 linewidth=1.5, color=plot_color)
    
    plt.legend([title], loc='upper center')
    plt.xlabel('X position (um)')
    plt.ylabel('Y position (um)')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.gca().spines['linewidth'] = 2
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    return cells_pos_corrected, conv_ratio, mig_speed
