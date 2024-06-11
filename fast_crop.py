import open3d as o3d
from funcs import *
from data import colors, matrixes, angles

mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
num = 4

first = to_pcd_from_ply_file(f'ply/{num}.ply', colors[0])


A = mesh.get_rotation_matrix_from_xyz((np.pi / 180 * 45, 0, 0))
# B = mesh.get_rotation_matrix_from_xyz((0, 0, np.pi / 180 * 45)) 


obb = create_bounding_box(center=(-0.5, -1.06, -0.84))
obb.rotate(A)
first = first.crop(obb)
# o3d.io.write_point_cloud(f'up/{num}.ply', first)
o3d.visualization.draw_geometries([first, obb, mesh])