import open3d as o3d
from funcs import *

# rotation xyz - 1 red, 2 green, 3 blue po chasovoi
# translate - r g b
# rotation without center rotate in center of figure overwise around coords
mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()

first = to_pcd_from_ply_file('ply/unprocessed/3.ply', [0.5, 0.9, 0.9])

second = to_pcd_from_ply_file('ply/unprocessed/4.ply', [0.9, 0.5, 0.9])

# o3d.visualization.draw_geometries([first, second])

# R = mesh.get_rotation_matrix_from_xyz((np.pi / 180 * 59,     # r
#                                        np.pi / 180 * 56,     # g
#                                        -np.pi / 180 * 105))   # b


R = mesh.get_rotation_matrix_from_xzy((-np.pi / 180 * 40,     # r 4
                                       np.pi / 180 * 54,     # g
                                       -np.pi / 180 * 88))   # b


second.rotate(R)
second.translate((0.7, 0.7, 0.7))


o3d.visualization.draw_geometries([first, second])

evaluate = connect_images(second, first)
draw_registration_result(second, first, evaluate.transformation)
