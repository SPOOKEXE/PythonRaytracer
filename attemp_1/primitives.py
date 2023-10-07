
from dataclasses import dataclass
from math import sqrt

from rmath import Vector3, Vector3Methods
from materials import BaseMaterial
from boundbox import BoundingBox, BoundBoxMethods
from raycast import Ray, RayResult, RayMethods, RayResultMethods

@dataclass
class BasePrimitive:
	position : Vector3 = Vector3Methods.ZERO
	bounds : BoundingBox = BoundingBox()
	material : BaseMaterial = BaseMaterial()

@dataclass
class Sphere(BasePrimitive):
	radius : float = 1

class PrimitiveMethods:

	@staticmethod
	def GenerateBoundingBox( self : BasePrimitive ) -> None:
		self.bounds = BoundingBox()

	@staticmethod
	def IsRayIntersectingBounds( self : BasePrimitive, ray : Ray ) -> bool:
		return BoundBoxMethods.IsRayIntersecting( self.bounds, ray )

	@staticmethod
	def FindRayIntersect( self : BasePrimitive, ray : Ray, t_min : float, t_max : float ) -> RayResult | None:
		return None

class SphereMethods(PrimitiveMethods):

	@staticmethod
	def GenerateBoundingBox( self : Sphere ) -> None:
		rVec = Vector3(self.radius, self.radius, self.radius)
		self.bounds = BoundingBox(
			Vector3Methods.subVec( self.position, rVec ),
			Vector3Methods.addVec( self.position, rVec )
		)

	@staticmethod
	def FindRayIntersect( self : Sphere, ray : Ray, t_min : float, t_max : float ) -> RayResult:
		oc : Vector3 = Vector3Methods.subVec( ray.origin, self.position )
		a : float = Vector3Methods.mag_sqred( ray.direction )
		half_b : float = Vector3Methods.dot(oc, ray.direction)
		c : float = Vector3Methods.mag_sqred(oc) - (self.radius*self.radius)

		discriminant : float = (half_b*half_b) - (a*c)
		if (discriminant < 0):
			return None

		sqrtd : float = sqrt(discriminant)

		# Find the nearest root that lies in the acceptable range.
		root : float = (-half_b - sqrtd) / a
		if (root < t_min or t_max < root):
			root = (-half_b + sqrtd) / a
			if (root < t_min or t_max < root):
				return None

		position : Vector3 = RayMethods.stepForward( ray, root )
		outward_normal : Vector3 = Vector3Methods.divN( Vector3Methods.subVec(position, self.position) , self.radius)

		result : RayResult = RayResult(position, None, root)
		RayResultMethods.setFaceNormal( result, ray, outward_normal )
		result.material = self.material
		return result
