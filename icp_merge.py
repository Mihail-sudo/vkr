import open3d as o3d
from funcs import *
from new_data import colors, matrixes, angles
# from data import colors, matrixes, angles
from numpy import pi

mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()

first = to_pcd_from_ply_file(f'cleaned_up/1.ply', colors[0])
second = to_pcd_from_ply_file(f'cleaned_up/4.ply', colors[1])

# first = to_pcd_from_ply_file(f'ply/1.ply', colors[0])
# second = to_pcd_from_ply_file(f'ply/4.ply', colors[1])

o3d.visualization.draw_geometries([first, second])

# A = mesh.get_rotation_matrix_from_xyz((pi / 180 * 72, pi / 180 * 64, -pi / 180 * 114)) # 2
# # A = mesh.get_rotation_matrix_from_xyz((-pi / 180 * 118, -pi / 180 * 132, -pi / 180 * 82)) # 3
A = mesh.get_rotation_matrix_from_xyz((-pi / 180 * 90, -pi / 180 * 182, 0)) # 4
second.rotate(A)

o3d.visualization.draw_geometries([first, second])


ev = execute_ICP(second, first)
second.transform(ev.transformation)

o3d.visualization.draw_geometries([first, second])
# print(ev.transformation)

# num = 3
# R = mesh.get_rotation_matrix_from_xyz(angles[num])
# second.rotate(R)
# second.transform(matrixes[num])
# o3d.visualization.draw_geometries([first, second, mesh])

