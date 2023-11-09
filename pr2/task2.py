import os
import numpy as np

matrix = np.load('./matrix_6_2.npy')
matrix = matrix.astype(float)

x = list()
y = list()
z = list()

filter_value = 505

for i in range(0, matrix.shape[0]):
    for j in range(0, matrix.shape[1]):
        if matrix[i][j] > filter_value:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez('./result/points.npz', x=x, y=y, z=z)
np.savez_compressed('./result/points_zip.npz', x=x, y=y, z=z)

print(f"points = {os.path.getsize('./result/points.npz')}")
print(f"points_zip = {os.path.getsize('./result/points_zip.npz')}")


