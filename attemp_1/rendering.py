
from asyncio import as_completed
import time

from concurrent import futures

from PIL import Image
from dataclasses import dataclass
from math import nan, sqrt, inf

from rmath import Vector3, Vector3Methods, clamp, randFloat
from world import World, WorldMethods
from camera import Camera, CameraMethods
from raycast import Ray, RayResult, RayMethods, RayResultMethods
from materials import MaterialReflectionData, MaterialMethods

COLOR_WHITE_V3 : Vector3 = Vector3(1.0, 1.0, 1.0)
COLOR_LIGHT_BLUE_V3 : Vector3 = Vector3(0.5, 0.7, 1.0)

def resolveColor( r : float, g : float, b : float, samples_per_pixel : int ) -> Vector3:
	if r == nan: r = 0
	if g == nan: g = 0
	if b == nan: b = 0
	scale : float = (1.0 / samples_per_pixel)
	r = sqrt(scale * r)
	g = sqrt(scale * g)
	b = sqrt(scale * b)
	return Vector3( clamp(r, 0, 0.999), clamp(g, 0, 0.999), clamp(b, 0, 0.999) )

def getRayColorVector( ray : Ray, world : World, depth : int ) -> Vector3:
	if (depth <= 0): return Vector3()

	result : RayResult = WorldMethods.FindClosestIntersection( world, ray, 0.001, inf )
	if (result != None):
		reflectData : MaterialReflectionData = MaterialMethods.scatter(result.material, ray, result)
		if (reflectData == None): return Vector3()
		return getRayColorVector(reflectData.scattered, world, depth-1).mult(reflectData.attenuation)
	unit_direction : Vector3 = Vector3Methods.unit( ray.direction )
	t : float = 0.5 * (unit_direction.y + 1.0)
	return Vector3Methods.addVec(
		Vector3Methods.multN( COLOR_LIGHT_BLUE_V3, 1.0-t),
		Vector3Methods.multN( COLOR_WHITE_V3, t )
	)

@dataclass
class RenderConfiguration:
	world : World = None
	camera : Camera = None
	samples_per_pixel : int = 25
	image_width : int = 500
	image_height : int = 480
	max_ray_depth : int = 2

class DefaultPipeline:

	def __init__( self, config : RenderConfiguration ):
		self.config = config
		self.image = None
		self.pixels = None

	def _render_pixel( self, x : int, y : int ) -> tuple[int, int, list]:
		rz : float = 0
		gz : float = 0
		bz : float = 0
		for _ in range( self.config.samples_per_pixel ):
			u : float = (x + randFloat()) / (self.config.image_width-1)
			v : float = (y + randFloat()) / (self.config.image_height-1)
			ray : Ray = CameraMethods.getRay( self.config.camera, u, v )
			rayColor : Vector3 = getRayColorVector(ray, self.config.world, self.config.max_ray_depth)
			rz += rayColor.x
			gz += rayColor.y
			bz += rayColor.z
		pixel_color : Vector3 = resolveColor(rz,gz,bz, self.config.samples_per_pixel)
		return [pixel_color.x, pixel_color.y, pixel_color.z] #y, [pixel_color.x, pixel_color.y, pixel_color.z]

	def render( self ) -> None:
		self.image = None
		self.pixels = []

		s_time = time.time()

		for x in range( self.config.image_width ):
			print(f"Computing Column: {x} / {self.config.image_width}")
			column = []
			for y in range( self.config.image_height ):
				pixel = self._render_pixel(x, y)
				column.append(pixel)
			self.pixels.append(column)

		# pool = futures.ThreadPoolExecutor(max_workers=16)
		# for x in range( self.config.image_width ):
		# 	print(f"Computing Column: {x} / {self.config.image_width}")
		# 	future_list = []
		# 	for y in range( self.config.image_height ):
		# 		future_list.append( pool.submit( DefaultPipeline._render_pixel, self=self, x=x, y=y ) )
		# 	pixel_dict = { }
		# 	for result in futures.as_completed( future_list ):
		# 		y, pixel = result.result()
		# 		pixel_dict[ y ] = pixel
		# 	column = []
		# 	for i in range( self.config.image_height ):
		# 		column.append( pixel_dict[i] )
		# 	self.pixels.append( column )

		print(f"Finished after { round(time.time()-s_time, 1) } seconds.")

	def get_pixels( self ) -> list | None:
		return self.pixels

# RendererData renderData = new RendererData( world, camera, samples_per_pixel, image_height, image_width, max_depth);
# Color[][] pixel_columns = Pipeline.DistributeRender(renderData, progressBar, bufferImg, image_label);
# for (int widthIndex = 0; widthIndex < image_width - 1; widthIndex++) {
# 	Color[] columnPixels = pixel_columns[widthIndex];
# 	for (int heightIndex = 0; heightIndex < image_height - 1; heightIndex++) {
# 		Color pixel_color = columnPixels[heightIndex];
# 		if (pixel_color == null) continue;
# 		bufferImg.setRGB(widthIndex, heightIndex, pixel_color.getRGB());
# 	}
# }
