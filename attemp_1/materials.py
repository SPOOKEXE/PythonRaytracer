from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import sqrt

import raycast
import rmath

class EnumMaterial(Enum):
	Default = 0
	Dieletric = 1
	Lambertian = 2
	Metal = 3

@dataclass
class MaterialReflectionData:
	scatter_direction : rmath.Vector3 = None
	scattered : raycast.Ray = None
	attenuation : rmath.Vector3 = None

@dataclass
class BaseMaterial:
	enum : EnumMaterial = EnumMaterial.Default
	albedo : rmath.Vector3 = rmath.Vector3Methods.ZERO

@dataclass
class LambertianMaterial:
	enum : EnumMaterial = EnumMaterial.Lambertian

@dataclass
class DielectricMaterial:
	enum : EnumMaterial = EnumMaterial.Dieletric
	indexOfRefraction : float = 1

@dataclass
class MetalMaterial:
	enum : EnumMaterial = EnumMaterial.Metal
	albedo : rmath.Vector3 = rmath.Vector3Methods.ZERO
	fuzz : float = 0

class MaterialMethods:

	@staticmethod
	def reflectance( self : BaseMaterial, cosine : float, ref_idx : float ) -> float:
		if self.enum == EnumMaterial.Dieletric:
			r0 : float = (1-ref_idx) / (1+ref_idx)
			r0 = r0*r0
			return (r0 + (1-r0) * pow((1 - cosine), 5))
		return 1

	@staticmethod
	def scatter( self : BaseMaterial, r_in : raycast.Ray, hit : raycast.RayResult ) -> MaterialReflectionData | None:

		material_dat : MaterialReflectionData = MaterialReflectionData()

		if self.enum == EnumMaterial.Default:

			material_dat.scatter_direction = r_in.direction
			material_dat.scattered = r_in
			material_dat.attenuation = self.albedo

		elif self.enum == EnumMaterial.Lambertian:

			material_dat.scatter_direction = rmath.Vector3Methods.addVec( hit.normal, rmath.random_unit_vector() )
			if rmath.Vector3Methods.is_near_zero( material_dat.scatter_direction ):
				material_dat.scatter_direction = hit.normal
			material_dat.scattered = raycast.Ray(hit.position, material_dat.scatter_direction)
			material_dat.attenuation = self.albedo

		elif self.enum == EnumMaterial.Dieletric:

			refraction_ratio : float = hit.front_face and (1.0/self.indexOfRefraction) or self.indexOfRefraction
			unit_direction : rmath.Vector3 = rmath.Vector3Methods.unit( r_in )
			cos_theta : float = min(rmath.Vector3Methods.dot( rmath.Vector3Methods.multN( unit_direction, -1 ), hit.normal ), 1.0)
			sin_theta : float = sqrt(1.0 - (cos_theta*cos_theta))
			cannot_refract : bool = (refraction_ratio * sin_theta) > 1.0
			if (cannot_refract or MaterialMethods.reflectance(self, cos_theta, refraction_ratio) > rmath.randFloat()):
				direction : rmath.Vector3 = rmath.Vector3Methods.reflect(unit_direction, hit.normal)
			else:
				direction : rmath.Vector3 = rmath.Vector3Methods.refract(unit_direction, hit.normal, refraction_ratio)
			material_dat.scatter_direction = direction
			material_dat.attenuation = rmath.Vector3(1.0, 1.0, 1.0)
			material_dat.scattered = raycast.Ray(hit.position, direction)

		elif self.enum == EnumMaterial.Metal:

			reflected : rmath.Vector3 = rmath.Vector3Methods.reflect( rmath.Vector3Methods.unit( r_in.direction ), hit.normal )
			if reflected.dot(hit.normal) <= 0:
				return None
			material_dat.scatter_direction = reflected
			material_dat.scattered = raycast.Ray( hit.position, rmath.Vector3Methods.addVec(reflected, rmath.Vector3Methods.multN( rmath.random_in_unit_sphere(), self.fuzz) ) )
			material_dat.attenuation = self.albedo

		return material_dat
