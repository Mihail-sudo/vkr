import open3d as o3d
from funcs import *
from data import *

result = to_pcd_from_ply_file('ply/un/1.ply', colors[0])
for i in range(1, 4):
    scene = to_pcd_from_ply_file(f'ply/un/{i + 1}.ply', colors[i])
    result += scene

o3d.visualization.draw_geometries([result])
