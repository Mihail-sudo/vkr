import open3d as o3d
from funcs import *
from new_data import colors, matrixes, angles

mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
# scene = to_pcd_from_ply_file(f'ply/{1}.ply', colors[0])
# tutu = to_pcd_from_ply_file(f'ply/{2}.ply', colors[1])

# o3d.visualization.draw_geometries([scene, mesh])

# R = mesh.get_rotation_matrix_from_xyz(angles[1])
# tutu.rotate(R)
# tutu.transform(matrixes[1])


# A = mesh.get_rotation_matrix_from_xyz((-np.pi / 180 * 45, np.pi / 180 * 45, np.pi / 180 * 45))
# B = mesh.get_rotation_matrix_from_axis_angle((-np.pi / 180 * 45, np.pi / 180 * 45, np.pi / 180 * 45))
# tutu = to_pcd_from_ply_file(f'ply/{1}.ply', colors[1])
# tata = to_pcd_from_ply_file(f'ply/{1}.ply', colors[2])
# tutu.rotate(A)
# tata.rotate(B)
# o3d.visualization.draw_geometries([scene, tutu, mesh])


scenes = []
for i in range(0, 4):
    scene = to_pcd_from_ply_file(f'new/{i + 1}.ply', colors[i])
    R = mesh.get_rotation_matrix_from_xyz(angles[i])
    scene.rotate(R)
    scene.transform(matrixes[i])
    scenes.append(scene)

result = scenes[0] + scenes[1] + scenes[2] + scenes[3]
o3d.visualization.draw_geometries([result])




# A = mesh.get_rotation_matrix_from_xyz((-np.pi / 180 * 45, 0, 0))
# B = mesh.get_rotation_matrix_from_xyz((0, 0, np.pi / 180 * 45)) 

# result.rotate(A)
# result.rotate(B)


# R = np.identity(3)
# extent = np.array([1.5, 1.5, 2.5])
# center = np.zeros(3) 
# obb = o3d.geometry.OrientedBoundingBox(center, R, extent)
# obb.translate((0, 0.5, -0.425))

# result = result.crop(obb)

# alpha = 0.5
# mb = result.get_minimal_oriented_bounding_box()
# mb.color = [1, 0, 1]

# res_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(result, alpha)
# res_mesh.compute_vertex_normals()
# v = o3d.geometry.TriangleMesh.get_volume(res_mesh)
# print(f"Объем: {round(v, 4)} m^3")
# print(f"Длинна: {round(mb.extent[0], 3)} m")
# print(f"Ширина: {round(mb.extent[1], 3)} m")
# print(f"Высота: {round(mb.extent[2], 3)} m")

# o3d.io.write_triangle_mesh('box.gltf', res_mesh)

# # o3d.visualization.draw_geometries([res_mesh, mb])
