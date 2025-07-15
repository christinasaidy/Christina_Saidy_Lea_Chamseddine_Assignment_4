import omni.ui as ui
from .functionalities import object_spawn

#Ui tutorial :"https://github.com/NVIDIA-Omniverse/kit-extension-sample-ui-window/blob/main/exts/omni.example.ui_window/tutorial/tutorial.md"

class SpawnControlsUI:
    def __init__(self):
        with ui.ScrollingFrame():
            with ui.VStack():
                #object spawning controls
                self.object_spawning_controls()

                #randomizing scale rotation position and color
                self.randomization_setting()

                #Light configuration
                self.light_configuration()

                #camera configuration
                self.camera_configuration()

                #writer configuration
                self.writer_configuration()

                #Spawn Button
                self.button_spawn()

    def object_spawning_controls(self):
         with ui.CollapsableFrame("Object Spawning Controls", opened=True):
                    with ui.VStack(spacing=4, padding=5):
                        with ui.HStack(height=12, spacing=6):
                            ui.Label("Cubes:", style={"font_size": 12, "min_width": 50})
                            self.cube_checkbox = ui.CheckBox()
                            ui.Label("Number Of Cubes:", style={"font_size": 12, "min_width": 90})
                            self.cube_count = ui.IntField(width=50, height=20)

                        with ui.HStack(height=22, spacing=6):
                            ui.Label("Spheres:", style={"font_size": 12, "min_width": 50})
                            self.sphere_checkbox = ui.CheckBox()
                            ui.Label("Number Of Spheres:", style={"font_size": 12, "min_width": 90})
                            self.sphere_count = ui.IntField(width=50, height=20)

                        with ui.HStack(height=22, spacing=6):
                            ui.Label("Cylinder:", style={"font_size": 12, "min_width": 50})
                            self.cylinder_checkbox = ui.CheckBox()
                            ui.Label("Number Of Cylinders:", style={"font_size": 12, "min_width": 90})
                            self.cylinder_count = ui.IntField(width=50, height=20)

    def randomization_setting(self):
        with ui.CollapsableFrame("Randomization Settings", opened=True):
             with ui.VStack( padding=5):

                with ui.HStack(spacing =6,height =28):
                    ui.Label("Coordinates", style={"font_size": 12, "min_width": 30})  # empty label to align with input row label ("Position Min", etc.)
                    ui.Label("X", width = 45,  style={"font_size": 12})
                    ui.Label("Y", width = 45, style={"font_size": 12})
                    ui.Label("Z", width = 45,style={"font_size": 12})

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Position Min", style={"font_size": 12, "min_width": 50})
                    self.pos_min_x = ui.FloatField(width=50, height=20)
                    self.pos_min_y = ui.FloatField(width=50, height=20)
                    self.pos_min_z = ui.FloatField(width=50, height=20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Position Max", style={"font_size": 12, "min_width": 90})
                    self.pos_max_x = ui.FloatField(width=50, height=20)
                    self.pos_max_y = ui.FloatField(width=50, height=20)
                    self.pos_max_z = ui.FloatField(width=50, height=20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Rotation Min", style={"font_size": 12, "min_width": 90})
                    self.rot_min_x = ui.FloatField(width=50, height=20)
                    self.rot_min_y = ui.FloatField(width=50, height=20)
                    self.rot_min_z = ui.FloatField(width=50, height=20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Rotation Max", style={"font_size": 12, "min_width": 90})
                    self.rot_max_x = ui.FloatField(width=50, height=20)
                    self.rot_max_y = ui.FloatField(width=50, height=20)
                    self.rot_max_z = ui.FloatField(width=50, height=20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Scale Min", style={"font_size": 12, "min_width": 90})
                    self.scal_min_x = ui.FloatField(width=50, height=20)
                    self.scal_min_y = ui.FloatField(width=50, height=20)
                    self.scal_min_z = ui.FloatField(width=50, height=20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Scale Max", style={"font_size": 12, "min_width": 90})
                    self.scal_max_x = ui.FloatField(width=50, height=20)
                    self.scal_max_y = ui.FloatField(width=50, height=20)
                    self.scal_max_z = ui.FloatField(width=50, height=20)

                with ui.HStack(height=28, spacing=6):
                    ui.Label("Random Color Association:", style={"font_size": 12})
                    self.color_checkbox = ui.CheckBox()

                with ui.HStack(height =28, spacing=6):
                    ui.Label("Add Random Material: ", style ={"font_size": 12})
                    self.material_checkbox = ui.CheckBox()

    def light_configuration(self):
        with ui.CollapsableFrame("Lighting Configuration", opened=True):
            with ui.VStack(padding=5):
                with ui.HStack(spacing=6, height=28):
                    ui.Label("Number Of Lights", style={"font_size": 12, "min_width": 30})
                    self.light_num = ui.IntField(height=20, width=80)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Intensity Min", style={"font_size": 12, "min_width": 30})
                    self.intensity_min = ui.FloatField(height=20, width=80)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Intensity Max", style={"font_size": 12, "min_width": 30})
                    self.intensity_max = ui.FloatField(height=20, width=80)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Temperature", style={"font_size": 12, "min_width": 30})
                    self.temp = ui.FloatField(height=20, width=80)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Light Type", style={"font_size": 12, "min_width": 30})
                    self.light_options =["distant", "Sphere", "Dome"]
                    self.combo_lights = ui.ComboBox(0, *self.light_options, width =100)
                    #reference for combobox : "https://github.com/mati-nvidia/developer-office-hours/blob/main/exts/maticodes.doh_2022_09_23/scripts/combobox_selected_item.py"

    def camera_configuration(self): 
        with ui.CollapsableFrame("Camera Configuration", opened = True):
            with ui.VStack(spacing=4, padding=5):
                    with ui.HStack(spacing =6, height =28):
                        ui.Label("Number of Cameras:", style={"font_size": 12, "min_width": 50})
                        self.cam_numb= ui.IntField(width=50, height=20)
                    with ui.HStack(spacing =6, height = 28):
                        ui.Label("Scatter on Plane:", style={"font_size": 12, "min_width": 90})
                        self.scatter_checkbox = ui.CheckBox()
                        # ui.Label("Plane To Scatter On:", style={"font_size": 12, "min_width": 90})
                        # self.plane_scatter = ui.StringField(height =20)

    def writer_configuration(self):
        with ui.CollapsableFrame("Writer and Output Controls", opened=True):
            with ui.VStack(spacing=4, padding=5):
                with ui.HStack(spacing=6, height=28):
                    ui.Label("Writer Type:", style={"font_size": 12, "min_width": 90})
                    self.writer_options = ["BasicWriter", "KittiWriter", "WorkerWriter"]
                    self.combobox_writers = ui.ComboBox(0, *self.writer_options, width=100)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Output Directory:", style={"font_size": 12, "min_width": 90})
                    self.output_dir = ui.StringField(width=200, height= 20)

                with ui.HStack(spacing=6, height=28):
                    ui.Label("Number of Frames:", style={"font_size": 12, "min_width": 90})
                    self.num_frames = ui.IntField(width=50, height = 20)

                ui.Label("Output Types:", style={"font_size": 12})
                with ui.HStack(spacing=6, padding=6, height =22):
                    ui.Label("RGB", style={"font_size": 12, "min_width": 90})
                    self.rgb_checkbox = ui.CheckBox()
                    ui.Label("2D Bounding Box", style={"font_size": 12, "min_width": 90})
                    self.boundbox_checkbox = ui.CheckBox()
                    # ui.Label("Point Cloud", style={"font_size": 12, "min_width": 90})
                    # self.pointcloud_checkbox = ui.CheckBox()

    def button_spawn(self):
        with ui.HStack(height=30, padding=10):
            self.button = ui.Button("Spawn", clicked_fn=self.build_scene)

    def build_scene(self):
        object_settings = self.get_object_settings()
        transform_settings = self.get_transform_settings()
        lighting_settings = self.get_lighting_settings()
        camera_settings = self.get_camera_settings()
        writer_settings = self.get_writer_settings()

        object_spawn(object_settings["spawn_cubes"], object_settings["spawn_spheres"], object_settings["spawn_cylinders"],
            object_settings["cube_count"], object_settings["sphere_count"], object_settings["cylinder_count"],
            object_settings["spawn_colors"], 
            transform_settings["position_min"], transform_settings["position_max"],
            transform_settings["rotation_min"], transform_settings["rotation_max"],
            transform_settings["scale_min"], transform_settings["scale_max"],
            lighting_settings["number_lights"], lighting_settings["min_intensity"],
            lighting_settings["max_intensity"], lighting_settings["temperature"],
            lighting_settings["light_type"],
            object_settings["has_material"],
            camera_settings["camera_number"], camera_settings["scatter_mode"],
            # camera_settings["scatter_plane"],
            writer_settings["writer_type"], writer_settings["output_directory"], writer_settings["frame_number"],
            writer_settings["output_rgb"], writer_settings["output_bounding_box"])
        
    def get_object_settings(self):
        return {
            "spawn_cubes": self.cube_checkbox.model.get_value_as_bool(),
            "cube_count": self.cube_count.model.get_value_as_int(),
            "spawn_spheres": self.sphere_checkbox.model.get_value_as_bool(),
            "sphere_count": self.sphere_count.model.get_value_as_int(),
            "spawn_cylinders": self.cylinder_checkbox.model.get_value_as_bool(),
            "cylinder_count": self.cylinder_count.model.get_value_as_int(),
            "spawn_colors": self.color_checkbox.model.get_value_as_bool(),
            "has_material": self.material_checkbox.model.get_value_as_bool()
        }

    def get_transform_settings(self):
        return {
            "position_min": (self.pos_min_x.model.get_value_as_float(),
                self.pos_min_y.model.get_value_as_float(),
                self.pos_min_z.model.get_value_as_float()),
            "position_max": (self.pos_max_x.model.get_value_as_float(),
                self.pos_max_y.model.get_value_as_float(),
                self.pos_max_z.model.get_value_as_float()),

            "rotation_min": (self.rot_min_x.model.get_value_as_float(),
                self.rot_min_y.model.get_value_as_float(),
                self.rot_min_z.model.get_value_as_float()),

            "rotation_max": (self.rot_max_x.model.get_value_as_float(),
                self.rot_max_y.model.get_value_as_float(),
                self.rot_max_z.model.get_value_as_float()),

            "scale_min": (self.scal_min_x.model.get_value_as_float(),
                self.scal_min_y.model.get_value_as_float(),
                self.scal_min_z.model.get_value_as_float()),
                
            "scale_max": (self.scal_max_x.model.get_value_as_float(),
                self.scal_max_y.model.get_value_as_float(),
                self.scal_max_z.model.get_value_as_float())}

    def get_lighting_settings(self):
        selected_index = self.combo_lights.model.get_item_value_model().as_int
        light_type = self.light_options[selected_index]
        return {
            "number_lights": self.light_num.model.get_value_as_int(),
            "min_intensity": self.intensity_min.model.get_value_as_float(),
            "max_intensity": self.intensity_max.model.get_value_as_float(),
            "temperature": self.temp.model.get_value_as_float(),
            "light_type": light_type}

    def get_camera_settings(self):
        return {
            "camera_number": self.cam_numb.model.get_value_as_int(),
            "scatter_mode": self.scatter_checkbox.model.get_value_as_bool()}
            # "scatter_plane": self.plane_scatter.model.get_value_as_string()}
    
    def get_writer_settings(self):
        selected_index = self.combobox_writers.model.get_item_value_model().as_int
        writer_type = self.writer_options[selected_index]
        return{
            "writer_type": writer_type,
            "output_directory": self.output_dir.model.get_value_as_string(),
            "frame_number": self.num_frames.model.get_value_as_int(),
            "output_rgb": self.rgb_checkbox.model.get_value_as_bool(),
            "output_bounding_box": self.boundbox_checkbox.model.get_value_as_bool()}

