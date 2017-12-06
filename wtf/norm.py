#!/usr/bin/python3

import math
import sys

def norm(w, x, y, z):
    n = math.sqrt(w**2 + x**2 + y**2 + z**2)
    w /= n
    x /= n
    y /= n
    z /= n
    return w, y, y, z

def quat(x, y, z, w):
    ww = math.cos(w / 2)
    f = math.sin(w / 2)
    x = x * f
    y = y * f
    z = z * f
    return ww, x, y, z

def quat_mul(q, l):
    r = (q[0]*l[0] - q[1]*l[1] - q[2]*l[2] - q[3]*l[3],
         q[0]*l[1] + q[1]*l[0] - q[2]*l[3] + q[3]*l[2],
         q[0]*l[2] + q[1]*l[3] + q[2]*l[0] - q[3]*l[1],
         q[0]*l[3] - q[1]*l[2] + q[2]*l[1] + q[3]*l[0])
    return (r);
def quat_rot_vec3d_(q, x, y, z):
    xx = x*(q[1]*q[1] + q[0]*q[0] - q[2]*q[2] - q[3]*q[3]) + y*(2*q[1]*q[2] - 2*q[0]*q[3]) + z*(2*q[1]*q[3] + 2*q[0]*q[2])
    yy = x*(2*q[0]*q[3] + 2*q[1]*q[2]) + y*(q[0]*q[0] - q[1]*q[1] + q[2]*q[2] - q[3]*q[3]) + z*(-2*q[0]*q[1] + 2*q[2]*q[3])
    zz = x*(-2*q[0]*q[2] + 2*q[1]*q[3]) + y*(2*q[0]*q[1] + 2*q[2]*q[3]) + z*(q[0]*q[0] - q[1]*q[1]- q[2]*q[2] + q[3]*q[3])
    return (xx, yy, zz)

def quat_rot_vec3d(q, x, y, z):
    xx = x*(q[1]*q[1] + q[0]*q[0] - q[2]*q[2] - q[3]*q[3]) + y*(2*q[1]*q[2] - 2*q[0]*q[3]) + z*(2*q[1]*q[3] + 2*q[0]*q[2])
    yy = x*(2*q[0]*q[3] + 2*q[1]*q[2]) + y*(q[0]*q[0] - q[1]*q[1] + q[2]*q[2] - q[3]*q[3]) + z*(-2*q[0]*q[1] + 2*q[2]*q[3])
    zz = x*(-2*q[0]*q[2] + 2*q[1]*q[3]) + y*(2*q[0]*q[1] + 2*q[2]*q[3]) + z*(q[0]*q[0] - q[1]*q[1]- q[2]*q[2] + q[3]*q[3])
    return (xx, yy, zz)


if __name__ == "__main__":
    # w = float(sys.argv[1])
    # x = float(sys.argv[2])
    # y = float(sys.argv[3])
    # z = float(sys.argv[4])
    # q = norm(w, x, y, z)
    #    q = norm(q[0], q[1], q[2], q[3])
    #    q = (q[0]*l[0], q[1]*l[1], q[2]*l[2], q[3]*l[3])
    l = quat(0, 0, 1, 165*math.pi /180);
    q = l
    l = quat(0, 1, 0, 65*math.pi /180);
    q = quat_mul(q, l)
    l = q
    # print("%.6f %.6f %.6f %.6f" %q)
    # print("%.6f %.6f %.6f %.6f" %l)
    # print("%.6f %.6f %.6f %.6f" %quat_mul(q, l))
    print("%.6f %.6f %.6f" %quat_rot_vec3d(l, 10, 10, 10))
