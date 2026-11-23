import sys, math, wave
import numpy as np
import timeline as TL
SR = 48000
N = int(TL.DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(11)
F = np.fft.rfftfreq(N, 1 / SR)
def onepole(x, fc):
    return np.fft.irfft(np.fft.rfft(x) / (1 + 1j * F / fc), N).astype(np.float32)
def band(x, lo, hi):
    m = 1 / (1 + (lo / np.maximum(F, 1e-3)) ** 4) / (1 + (F / hi) ** 4)
    return np.fft.irfft(np.fft.rfft(x) * m, N).astype(np.float32)
def noise():
    return rng.standard_normal(N).astype(np.float32)
L = np.zeros(N, np.float32); R = np.zeros(N, np.float32)
L += onepole(noise(), 350) * 0.05 + band(noise(), 40, 160) * 0.06
R += onepole(noise(), 350) * 0.05 + band(noise(), 40, 160) * 0.06
wob = 1 + 0.15 * np.sin(2 * np.pi * 0.13 * t) + 0.08 * np.sin(2 * np.pi * 0.71 * t)
hum = (0.010 * np.sin(2 * np.pi * 100 * t) + 0.006 * np.sin(2 * np.pi * 200 * t + 1) + 0.003 * np.sin(2 * np.pi * 300 * t + 2)) * wob
buzz = band(noise(), 2400, 6000) * 0.004 * (0.6 + 0.4 * np.sin(2 * np.pi * 100 * t) ** 2)
L += hum + buzz; R += hum * 0.9 + buzz
for c, dur, pan in [(2.0, 14.0, 0.3), (19.0, 12.0, 0.7), (37.0, 9.0, 0.5)]:
    e = np.exp(-((t - c - dur / 2) / (dur / 3)) ** 2).astype(np.float32)
    r = band(noise(), 25, 140) * 0.22 * e
    cl = band(noise(), 300, 900) * 0.02 * e * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 1.6 * t)))
    L += (r + cl) * (1 - pan); R += (r + cl) * pan
e = np.exp(-((t - 22.5) / 1.4) ** 2).astype(np.float32)
horn = onepole(((np.sin(2 * np.pi * 311 * t) + 0.6 * np.sin(2 * np.pi * 370 * t)) * 0.006 * e).astype(np.float32), 700)
L += horn * 0.4; R += horn * 0.8
def place(at, s):
    out = np.zeros(N, np.float32); i = int(at * SR); n = min(len(s), N - i)
    if n > 0: out[i:i + n] = s[:n]
    return out
def click(at, amp, fc=2500, dur=0.012):
    n = int(dur * SR)
    s = rng.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / (n / 5))
    return band(place(at, s * amp), 200, fc * 3)
def thud(at, amp):
    n = int(0.5 * SR); k = np.arange(n) / SR
    s = np.sin(2 * np.pi * 62 * k) * np.exp(-k * 14) + rng.standard_normal(n) * 0.25 * np.exp(-k * 40)
    return onepole(place(at, (s * amp).astype(np.float32)), 900)
def creak(a, dur, amp, f0=180):
    n = int(dur * SR); k = np.arange(n) / SR
    f = f0 * (1 + 0.25 * np.sin(2 * np.pi * 0.9 * k / dur))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.3 + np.sin(ph * 2.01) * 0.4
    s *= np.sin(np.pi * k / dur) ** 2 * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * k)))
    return band(place(a, (s * amp).astype(np.float32)), 150, 3000)
ts = t[::480]
openamt = np.interp(t, ts, np.array([math.sin(math.radians(TL.door_angle(x))) for x in ts])).astype(np.float32)
air = band(noise(), 200, 2500) * 0.05 * openamt + band(noise(), 60, 400) * 0.06 * openamt
L += air * 0.85; R += air * 0.35
for ev in TL.EVENTS:
    o = ev['o']
    d = click(o - 0.08, 0.10) + creak(o, ev['od'] * 0.9, 0.025 if ev['c'] else 0.04, 170 if ev['c'] else 140)
    if ev['c']:
        cl = ev['c']
        d += creak(cl, ev['cd'] * 0.7, 0.015, 200) + thud(cl + ev['cd'] - 0.05, 0.22) + click(cl + ev['cd'], 0.08)
    L += d * 0.85; R += d * 0.35
    f = ev['fig']
    if f:
        for st in list(np.arange(f['t_in'], f['t_stand'], 0.52)) + list(np.arange(f['t_out'], f['t_gone'], 0.52)):
            s = click(st, 0.05, 1200, 0.03); L += s * 0.7; R += s * 0.25
last = TL.EVENTS[-1]['o']
tone_e = np.clip((t - last - 2.0) / 6.0, 0, 1) ** 2 * np.clip((TL.DUR - 0.3 - t) / 2.5, 0, 1)
tone = (np.sin(2 * np.pi * 55 * t) * 0.03 + np.sin(2 * np.pi * 82.4 * t) * 0.008) * tone_e
L += tone; R += tone
mix = np.stack([L, R], 1)
fade = np.clip(t / 1.5, 0, 1) * np.clip((TL.DUR - t) / 0.25, 0, 1)
mix *= fade[:, None]
mix /= np.abs(mix).max() / 0.7
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
print('wrote')
