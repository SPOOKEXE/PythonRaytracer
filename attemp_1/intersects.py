
from rmath import (Vector3, Vector3Methods)

def IsPointInSphere( point : Vector3, center : Vector3, radius : float ) -> bool:
	d = Vector3Methods.subVec( center, point )
	return (d.x*d.x + d.y*d.y + d.z*d.z) < (radius * radius)

def LineIntersectAxisAlignedBox( rayOrigin : Vector3, rayDirection : Vector3, boxMin : Vector3, boxMax : Vector3 ) -> Vector3 | None:
	minBox : Vector3 = Vector3Methods.subVec( boxMin, rayOrigin )
	maxBox : Vector3 = Vector3Methods.subVec( boxMax, rayOrigin )
	near : float = -9e9
	far : float = 9e9

	# X
	t1 : float = minBox.x / rayDirection.x
	t2  : float = maxBox.x / rayDirection.x
	tMin : float = min(t1, t2)
	tMax : float = max(t1, t2)
	if (tMin > near): near = tMin
	if (tMax < far): far = tMax
	if (near > far or far < 0):
		return None

	# Y
	t1 = minBox.y / rayDirection.y
	t2 = maxBox.y / rayDirection.y
	tMin = min(t1, t2)
	tMax = max(t1, t2)
	if (tMin > near): near = tMin
	if (tMax < far): far = tMax
	if (near > far or far < 0):
		return None

	# Z
	t1 : float = minBox.z / rayDirection.z
	t2 : float = maxBox.z / rayDirection.z
	tMin : float = min(t1, t2)
	tMax : float = max(t1, t2)
	if (tMin > near): near = tMin
	if (tMax < far): far = tMax
	if (near > far or far < 0):
		return None

	# return
	return Vector3(
		Vector3Methods.addVec(rayOrigin, Vector3Methods.multN(rayDirection, near)),
		Vector3Methods.addVec(rayOrigin, Vector3Methods.multN(rayDirection, far))
	)
