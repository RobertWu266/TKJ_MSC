import pandas as pd
import numpy as np

# Initialize the matrix sizes
n_submatrices = 5
submatrix_size = 4692
last_row_col_size = 4696
giant_matrix_size = (n_submatrices - 1) * submatrix_size + last_row_col_size

# Initialize the giant matrix
giant_matrix = np.zeros((giant_matrix_size, giant_matrix_size))


# Function to read a submatrix, with special handling for the last row and column
def read_submatrix(a, b):
    if a == 4 and b == 4:
        filename = f"full_data_{a}_{b},4696_4696.csv"
    elif b == 4:
        filename = f"full_data_{a}_{b},4692_4696.csv"
    else:
        filename = f"full_data_{a}_{b},4692_4692.csv"

    return pd.read_csv(filename, header=None).values


# Function to calculate the start index for a given submatrix position
def calculate_start_index(position):
    if position < 4:
        return position * submatrix_size
    else:
        return 4 * submatrix_size


# Assemble the giant matrix
for a in range(n_submatrices):
    for b in range(n_submatrices):
        if a <= b:
            submatrix = read_submatrix(a, b)
        else:
            # Use the transpose of the corresponding submatrix
            submatrix = read_submatrix(b, a).T

        # Calculate the start row and column
        start_row = calculate_start_index(a)
        start_col = calculate_start_index(b)

        # Determine the size of the submatrix
        submatrix_rows, submatrix_cols = submatrix.shape

        # Place the submatrix in the correct position
        giant_matrix[start_row:start_row + submatrix_rows, start_col:start_col + submatrix_cols] = submatrix

# giant_matrix now represents the assembled giant symmetric matrix
out_name = './All_Labeled_Images.csv'
(pd.DataFrame(giant_matrix)).to_csv(out_name, index=False, header=False)