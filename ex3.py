import open3d as o3d
from funcs import *
from data import colors, matrixes, angles

mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()


result = to_pcd_from_ply_file('ply/un/1.ply', colors[0])
for i in range(1, 4):
    scene = to_pcd_from_ply_file(f'ply/un/{i + 1}.ply', colors[i])
    R = mesh.get_rotation_matrix_from_xyz(angles[i])
    scene.rotate(R)
    scene.transform(matrixes[i])
    result += scene


A = mesh.get_rotation_matrix_from_xyz((-np.pi / 180 * 45, 0, 0))
B = mesh.get_rotation_matrix_from_xyz((0, 0, np.pi / 180 * 45)) 

result.rotate(A)
result.rotate(B)

R = np.identity(3)
extent = np.array([1.5, 1.5, 2.5])
center = np.zeros(3)
obb = o3d.geometry.OrientedBoundingBox(center, R, extent)

obb.translate((0, 0.5, -0.45))

result = result.crop(obb)
o3d.visualization.draw_geometries([result, obb])


alpha = 0.5
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(result, alpha)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

v = o3d.geometry.TriangleMesh.get_volume(mesh)
print(f"Volume: {round(v, 4)} m^3")
