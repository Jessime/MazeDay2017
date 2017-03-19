from math import sqrt

def circle_circle(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce, i.e. update their angle, speed and position """

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap


def closest_point_on_seg(seg, pt):
    """Finds position on line closest to a given point, using projection

    Parameters
    ----------
    seg : Segment
        Line segment on which to find point
    pt : Point
        Off line point (usually center of circle)

    Returns
    -------
    proj_point : Point
        Location of closest point on seg
    """
    seg_v = seg.b - seg.a
    pt_v = pt - seg.a
    seg_len = sqrt(seg_v.dot(seg_v))
    seg_v_unit = seg_v.copy() / seg_len
    proj = pt_v.dot(seg_v_unit)
    if proj <= 0:
        return seg.a.copy()
    if proj >= seg_len:
        return seg.b.copy()
    return (seg_v_unit*proj)+seg.a

def segment_particle(seg, particle):
    """Check collision between a line segment and a circle.

    Parameters
    ----------
    seg : Segment
        A line segment containing Points 'a' and 'b'
    particle : Particle
        A circle described by a Point and a size (radius)
    """
    dist_v = closest_point_on_seg(seg, particle.pos)-particle.pos
    distsq = dist_v.dot(dist_v)
    return particle.size**2 >= distsq
