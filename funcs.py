import open3d as o3d
import numpy as np
import copy 
from new_data import *


VOXEL_SIZE = 0.01


def to_pcd_from_ply_file(ply_path, color=[0.5, 0.5, 0.5]):
    ply = o3d.io.read_point_cloud(ply_path)
    pcd = ply.voxel_down_sample(VOXEL_SIZE)
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=60, std_ratio=0.7)
    pcd.paint_uniform_color(color)
    return pcd


def merge_files(files):
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    scenes = []

    for idx, file in enumerate(files):
        scene = to_pcd_from_ply_file(file, colors[idx])
        R = mesh.get_rotation_matrix_from_xyz(angles[idx])
        scene.rotate(R)
        scene.transform(matrixes[idx])
        scenes.append(scene)

    result = scenes[0] + scenes[1] + scenes[2] + scenes[3]
    return result


def create_bounding_box(extent=[1.5, 1.5, 2.5], center=(0, 0, 0)):
    R = np.identity(3)
    extent = np.array(extent)
    obb = o3d.geometry.OrientedBoundingBox(center, R, extent)
    # obb.translate((0, 0.5, -0.425))
    return obb


#######################################

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)

    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def execute_ICP(img1, img2):
    trans_init = np.eye(4)
    treshold = 0.1
    evaluation = o3d.pipelines.registration.registration_icp(
        img1, img2, treshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=500))
    return evaluation


def preprocess_pcd(pcd):
    radius_feature = VOXEL_SIZE * 5
    radius_normal = VOXEL_SIZE * 2

    pcd_down = pcd.voxel_down_sample(VOXEL_SIZE)
    pcd_down.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )

    pcd_down, _ = pcd_down.remove_statistical_outlier(nb_neighbors=60, std_ratio=0.7)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100)
    )
    return pcd_down, pcd_fpfh


def execute_global_registration(source_down, target_down, source_fpfh, 
                                target_fpfh):
    distance_treshold = VOXEL_SIZE * 1.5
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True, distance_treshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_treshold),
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999)
    )
    return result


def refine_registration(source, target, result_ransac):
    distance_threshold = VOXEL_SIZE * 0.4
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=300))
    return result
