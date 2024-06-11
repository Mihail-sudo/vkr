# -*- coding: utf-8 -*-
import os
from funcs import merge_files, create_bounding_box
import numpy as np

import open3d as o3d
import open3d.visualization.gui as gui # type: ignore
import open3d.visualization.rendering as rendering # type: ignore


SIDE_BAR_WIDTH = 550


class App:
    def __init__(self) -> None:
        self.window = gui.Application.instance.create_window("params cheker", 1400, 900)

        self.text_fields = []
        self.num = None

        w = self.window
        self.em = w.theme.font_size
        em = w.theme.font_size

        gui_layout = gui.Vert(0, gui.Margins(0.5 * em, 0.5 * em, 0.5 * em, 0.5 * em))
        # create frame that encapsulates the gui
        gui_layout.frame = gui.Rect(w.content_rect.x, w.content_rect.y,
                                    SIDE_BAR_WIDTH, w.content_rect.height)
        

        file_buttons = [self.create_button(0), self.create_button(1), self.create_button(2), self.create_button(3)]
        for button in file_buttons:
            gui_layout.add_child(button)
            gui_layout.add_child(gui.Label(''))

        # labels and buttons 
        count_button = gui.Button("Count volume")
        count_button.vertical_padding_em = 0.5
        count_button.set_on_clicked(self.calculate_params)
        gui_layout.add_child(count_button)

        gui_layout.add_child(gui.Label(''))

        self.clear_button = gui.Button('Clear')
        self.clear_button.enabled = False
        self.clear_button.set_on_clicked(self.clear)
        gui_layout.add_child(self.clear_button)

        self.result_label = gui.Label('')
        gui_layout.add_child(self.result_label)


        # show the scene
        self.widget3d = gui.SceneWidget()
        self.widget3d.scene = rendering.Open3DScene(w.renderer)
        self.widget3d.set_view_controls(gui.SceneWidget.Controls.ROTATE_CAMERA)

        self.widget3d.scene.camera.look_at([0, 0, -1], [1, 1, 0], [0, 0, 1])
        # create a frame that encapsulates the Scenewidget
        self.widget3d.frame = gui.Rect(SIDE_BAR_WIDTH, w.content_rect.y,
                                         w.content_rect.width, w.content_rect.height)
        

        w.add_child(gui_layout)
        w.add_child(self.widget3d)


    def calculate_params(self):
        # get files
        files = self.get_all_files()
        if not files:
            self.result_label.text = '\nPlease choose correct files'
            return

        # create scene / transform every file with matrix from data
        scene = merge_files(files)

        mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        A = mesh.get_rotation_matrix_from_xyz((-np.pi / 180 * 45, 0, 0))
        B = mesh.get_rotation_matrix_from_xyz((0, 0, np.pi / 180 * 45)) 

        scene.rotate(A)
        scene.rotate(B)

        # crop full scene
        obb = create_bounding_box(center=(0, 0.5, -0.425))
        scene = scene.crop(obb)

        # get the minimal bounding box
        mb = scene.get_minimal_oriented_bounding_box()
        rotate = mb.R

        new_extent = mb.extent - np.array([0.02, 0.02, 0.02])
        mb = create_bounding_box(extent=new_extent, center=mb.center)
        mb.R = rotate
        mb.color = [0, 0, 0]
        length, width, height = mb.extent

        # make triangulation
        alpha = 0.5
        res_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(scene, alpha)
        # res_mesh.compute_vertex_normals()
        volume = o3d.geometry.TriangleMesh.get_volume(res_mesh)

        # show the result
        self.result_label.text = '\n' \
        f'Params of minimal bounding box:\n' \
        f'Length: {round(length, 3)} m \n' \
        f'Width: {round(width, 3)} m \n' \
        f'Height: {round(height, 3)} m \n' \
        f'Box volume: {round(length * width * height, 3)} m^3 \n \n' \
        f'Volume of object: {round(volume, 3)} m^3 \n'

        material = rendering.MaterialRecord()
        material.shader = "defaultLit"
        self.widget3d.scene.add_geometry('mesh', res_mesh, material)
        self.widget3d.scene.add_geometry('mb', mb, material)
        self.clear_button.enabled = True

        
    
    def get_all_files(self):
        files = []
        for text_field in self.text_fields:
            file_name = text_field.text_value
            if not os.path.exists(file_name):
                return False
            if not file_name.split('.') != 'ply':
                return False
            files.append(file_name)
        return files


    def create_button(self, num):
        file = gui.TextEdit()
        file.text_value = f'/Users/mikhail/vkr/ply/{num + 1}.ply' 
        self.text_fields.append(file)

        button = gui.Button("...")
        button.horizontal_padding_em = 0.5
        button.vertical_padding_em = 0
        button.set_on_clicked(lambda: self._on_filedlg_button(num))

        file_edit_layout = gui.Horiz()
        file_edit_layout.add_child(gui.Label(f"Camera {num + 1}"))
        file_edit_layout.add_child(file)
        file_edit_layout.add_fixed(0.25 * self.em)
        file_edit_layout.add_child(button)
        return file_edit_layout
        

    def _on_filedlg_button(self, num):
        filedlg = gui.FileDialog(gui.FileDialog.OPEN, "Select file",
                                self.window.theme)
        filedlg.add_filter(".obj .ply .stl", "Triangle mesh (.obj, .ply, .stl)")
        filedlg.add_filter("", "All files")
        filedlg.set_on_cancel(self._on_filedlg_cancel)

        filedlg.set_on_done(self._on_filedlg_done)
        self.num = num

        self.window.show_dialog(filedlg)


    def _on_filedlg_done(self, path):
        self.text_fields[self.num].text_value = path
        self.window.close_dialog()


    def _on_filedlg_cancel(self):
        self.window.close_dialog()


    def clear(self):
        # self.text_fields = ['', '', '', '']
        self.widget3d.scene.clear_geometry()
        self.result_label.text = ''
        self.clear_button.enabled = False


def main():
    gui.Application.instance.initialize()
    w = App()
    gui.Application.instance.run()


if __name__ == "__main__":
    main()