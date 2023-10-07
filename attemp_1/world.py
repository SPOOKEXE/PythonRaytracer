
from raycast import Ray, RayResult
from primitives import BasePrimitive, PrimitiveMethods

class World:
	primitives : list = [ ]

class WorldMethods:

	@staticmethod
	def clear( self : World ) -> None:
		self.primitives = []

	@staticmethod
	def extend( self : World, *args ) -> None:
		self.primitives.extend( [*args] )

	@staticmethod
	def append( self : World, item : BasePrimitive ) -> None:
		self.primitives.append( item )

	@staticmethod
	def FindClosestIntersection( self : World, ray : Ray, t_min : float, t_max : float ) -> RayResult | None:
		closest : RayResult = None
		closest_max : float = t_max
		for obj in self.primitives:
			# if not PrimitiveMethods.IsRayIntersectingBounds( obj, ray ):
			# 	continue
			result : RayResult = PrimitiveMethods.FindRayIntersect( obj, ray, t_min, closest_max )
			if (result != None):
				closest_max = result.t
				closest = result
		return closest
