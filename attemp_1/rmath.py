
from __future__ import annotations

from random import ( randint, randrange )
from math import ( degrees, radians, inf, nan, sqrt )
from dataclasses import dataclass

def randFloat( dec=10^3 ) -> float:
	'''
	-1 to 1
	'''
	return randint(-1 * dec, 1 * dec) / dec

def randFloatRange( minn : float, maxx : float, step=1, dec=10^2 ) -> float:
	if minn == 0 and maxx == 0:
		return 0
	return randrange( minn * dec, maxx * dec, step ) / dec

def random_in_unit_sphere( ) -> Vector3:
	while True:
		p = Vector3Methods.randomRange(-1, 1)
		if ( Vector3Methods.mag_sqred(p) < 1 ):
			return p

def random_unit_vector() -> Vector3:
	return Vector3Methods.unit( random_in_unit_sphere() )

def random_in_hemisphere( normal : Vector3 ) -> Vector3:
	in_unit_sphere = random_in_unit_sphere()
	if Vector3Methods.dot(in_unit_sphere, normal) > 0.0:
		return in_unit_sphere
	return Vector3Methods.multN( in_unit_sphere, -1)

def random_in_unit_disk( ) -> Vector3:
	while True:
		p = Vector3(randFloatRange(-1, 1), randFloatRange(-1, 1), 0)
		if ( Vector3Methods.mag_sqred(p) < 1):
			return p

def clamp( x : float, minn : float, maxx : float ) -> float:
	return min( max(x, minn), maxx )

@dataclass
class Vector3:
	x : float = 0
	y : float = 0
	z : float = 0

class Vector3Methods:
	ZERO = Vector3(x=0,y=0,z=0)
	ONE = Vector3(x=1,y=1,z=1)
	NAN = Vector3(x=nan,y=nan,z=nan)

	XAXIS = Vector3(x=1,y=0,z=0)
	YAXIS = Vector3(x=0,y=1,z=0)
	ZAXIS = Vector3(x=0,y=0,z=1)

	POS_INF = Vector3(x=inf,y=inf,z=inf)
	NEG_INF = Vector3(x=-inf,y=-inf,z=-inf)

	@staticmethod
	def setXYZ( self : Vector3, x : float, y : float, z : float ) -> None:
		self.x = x
		self.y = y
		self.z = z

	@staticmethod
	def setVec3( self : Vector3, other : Vector3 ) -> None:
		self.x = other.x
		self.y = other.y
		self.z = other.z

	@staticmethod
	def addVec( self : Vector3, other : Vector3 ) -> Vector3:
		return Vector3( self.x + other.x, self.y + other.y, self.z + other.z )

	@staticmethod
	def addN( self : Vector3, v : float ) -> Vector3:
		return Vector3( self.x + v, self.y + v, self.z + v )

	@staticmethod
	def subVec( self : Vector3, other : Vector3 ) -> Vector3:
		return Vector3( self.x - other.x, self.y - other.y, self.z - other.z )

	@staticmethod
	def subN( self : Vector3, v : float ) -> Vector3:
		return Vector3( self.x - v, self.y - v, self.z - v )

	@staticmethod
	def divVec( self : Vector3, other : Vector3 ) -> Vector3:
		return Vector3( self.x / other.x, self.y / other.y, self.z / other.z )

	@staticmethod
	def divN( self : Vector3, v : float ) -> Vector3:
		return Vector3( self.x / v, self.y / v, self.z / v )

	@staticmethod
	def multVec( self : Vector3, other : Vector3 ) -> Vector3:
		return Vector3( self.x * other.x, self.y * other.y, self.z * other.z )

	@staticmethod
	def multN( self : Vector3, v : float ) -> Vector3:
		return Vector3( self.x * v, self.y * v, self.z * v )

	@staticmethod
	def dot( self : Vector3, other : Vector3 ) -> Vector3:
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

	@staticmethod
	def cross( self : Vector3, other : Vector3 ) -> Vector3:
		return Vector3(
			(self.y * other.z) - (other.y * self.z),
			(self.z * other.x) - (other.z * self.x),
			(self.x * other.y) - (other.x * self.y)
		)

	@staticmethod
	def mag( self : Vector3 ) -> float:
		return Vector3Methods.dot( self, self )

	@staticmethod
	def mag_sqred( self : Vector3 ) -> float:
		v = Vector3Methods.mag( self )
		return (v * v)

	@staticmethod
	def unit( self : Vector3 ) -> Vector3:
		norm = Vector3Methods.mag( self )
		if norm == 0:
			return Vector3Methods.ZERO
		return Vector3(self.x / norm, self.y / norm, self.z / norm)

	@staticmethod
	def lerp( self : Vector3, other : Vector3, t : float ) -> Vector3:
		return Vector3Methods.addVec( Vector3Methods.multN(self, 1-t), Vector3Methods.multN(other, t) )

	@staticmethod
	def is_near_zero( self : Vector3, s : float = 1e-8 ) -> bool:
		return (self.x < s) and (self.y < s) and (self.z < s)

	@staticmethod
	def reflect( self : Vector3, normal : Vector3 ) -> Vector3:
		return Vector3Methods.subVec( self, Vector3Methods.multN( normal, Vector3Methods.dot(self, normal) * 2 ) )

	@staticmethod
	def refract( uv : Vector3, n : Vector3, etai_over_etat : float ) -> Vector3:
		cos_theta = min( Vector3Methods.dot( Vector3Methods.multN(uv, -1), n), 1.0)
		r_out_perp = Vector3Methods.multN( Vector3Methods.addVec(uv, Vector3Methods.multVec(n, cos_theta)), etai_over_etat)
		parallel_n = -sqrt( abs( 1 - Vector3Methods.mag_sqred(r_out_perp) ) )
		r_out_parallel = Vector3Methods.multN(n, parallel_n)
		return Vector3Methods.addVec(r_out_perp, r_out_parallel)

	@staticmethod
	def toString( self : Vector3 ) -> str:
		return f"v3({self.x}, {self.y}, {self.z})"

	@staticmethod
	def randomRange( minn : float, maxx : float ) -> Vector3:
		return Vector3( randFloatRange(minn, maxx), randFloatRange(minn, maxx), randFloatRange(minn, maxx) )

	@staticmethod
	def random( ) -> Vector3:
		return Vector3( randFloat(), randFloat(), randFloat() )
