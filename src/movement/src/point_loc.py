from math import degrees, cos, atan, tan, sin, sqrt, asin, radians

#---Constants-----
max_dis = 3000 #maximum distance from user robot

def point_loc(x1, y1, z1, x2, y2, z2, ur_dis):
    #print (str(y2))
    if y2 >= 0:
        alpha = radians(0)
        loc_dis = max_dis
    else:
        alpha = atan((x1 - x2)/(y1 - y2))
        #print (str(degrees(alpha)))
        loc_dis = average_height * tan(alpha)
        if loc_dis > max_dis:
            loc_dis = max_dis

    if z1 == z2:
        beta = radians(90)
    else:
        beta = atan((x1 - x2)/(z1 - z2))

    print (str(degrees(alpha)))
    print (str(degrees(beta)))
    print (str(loc_dis))

    trav_dis = sqrt(loc_dis**2 + ur_dis**2 - loc_dis*ur_dis*cos(beta))
    print (str(trav_dis))
    zeta = asin(sin(beta)*(loc_dis/trav_dis))
    print (str(degrees(zeta)))

#------Main--------
if __name__ == '__main__':
    point_loc(0, 0, 0, -68, -12, -65, ur_distance())
