import math

def circle_circle(ball, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce, i.e. update their angle, speed and position """

    dx = ball.x - p2.x
    dy = ball.y - p2.y

    dist = math.hypot(dx, dy)
    collision_occurs = dist < ball.size + p2.size
    if collision_occurs:
        angle = (math.atan2(dy, dx) + 0.5 * math.pi) % (2*math.pi)
        total_mass = ball.mass + p2.mass
        # print(ball.speed)
        print(ball.angle,ball.speed*(ball.mass-p2.mass)/total_mass,
                                              angle,
                                              2*p2.speed*p2.mass/total_mass)
        (ball.angle, ball.speed) = ball.addVectors(ball.angle,
                                              ball.speed*(ball.mass-p2.mass)/total_mass,
                                              angle,
                                              2*p2.speed*p2.mass/total_mass)
        print(ball.angle,ball.speed)
        # 1/0
        # (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-ball.mass)/total_mass, angle+math.pi, 2*ball.speed*ball.mass/total_mass)
        # print(ball.speed)
        elasticity = ball.elasticity * p2.elasticity
        ball.speed *= elasticity
        # p2.speed *= elasticity
        # print(ball.speed)

        overlap = 0.5*(ball.size + p2.size - dist+1)
        ball.x += math.sin(angle)*overlap
        ball.y -= math.cos(angle)*overlap
        # p2.x -= math.sin(angle)*overlap
        # p2.y += math.cos(angle)*overlap
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
