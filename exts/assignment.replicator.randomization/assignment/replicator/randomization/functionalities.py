import omni.replicator.core as rep
import random 

def object_spawn(spawn_cubes_bool: bool, spawn_spheres_bool :bool, spawn_cylinders_bool: bool, cube_count: int, sphere_count: int, cylinder_count: int, 
                spawn_colors_bool: bool, position_min :float, position_max: float, rotation_min: float,rotation_max,scale_min :float,scale_max:float,
                number_lights: int, minimum_intensity: float, maximum_intensity:float, temperature: float, type_light: str, has_material: bool,
                camera_number: int,scatter_mode : bool,plane: str):
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

        add_cameras(camera_number, scatter_mode, plane)
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
    with rep.trigger.on_frame(max_execs=30): #max_execs same as num_frames which will soon be deprecated so debugger said use this
        rep.randomizer.randomize_position()

    if spawn_colors_bool:
        rep.randomizer.register(randomize_color)
        with rep.trigger.on_frame(max_execs=30):
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
        rep.randomizer.get_lights(10)

def add_material():
    shapes = rep.get.prims(semantics=[('class', 'cube'), ('class', 'sphere'), ('class', 'cylinder')])
    mats = rep.create.material_omnipbr(diffuse = rep.distribution.uniform((0,0,0),(1,1,1)), count = 100)
    def get_shapes():
        with shapes:
            rep.randomizer.materials(mats)
        return shapes.node
    
    rep.randomizer.register(get_shapes)
    with rep.trigger.on_frame(num_frames =100):
        rep.randomizer.get_shapes()

def add_cameras(camera_number, scatter_mode, plane_name):
    cameras = []

    for i in range(camera_number):
        position = random.choice([
            rep.distribution.uniform((-500, 100, -500), (-300, 550, -300)),
            rep.distribution.uniform((300, 100, 300), (500, 550, 500)),
        ])
        camera = rep.create.camera(
            position=position,
            focus_distance=rep.distribution.normal(400.0, 100),
            f_stop=1.8,
            focal_length=rep.distribution.uniform(2, 10),
            horizontal_aperture=10
        )
        cameras.append(camera)

    # if scatter_mode:
    #     rep.randomizer.scatter_2d(objects=cameras, surface=plane_name,check_for_collisions=True)
    # renders = [rep.create.render_product(cam, (1920, 1080)) for cam in cameras]
    # return renders


        
