from __future__ import annotations
from dataclasses import dataclass

import rmath
import materials

@dataclass
class RayResult:
	position : rmath.Vector3 = rmath.Vector3Methods.ZERO
	normal : rmath.Vector3 = rmath.Vector3Methods.ZERO
	material : materials.BaseMaterial = None
	t : float = 0
	front_face : bool = True

class RayResultMethods:

	@staticmethod
	def setFaceNormal( self : RayResult, ray : Ray, outward_normal : rmath.Vector3 ) -> None:
		self.front_face = rmath.Vector3Methods.dot( outward_normal, ray.direction ) < 0
		if self.front_face:
			self.normal = outward_normal
		else:
			self.normal = rmath.Vector3Methods.multN(outward_normal, -1)

@dataclass
class Ray:
	origin : rmath.Vector3 = rmath.Vector3()
	direction : rmath.Vector3 = rmath.Vector3Methods.XAXIS

class RayMethods:

	@staticmethod
	def stepForward( self : Ray, distance : float ) -> rmath.Vector3:
		return rmath.Vector3Methods.addVec( self.origin, rmath.Vector3Methods.multN(self.direction, distance) )
