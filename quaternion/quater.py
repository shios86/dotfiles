#!/usr/bin/python3
import math
import sys

def rad(x):
    return (x * math.pi / 180)

def quater(x, y, z):
    c3 = math.cos(rad(x) / 2);
    c2 = math.cos(rad(y) / 2);
    c1 = math.cos(rad(z) / 2);
    
    s3 = math.sin(rad(x) / 2);
    s2 = math.sin(rad(y) / 2);
    s1 = math.sin(rad(z) / 2);

    # and now compute quaternion
    w = c1*c2*c3 - s1*s2*s3;
    x = c1*c2*s3 + s1*s2*c3;
    y = c1*s2*c3 - s1*c2*s3;
    z = s1*c2*c3 + c1*s2*s3;
    return w, x, y, z; 

#f h = heading angle (rotation about y)
#if a = attitude angle (rotation about z)
#if b = bank angle (rotation about x)

############################################################################################
# P2.x = x*(qx*qx+qw*qw-qy*qy- qz*qz) + y*(2*qx*qy- 2*qw*qz) + z*(2*qx*qz+ 2*qw*qy)        #
# P2.y = x*(2*qw*qz + 2*qx*qy) + y*(qw*qw - qx*qx+ qy*qy - qz*qz)+ z*(-2*qw*qx+ 2*qy*qz)   #
# P2.z = x*(-2*qw*qy+ 2*qx*qz) + y*(2*qw*qx+ 2*qy*qz)+ z*(qw*qw - qx*qx- qy*qy+ qz*qz)     #
############################################################################################
    
#euler rotation matrix
def mat(u, v, w, p1, p2, p3):
    x1 = p1
    y1 = p2*math.cos(rad(u)) + p3*math.sin(rad(u))
    z1 = -p2*math.sin(rad(u)) + p3*math.cos(rad(u))
    
    x2 = x1*math.cos(rad(v)) - z1*math.sin(rad(v))
    y2 = y1
    z2 = x1*math.sin(rad(v)) + z1*math.cos(rad(v))
    
    x3 = x2*math.cos(rad(w)) + y2*math.sin(rad(w))
    y3 = -x2*math.sin(rad(w)) + y2*math.cos(rad(w))
    z3 = z2
    return (x3, y3, z3)

#quaternion rotation

def quater_matrix(x, y, z, p1, p2, p3):
    q  = quater(x, y, z)
    xx = q[1] * q[1];
    xy = q[1] * q[2];
    xz = q[1] * q[3];
    xw = q[1] * q[0];

    yy = q[2] * q[2];
    yz = q[2] * q[3];
    yw = q[2] * q[0];

    zz = q[3] * q[3];
    zw = q[3] * q[0];

#    print("xx:%.6f xy:%.6f xz:%.6f\nxw:%.6f yy:%.6f yz:%.6f\nyw:%.6f zz:%.6f zw:%.6f" %(xx * 2, xy * 2, xz * 2, xw * 2, yy * 2, yz * 2, yw * 2, zz * 2, zw * 2))
 #   print("----")
    m00  = 1 - 2 * ( yy + zz );
    m01  =     2 * ( xy - zw );
    m02  =     2 * ( xz + yw );
    
    m10  =     2 * ( xy + zw );
    m11  = 1 - 2 * ( xx + zz );
    m12  =     2 * ( yz - xw );

    m20  =     2 * ( xz - yw );
    m21  =     2 * ( yz + xw );
    m22  = 1 - 2 * ( xx + yy );
    print("%-6d:%.6f %.6f %.6f\n%-6d:%.6f %.6f %.6f\n%-6d:%.6f %.6f %.6f" %(p1, m00, m01, m02, p2, m10, m11, m12, p3, m20, m21, m22))
    print("----")
    return (p1*m00) + (p2*m10) + (p3*m20),\
           (p1*m01) + (p2*m11) + (p3*m21),\
           (p1*m02) + (p2*m12) + (p3*m22)
    # m00  = ww + xx - yy - zz;
    # m01  =     2 * ( xy - zw );
    # m02  =     2 * ( xz + yw );
    
    # m10  =     2 * ( xy + zw );
    # m11  = ww - xx + yy - zz;
    # m12  =     2 * ( yz - xw );

    # m20  =     2 * ( xz - yw );
    # m21  =     2 * ( yz + xw );
    # m22  = ww - xx - yy + zz;
    #http://www.andre-gaschler.com/rotationconverter/
if __name__ == "__main__":
    print("qua:%-7.3f %-7.3f %-7.3f" %quater_matrix(float(sys.argv[1]),
                                           float(sys.argv[2]),
                                           float(sys.argv[3]),
                                           float(sys.argv[4]),
                                           float(sys.argv[5]),
                                           float(sys.argv[6])))
    print("mat:%-7.3f %-7.3f %-7.3f" %mat(float(sys.argv[1]),
                                float(sys.argv[2]),
                                float(sys.argv[3]),
                                float(sys.argv[4]),
                                float(sys.argv[5]),
                                float(sys.argv[6])))
    print("%.6f %.6f %.6f %.6f"%quater(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])))
