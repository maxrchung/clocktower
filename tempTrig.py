__author__ = 'Ira'
import math

def get_center_x(gear_radius, d_angle):
    p_angle = math.radians(d_angle)
    return gear_radius*math.cos(p_angle)

def get_center_y(gear_radius, d_angle):
    p_angle = math.radians(d_angle)
    return gear_radius*math.sin(p_angle)

