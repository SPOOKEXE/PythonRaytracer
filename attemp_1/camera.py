
from __future__ import annotations

from dataclasses import dataclass
from math import radians, tan

from rmath import Vector3, Vector3Methods, random_in_unit_disk
from raycast import Ray

@dataclass
class Camera:
	origin : Vector3 = Vector3Methods.ZERO
	horizontal : Vector3 = Vector3Methods.ZERO
	vertical : Vector3 = Vector3Methods.ZERO
	lower_left_corner : Vector3 = Vector3Methods.ZERO

	u : Vector3 = Vector3Methods.ZERO
	v : Vector3 = Vector3Methods.ZERO
	w : Vector3 = Vector3Methods.ZERO
	lens_radius : float = 1

class CameraMethods:

	@staticmethod
	def setFromValues( self : Camera, origin : Vector3, lookAt : Vector3, up : Vector3, vfov : float, aspect_ratio : float, aperture : float, focus_distance : float ) -> None:
		theta : float = radians(vfov)
		h : float = tan(theta / 2)
		viewport_height : float = (2 * h)
		viewport_width : float = (aspect_ratio * viewport_height)

		self.w = Vector3Methods.unit( Vector3Methods.subVec( origin, lookAt ) )
		self.u = Vector3Methods.unit( Vector3Methods.cross(up, self.w) )
		self.v = Vector3Methods.cross( self.w, self.u )

		self.origin = origin
		self.horizontal = Vector3Methods.multN( self.u, focus_distance * viewport_width )
		self.vertical = Vector3Methods.multN( self.v, focus_distance * viewport_height)
		self.lower_left_corner = Vector3Methods.subVec(
			Vector3Methods.subVec(
				origin,
				Vector3Methods.multN(self.horizontal, 0.5 )
			),
			Vector3Methods.subVec(
				Vector3Methods.multN( self.vertical, 0.5 ),
				Vector3Methods.multN( self.w, focus_distance )
			)
		)

		self.lens_radius = (aperture / 2)

	@staticmethod
	def getRay( self : Camera, s : float, t : float ) -> Ray:
		rd : Vector3 = Vector3Methods.multN( random_in_unit_disk(), self.lens_radius )
		offset : Vector3 = Vector3Methods.addVec(
			Vector3Methods.multN( self.u, rd.x ),
			Vector3Methods.multN( self.v, rd.y)
		)

		b = Vector3Methods.addVec( self.lower_left_corner, Vector3Methods.multN( self.horizontal, s ) )
		c = Vector3Methods.addVec( b, Vector3Methods.multN( self.vertical, t ) )
		return Ray(
			Vector3Methods.addVec( self.origin, offset),
			Vector3Methods.subVec( Vector3Methods.subVec( c, self.origin ), offset )
		)
