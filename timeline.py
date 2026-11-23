"""Lost and Found: the one timeline every part reads (picture and sound).

Angles of the umbrella are in degrees: positive leans right, onto the shelf
upright (its resting place); negative leans left, toward the far door.
"""
import math

FPS = 24
DUR = 62.0
NFRAMES = int(round(DUR * FPS))
REST = 1.5


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * x * (x * (x * 6 - 15) + 10)


def seg(t, a, b):
    return smooth((t - a) / (b - a))


EVENTS = [
    dict(o=9.0, od=1.6, door=74.0, c=13.4, cd=2.6,
         ld=0.55, li=1.9, lean=-4.5, s=14.4, sd=3.4,
         fig=dict(side=1, x_in=-3.05, y=10.55, t_in=10.0, t_stand=11.0,
                  t_back=None, t_out=12.6, t_gone=13.6, step_y=None, height=1.74)),
    dict(o=28.0, od=1.3, door=80.0, c=33.5, cd=2.6,
         ld=0.22, li=1.4, lean=-9.0, s=34.4, sd=4.8,
         fig=dict(side=-1, x_in=-3.0, y=10.5, t_in=28.6, t_stand=29.6,
                  t_back=31.8, t_out=32.6, t_gone=33.6, step_y=9.8, height=1.83)),
    dict(o=47.0, od=3.6, door=70.0, c=None, cd=None,
         ld=0.15, li=2.8, lean=-14.0, s=None, sd=None, creep=-3.0, fig=None),
]


def door_angle(t):
    a = 0.0
    for e in EVENTS:
        if t < e['o']:
            break
        v = e['door'] * seg(t, e['o'], e['o'] + e['od'])
        if e['c'] is not None:
            v *= 1.0 - seg(t, e['c'], e['c'] + e['cd'])
        a = v
    return a


def umb_angle(t):
    a = REST
    for e in EVENTS:
        if t < e['o']:
            break
        ls = e['o'] + e['ld']
        lean = REST + (e['lean'] - REST) * seg(t, ls, ls + e['li'])
        if e['s'] is not None:
            a = lean + (REST - e['lean']) * seg(t, e['s'], e['s'] + e['sd'])
        else:
            a = lean + e.get('creep', 0.0) * seg(t, ls + e['li'], DUR)
    return a


def figures(t):
    out = []
    for i, e in enumerate(EVENTS):
        f = e['fig']
        if not f or t < f['t_in'] - 0.01 or t > f['t_gone'] + 0.01:
            continue
        far = f['x_in'] + 1.5 * f['side']
        if t < f['t_stand']:
            k = seg(t, f['t_in'], f['t_stand'])
            x = far + (f['x_in'] - far) * k
        elif t < f['t_out']:
            x = f['x_in']
        else:
            k = seg(t, f['t_out'], f['t_gone'])
            x = f['x_in'] + (far - f['x_in']) * k
        y = f['y']
        if f['step_y'] is not None:
            tb = f['t_back']
            ki = seg(t, f['t_stand'], f['t_stand'] + 0.8)
            ko = seg(t, tb, tb + 0.8)
            y = f['y'] + (f['step_y'] - f['y']) * ki * (1 - ko)
        moving = (f['t_in'] < t < f['t_stand']) or (f['t_out'] < t < f['t_gone'])
        bob = 0.018 * abs(math.sin(t * math.pi * 1.9)) if moving else 0.0
        out.append((i, x, y, f['height'], bob))
    return out


def state(frame):
    t = frame / FPS
    return dict(t=t, door=door_angle(t), umb=umb_angle(t), figs=figures(t))
