import omni.replicator.core as rep
import random 
from assignment.replicator.randomization.custom_writer import WorkerWriter
from pxr import Gf
import omni.usd

def object_spawn(spawn_cubes_bool: bool, spawn_spheres_bool :bool, spawn_cylinders_bool: bool, cube_count: int, 
                sphere_count: int, cylinder_count: int, spawn_colors_bool: bool, position_min :float, position_max: float, 
                rotation_min: float,rotation_max,scale_min :float,scale_max:float, number_lights: int, minimum_intensity: float,
                maximum_intensity:float, temperature: float, type_light: str, has_material: bool, camera_number: int,
                scatter_mode : bool, writer_type: str, directory: str, frame_number: int,
                output_rgb: bool, output_bounding_box: bool):
    
    with rep.new_layer():
        if spawn_cubes_bool:
            spawn_cubes(cube_count)

        if spawn_spheres_bool:
            spawn_spheres(sphere_count)

        if spawn_cylinders_bool:
            spawn_cylinders(cylinder_count)
            print("cylinder", cylinder_count)

        add_randomization(position_min, position_max, rotation_min, rotation_max, scale_min, scale_max, spawn_colors_bool)
        add_light(number_lights, minimum_intensity, maximum_intensity, temperature, type_light)

        if has_material:
            add_material()
    
        renders =add_cameras(camera_number, scatter_mode)

        add_writer(writer_type, directory, frame_number,output_rgb, output_bounding_box, renders)
         

    rep.orchestrator.run()  



def spawn_cubes(count):
    for i in range(count):
        rep.create.cube(semantics=[('class', 'cube')])


def spawn_spheres(count):
    for i in range(count):
        rep.create.sphere(semantics=[('class', 'sphere')])


def spawn_cylinders(count):
    for i in range(count):
        rep.create.cylinder(semantics=[('class', 'cylinder')])


def add_randomization(position_min, position_max, rotation_min, rotation_max, scale_min, scale_max, spawn_colors_bool):

    shapes = rep.get.prims(semantics=[('class', 'cube'), ('class', 'sphere'), ('class', 'cylinder')])
    print(shapes)
    def randomize_position():
        with shapes:
            rep.modify.pose(
                position=rep.distribution.uniform(position_min, position_max),
                rotation=rep.distribution.uniform(rotation_min, rotation_max),
                scale=rep.distribution.uniform(scale_min, scale_max))
        return shapes.node

    def randomize_color():
        with shapes:
            rep.randomizer.color(colors=rep.distribution.uniform((0, 0, 0), (1, 1, 1)))
        return shapes.node

    rep.randomizer.register(randomize_position)
    with rep.trigger.on_frame(max_execs=10): 
        rep.randomizer.randomize_position()

    if spawn_colors_bool:
        rep.randomizer.register(randomize_color)
        with rep.trigger.on_frame(max_execs=10):
            rep.randomizer.randomize_color()

def add_light(number_lights, minimum_intensity, maximum_intensity, temperature, type_light):
    distance_light = rep.create.light(rotation=(315,0,0), intensity=3000, light_type="distant")

    def get_lights(number_lights):
        lights = rep.create.light(
            light_type=type_light,
            temperature= temperature,
            intensity=rep.distribution.normal(minimum_intensity, maximum_intensity),
            position=rep.distribution.uniform((-300, -300, -300), (300, 300, 300)),
            scale=rep.distribution.uniform(50, 100),
            count= number_lights
        )
        return lights.node

    rep.randomizer.register(get_lights)

    with rep.trigger.on_frame(num_frames=10):
        rep.randomizer.get_lights(number_lights)

def add_material():
    shapes = rep.get.prims(semantics=[('class', 'cube'), ('class', 'sphere'), ('class', 'cylinder')])
    mats = rep.create.material_omnipbr(diffuse = rep.distribution.uniform((0,0,0),(1,1,1)), count = 100)
    def get_shapes():
        with shapes:
            rep.randomizer.materials(mats)
        return shapes.node
    
    rep.randomizer.register(get_shapes)
    with rep.trigger.on_frame(num_frames =10):
        rep.randomizer.get_shapes()

def add_cameras(camera_number, scatter_mode):

    # random_plane = rep.create.plane(position=rep.distribution.uniform((-20,0,-20),(20,20,20)),scale=(2,2,0.1))
    
    cameras = []
    for i in range(camera_number):
        cam = rep.create.camera(
            focus_distance=rep.distribution.normal(50, 150),
            f_stop=1.8,
            focal_length=rep.distribution.uniform(2, 10),
            horizontal_aperture=10,
            look_at=(0, 0, 0))
        cameras.append(cam)

    with rep.trigger.on_frame(num_frames=10):
        for cam in cameras: #scattering code is commented out because it makes isaac crash 
            # if scatter_mode: #
            #     with cam:
            #         rep.randomizer.scatter_2d(random_plane, check_for_collisions=True)
            # else:
            with cam:
                    rep.modify.pose(
                        position=rep.distribution.uniform((-20, 10, -20), (20, 20, 30)))
                    
#look at object (attempt)
    # shapes = rep.get.prims(semantics=[('class', 'cube'), ('class', 'sphere'), ('class', 'cylinder')])
    # shape_to_look_at = random.choice(shapes)
    # shape_position = omni.usd.get_world_transform_matrix(shape_to_look_at).ExtractTranslation() 
    # print("SHAPE", shape_position)

    for cam in cameras:
    
        with rep.trigger.on_frame(num_frames=10):
            with cam:
                rep.modify.pose(look_at=(1,1,1))
                #rep.modify.pose(look_at=(shape_position))

    renders = [rep.create.render_product(cam, (1280, 720)) for cam in cameras]
    return renders
        
        
def add_writer(writer_type, directory, frame_number,output_rgb, output_bounding_box, renders):
    if writer_type =='KittiWriter':
        writer = rep.WriterRegistry.get(writer_type)
        writer.initialize(output_dir=directory,bbox_height_threshold=5,
        fully_visible_threshold=0.75, omit_semantic_type=True, num_frames = frame_number)
        writer.attach(renders)

    if writer_type == 'WorkerWriter':
        writer = WorkerWriter(output_dir=directory,
                              rgb=output_rgb,
                              bounding_box_2d_tight=output_bounding_box)
        writer.attach(renders)

#basic writer
    rep.WriterRegistry.register(WorkerWriter)
    writer = rep.WriterRegistry.get(writer_type)
    writer.initialize(output_dir= directory, rgb= output_rgb, bounding_box_2d_tight=output_bounding_box)
    writer.attach(renders)
    