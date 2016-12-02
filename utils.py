from __future__ import division
import math

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i


def intersect(x, y, l, theta, x0, y0, r):
    x -= x0
    y -= y0
    a = math.tan(theta)
    b = y - a * x

    disc = a**2 * r**2 - b**2 + r**2
    if disc <= 0:
        return 1.0

    sqrtdisc = math.sqrt(disc)
    t1 = (- a * b + sqrtdisc) / (a**2 + 1);
    t2 = (- a * b - sqrtdisc) / (a**2 + 1);
    x2 = x + l * math.cos(theta)
    if (x < t2 and x2 < t2) or (x > t1 and x2 > t1):
        return 1.0
    if t2 < x < t1:
        return 0.0
    return min(abs(x - t2), abs(x - t1)) / abs(x - x2)
