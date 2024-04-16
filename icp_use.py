import open3d as o3d
from funcs import *


mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()

first = o3d.io.read_point_cloud('ply/unprocessed/1.ply')
first = magic(first)

first.translate((-1, 0, 0))
R = mesh.get_rotation_matrix_from_xyz((np.pi / 6,  # x 
                                       np.pi / 9,  # y red
                                       -np.pi / 2))  # z
first.rotate(R)

second = o3d.io.read_point_cloud('ply/unprocessed/2.ply')
second = magic(second)

second.translate((0, 1, 1))
R = mesh.get_rotation_matrix_from_xyz((np.pi / 2,  # x 
                                       -np.pi / 6,  # y 
                                       np.pi))  # z
second.rotate(R)

third = o3d.io.read_point_cloud('ply/unprocessed/3.ply')
third = magic(third)

fourth = o3d.io.read_point_cloud('ply/unprocessed/4.ply')
fourth = magic(fourth)

fourth.translate((1, 0.8, 1))

# mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
R = mesh.get_rotation_matrix_from_xyz((-np.pi / 1.7,  # x 
                                       -np.pi / 1.5,  # y red
                                       -np.pi / 4))  # z
fourth.rotate(R)


evaluate = connect_images(third, fourth)    # find transform matrix
third.transform(evaluate.transformation)
summmm = third + fourth

evaluate = connect_images(first, summmm)
first.transform(evaluate.transformation)
summmm += first

evaluate = connect_images(second, summmm)
second.transform(evaluate.transformation)
summmm += second
# summmm.paint_uniform_color([0, 0.8, 0.8])
# draw_registration_result(second, summmm, evaluate.transformation)
o3d.visualization.draw_geometries([summmm])

# draw_two(summmm, second)
