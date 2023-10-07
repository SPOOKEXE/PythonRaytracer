
import numpy as np
import json

from PIL import Image
from materials import LambertianMaterial, BaseMaterial, DielectricMaterial, MetalMaterial
from primitives import Sphere
from rmath import Vector3
from world import World, WorldMethods
from camera import Camera, CameraMethods
from rendering import DefaultPipeline, RenderConfiguration

def random_world( ) -> World:
	world = World()

	# BaseMaterial ground_material = new LambertianMaterial(new Vector3(0.5f, 0.5f, 0.5f));
	# world.add(new Sphere(new Vector3(0, -1000f, 0), 1000f, ground_material));

	# for (int a = -11; a < 11; a++) {
	# 	for (int b = -11; b < 11; b++) {
	# 		float choose_mat = Utility.random_float();
	# 		Vector3 center = new Vector3(a + 0.9f * Utility.random_float(), 0.2f, b + 0.9f * Utility.random_float());
	# 		if ((center.sub(new Vector3(4f, 0.2f, 0))).mag() > 0.9f) {
	# 			BaseMaterial sphere_material;
	# 			if (choose_mat < 0.8f) {
	# 				// diffuse
	# 				Vector3 albedo = Utility.randomColorVec();
	# 				sphere_material = new LambertianMaterial(albedo);
	# 				world.add(new Sphere(center, 0.2f, sphere_material));
	# 			} else if (choose_mat < 0.95f) {
	# 				// metal
	# 				Vector3 albedo = Utility.randomColorVec(0.5f, 1f);
	# 				float fuzz = Utility.random_float(0, 0.5f);
	# 				sphere_material = new MetalMaterial(albedo, fuzz);
	# 				world.add(new Sphere(center, 0.2f, sphere_material));
	# 			} else {
	# 				// glass
	# 				sphere_material = new DielectricMaterial(1.5f);
	# 				world.add(new Sphere(center, 0.2f, sphere_material));
	# 			}
	# 		}
	# 	}
	# }

	# BaseMaterial material1 = new DielectricMaterial(1.5f);
	# world.add(new Sphere(new Vector3(0, 1, 0), 1.0f, material1));

	# BaseMaterial material2 = new LambertianMaterial(new Vector3(0.4f, 0.2f, 0.1f));
	# world.add(new Sphere(new Vector3(-4, 1, 0), 1.0f, material2));

	# BaseMaterial material3 = new MetalMaterial(new Vector3(0.7f, 0.6, 0.5f), 0.0f);
	# world.add(new Sphere(new Vector3(4, 1, 0), 1.0f, material3));

	return world

def test_scene_world( ) -> World:
	world : World = World()
	material_ground : BaseMaterial = LambertianMaterial( Vector3(0.8, 0.8, 0.0) )
	material_center : BaseMaterial = LambertianMaterial( Vector3(0.1, 0.2, 0.5) )
	material_left : BaseMaterial = DielectricMaterial( 1.5 )
	material_right : BaseMaterial = MetalMaterial( Vector3(0.8, 0.6, 0.2), 0.0 )
	WorldMethods.extend(
		world,
		Sphere(Vector3( 0.0, -100.5, -1.0), 100.0, material_ground),
		Sphere(Vector3( 0.0, 0.0, -1.0), 0.5, material_center),
		Sphere(Vector3(-1.0, 0.0, -1.0), 0.5, material_left),
		Sphere(Vector3(-1.0, 0.0, -1.0), -0.45, material_left),
		Sphere(Vector3( 1.0, 0.0, -1.0), 0.5, material_right)
	)
	return world

def default_simulation( ) -> None:

	# output image settings
	aspect_ratio : float = 16.0 / 9.0
	image_width : int = 768
	image_height : int = int(image_width / aspect_ratio)
	max_depth : int = 2
	samples_per_pixel : int = 50

	# camera
	origin : Vector3 = Vector3(16, 2.2, 3.2)
	lookAt : Vector3 = Vector3(0, 0, 0)
	upVec : Vector3 = Vector3(0, 1, 0)
	dist_to_focus : float = 10.0
	aperture : float = 0.1

	camera = Camera()
	CameraMethods.setFromValues(camera, origin, lookAt, upVec, 20.0, aspect_ratio, aperture, dist_to_focus )

	# world
	world = test_scene_world()

	# config
	config = RenderConfiguration(world, camera, samples_per_pixel, image_width, image_height, max_depth)

	# pipeline
	pipeline = DefaultPipeline( config )

	# render
	pipeline.render()

	# output
	pixels = pipeline.get_pixels()
	with open("pixels.json", "w") as file:
		file.write( json.dumps(pixels) )

	image = Image.fromarray( np.array(pixels), mode="RGB" )
	image.save("output.png")

if __name__ == '__main__':
	default_simulation( )

	# with open("pixels.json", "r") as file:
	# 	data = json.loads( file.read() )

	# color255 = [ ]
	# for c in data:
	# 	col = []
	# 	for rgb in c:
	# 		col.append([ rgb[0] * 255, rgb[1] * 255, rgb[2] * 255 ])
	# 	color255.append(col)

	# color255 = np.array(color255)
	# image = Image.fromarray( np.array(color255), mode="RGB" )
	# image.save("output2.png")