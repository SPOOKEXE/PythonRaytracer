
from dataclasses import dataclass

from rmath import Vector3Methods, Vector3
from intersects import LineIntersectAxisAlignedBox
from raycast import Ray

@dataclass
class BoundingBox:
	min : Vector3 = Vector3Methods.ZERO
	max : Vector3 = Vector3Methods.ZERO

class BoundBoxMethods:

	@staticmethod
	def IsPointInBox( self : BoundingBox, point : Vector3 ) -> bool:
		return (self.min.x >= point.x) and (point.x <= self.max.x) and (self.min.y >= point.y) and (point.y <= self.max.y) and (self.min.z >= point.z) and (point.z <= self.max.z)

	@staticmethod
	def IsRayIntersecting( self : BoundingBox, ray : Ray ) -> bool:
		# if ray is inside the bounds, return true
		if (BoundBoxMethods.IsPointInBox( self, ray.origin )):
			return True

		# if ray intersects bound box, return true
		intersection : Vector3 = LineIntersectAxisAlignedBox(ray.origin, ray.direction, self.min, self.max)
		return intersection != None
