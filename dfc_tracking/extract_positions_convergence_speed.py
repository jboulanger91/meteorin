import numpy as np
import matplotlib.pyplot as plt

def extract_positions_convergence_speed(rec, pix_size):

    # Number of cells per recording
    num_cells = rec.shape[1] // 3  # Assuming each cell has x, y, and z columns

    # Loop over cells and extract positions for each time point
    positions_per_cell = []
    for cell_idx in range(num_cells):
        cell_positions = []
        for time_point in range(rec.shape[0]-1):
            x = rec.iloc[time_point+1, cell_idx * 3 + 1]*pix_size
            y = rec.iloc[time_point+1, cell_idx * 3 + 2]*pix_size
            z = rec.iloc[time_point+1, cell_idx * 3 + 3]*pix_size
            cell_positions.append((x, y, z))
        positions_per_cell.append(cell_positions)

    # Centering the data: 
    # Starting point should be 0 in y and mean(x) in x, to center plots
    # Calculate the mean x-coordinate of all cells at the first time point
    mean_x_init = np.mean([positions[0][0] for positions in positions_per_cell])
    min_y_init = np.min([positions[0][1] for positions in positions_per_cell])

    # Subtract the mean x-coordinate of all cells at the first time point from each x-coordinate for each cell at each time point
    centered_positions_per_cell = []
    for cell_positions in positions_per_cell:
        centered_cell_positions = [(x - mean_x_init, y-min_y_init, z) for x, y, z in cell_positions]
        centered_positions_per_cell.append(centered_cell_positions)

    # Compute convergence ratio
    width_init = np.max([positions[0][0] for positions in positions_per_cell])-np.min([positions[0][0] for positions in positions_per_cell])
    width_final = np.max([positions[12][0] for positions in positions_per_cell])-np.min([positions[12][0] for positions in positions_per_cell])
    conv_ratio = width_init / width_final
    conv_ratio

    # Compute migration speed, 12 time points equals to 3 hours recording
    mig_speed = np.zeros(num_cells)
    for idx_cell in range(num_cells):
        mig_speed[idx_cell] = (centered_positions_per_cell[idx_cell][12][1] - centered_positions_per_cell[idx_cell][0][1]) / 3

    # Convert into an np array 
    centered_positions = np.array(centered_positions_per_cell)

    return centered_positions, conv_ratio, mig_speed
