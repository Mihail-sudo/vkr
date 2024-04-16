import open3d as o3d
from funcs import *


mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()

first = to_pcd_from_ply_file('ply/unprocessed/1.ply', [0.5, 0.9, 0.9])

second =  to_pcd_from_ply_file('ply/unprocessed/2.ply', [0.9, 0.5, 0.9])

o3d.visualization.draw_geometries([first, second])

first_down, first_fpfh = preprocess_pcd(first)
second_down, second_fpfh = preprocess_pcd(second)

result_ransac = execute_global_registration(second_down, first_down, second_fpfh, first_fpfh)

second_down.transform(result_ransac.transformation)
o3d.visualization.draw_geometries([first_down, second_down])

