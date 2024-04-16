import open3d as o3d
import numpy as np
import copy 


TRANS_INIT = np.eye(4)
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


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)

    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def draw_two(source, target):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0])
    o3d.visualization.draw_geometries([source_temp, target_temp, o3d.geometry.TriangleMesh.create_coordinate_frame()])


def connect_images(img1, img2):
    trans_init = copy.deepcopy(TRANS_INIT)
    
    treshold = 0.2

    evaluation = o3d.pipelines.registration.registration_icp(
        img1, img2, treshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=200))
    return evaluation


def preprocess_pcd(pcd):
    pcd_down = pcd.voxel_down_sample(VOXEL_SIZE)
    radius_normal = VOXEL_SIZE * 2
    pcd_down.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )

    pcd_down, _ = pcd_down.remove_statistical_outlier(nb_neighbors=60, std_ratio=0.7)

    radius_feature = VOXEL_SIZE * 5
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
