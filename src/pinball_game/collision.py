import math

def ball_circle(ball, p2):
    dx = ball.x - p2.x
    dy = -ball.y + p2.y

    dist = math.hypot(dx, dy)
    collision_occurs = dist < ball.size + p2.size
    if collision_occurs:
        ball.angle = (math.atan2(dy, dx)) % (2*math.pi)
        overlap = 0.5*(ball.size + p2.size - dist+1)
        ball.x += math.cos(ball.angle)*overlap
        ball.y -= math.sin(ball.angle)*overlap
    return  collision_occurs


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
    seg_len = math.sqrt(seg_v.dot(seg_v))
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
