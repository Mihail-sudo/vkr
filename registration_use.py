import open3d as o3d
from funcs import *

voxel_size = 0.05
mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
R = mesh.get_rotation_matrix_from_xyz((np.pi / 6,  # x 
                                       np.pi / 9,  # y red
                                       -np.pi / 2))  # z

first = o3d.io.read_point_cloud('ply/unprocessed/3.ply')
first.rotate(R)

second = o3d.io.read_point_cloud('ply/unprocessed/4.ply')

first_down, first_fpfh = preprocess_pcd(first, voxel_size)
second_down, second_fpfh = preprocess_pcd(second, voxel_size)

# draw_two(first_down, second_down)

result_ransac = execute_global_registration(first_down, second_down, first_fpfh, second_fpfh, voxel_size)
# result_icp = refine_registration(first_down, second_down, result_ransac, voxel_size)

draw_registration_result(first_down, second_down, result_ransac.transformation)
# draw_registration_result(first_down, second_down, result_icp.transformation)
