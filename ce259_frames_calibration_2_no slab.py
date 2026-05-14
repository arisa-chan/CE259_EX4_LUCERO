# %%
# Di Sarno (2012)
import openseespy.opensees as ops
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import opsvis as opsv
import math

ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 6)

# Main nodes
ops.node(1, 0, 0, 0)
ops.node(2, 4.7, 0, 0)
ops.node(3, 0, 2.85, 0)
ops.node(4, 4.7, 2.85, 0)
ops.node(5, 0, 5.7, 0)
ops.node(6, 4.7, 5.7, 0)

ops.node(7, 0, 0, 4.3)
ops.node(8, 4.7, 0, 4.3)
ops.node(9, 0, 2.85, 4.3)
ops.node(10, 4.7, 2.85, 4.3)
ops.node(11, 0, 5.7, 4.3)
ops.node(12, 4.7, 5.7, 4.3)
ops.node(19, 4.7/3, 0, 4.3)
ops.node(20, 2*4.7/3, 0, 4.3)
ops.node(21, 4.7/3, 2.85, 4.3)
ops.node(22, 2*4.7/3, 2.85, 4.3)
ops.node(23, 4.7/3, 5.7, 4.3)
ops.node(24, 2*4.7/3, 5.7, 4.3)
ops.node(25, 0, 2.85/3, 4.3)
ops.node(26, 0, 2*2.85/3, 4.3)
ops.node(27, 0, 2.85 + 2.85/3, 4.3)
ops.node(28, 0, 2.85 + 2*2.85/3, 4.3)
ops.node(29, 4.7, 2.85/3, 4.3)
ops.node(30, 4.7, 2*2.85/3, 4.3)
ops.node(31, 4.7, 2.85 + 2.85/3, 4.3)
ops.node(32, 4.7, 2.85 + 2*2.85/3, 4.3)

ops.node(13, 0, 0, 7.6)
ops.node(14, 4.7, 0, 7.6)
ops.node(15, 0, 2.85, 7.6)
ops.node(16, 4.7, 2.85, 7.6)
ops.node(17, 0, 5.7, 7.6)
ops.node(18, 4.7, 5.7, 7.6)
ops.node(33, 4.7/3, 0, 7.6)
ops.node(34, 2*4.7/3, 0, 7.6)
ops.node(35, 4.7/3, 2.85, 7.6)
ops.node(36, 2*4.7/3, 2.85, 7.6)
ops.node(37, 4.7/3, 5.7, 7.6)
ops.node(38, 2*4.7/3, 5.7, 7.6)
ops.node(39, 0, 2.85/3, 7.6)
ops.node(40, 0, 2*2.85/3, 7.6)
ops.node(41, 0, 2.85 + 2.85/3, 7.6)
ops.node(42, 0, 2.85 + 2*2.85/3, 7.6)
ops.node(43, 4.7, 2.85/3, 7.6)
ops.node(44, 4.7, 2*2.85/3, 7.6)
ops.node(45, 4.7, 2.85 + 2.85/3, 7.6)
ops.node(46, 4.7, 2.85 + 2*2.85/3, 7.6)

ops.fix(1, 1, 1, 1, 1, 1, 1)
ops.fix(2, 1, 1, 1, 1, 1, 1)
ops.fix(3, 1, 1, 1, 1, 1, 1)
ops.fix(4, 1, 1, 1, 1, 1, 1)
ops.fix(5, 1, 1, 1, 1, 1, 1)
ops.fix(6, 1, 1, 1, 1, 1, 1)

# Concrete material
# f_cm = 19.4 MPa, E_cm = 26.672 GPa, sigma_f_cm = 1.3 MPa
ops.uniaxialMaterial('Concrete02', 11, -19.4e3, -0.002, -19.4e3 * 0.2, -0.0038, 0.1, 0.62e3 * math.sqrt(19.4), 0.05 * 4700e3 * math.sqrt(19.4))
# ops.uniaxialMaterial('Concrete02', 11, -28.3e3, -0.002, -28.3e3 * 0.2, -0.0038, 0.1, 0.62e3 * math.sqrt(28.3), 0.1 * 4700e3 * math.sqrt(28.3))

# Reinforcement material
# diameter 6mm: f_y_low = 338.7 MPa, f_y_high = 358.6 MPa, f_u = 433.9 MPa, ultimate elongation = 50%
# diameter 8mm: f_y_low = 345.9 MPa, f_y_high = 355.8 MPa, f_u = 438.3 MPa, ultimate elongation = 42%
# diameter 10mm: f_y_low = 350.8 MPa, f_y_high = 354.1 MPa, f_u = 515.1 MPa, ultimate elongation = 34%
# diameter 12mm: f_y_low = 322.3 MPa, f_y_high = 342.2 MPa, f_u = 415.4 MPa, ultimate elongation = 38%
# diameter 14mm: f_y_low = 334.1 MPa, f_y_high = 348.1 MPa, f_u = 444.0 MPa, ultimate elongation = 41%
# diameter 16mm: f_y_low = 312.7 MPa, f_y_high = 329.7 MPa, f_u = 417.5 MPa, ultimate elongation = 43%
ops.uniaxialMaterial('Steel02', 12, (338.7e3 + 358.6e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 6mm
ops.uniaxialMaterial('Steel02', 13, (345.9e3 + 355.8e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 8mm
ops.uniaxialMaterial('Steel02', 14, (350.8e3 + 354.1e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 10mm
ops.uniaxialMaterial('Steel02', 15, (322.3e3 + 342.2e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 12mm
ops.uniaxialMaterial('Steel02', 16, (334.1e3 + 348.1e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 14mm
ops.uniaxialMaterial('Steel02', 17, (312.7e3 + 329.7e3)/2, 210.0e6, 0.18, 18.0, 0.925, 0.15)    # diameter 16mm

# Minmax material
ops.uniaxialMaterial('MinMax', 1, 11, '-min', -0.01)                # Concrete
ops.uniaxialMaterial('MinMax', 2, 12, '-min', -0.1, '-max', 0.1)    # Steel 6mm
ops.uniaxialMaterial('MinMax', 3, 13, '-min', -0.1, '-max', 0.1)    # Steel 8mm
ops.uniaxialMaterial('MinMax', 4, 14, '-min', -0.1, '-max', 0.1)    # Steel 10mm
ops.uniaxialMaterial('MinMax', 5, 15, '-min', -0.1, '-max', 0.1)    # Steel 12mm
ops.uniaxialMaterial('MinMax', 6, 16, '-min', -0.1, '-max', 0.1)    # Steel 14mm
ops.uniaxialMaterial('MinMax', 7, 17, '-min', -0.1, '-max', 0.1)    # Steel 16mm

# CROSS-SECTIONS
# Beams 1-5 & 2-6
# Dimensions: 300mm x 500mm, cover: 25mm
# Left and right support (L/3) reinforcements : top: D12-D16-D12, bottom: D12-D12, web: D8-D8, stirrups: D6 @ 300mm o.c.
# Midspan (L/3) reinforcements : top: D12-D12, bottom: D12-D12, web: D8-D8, stirrups: D6 @ 300mm o.c.
#
# ORIENTATION (matches existing/working geomTransf settings):
#   local y-axis  →  beam WIDTH  (bw = 0.3 m)
#   local z-axis  →  beam DEPTH  (h  = 0.5 m, vertical in service)
# Top bars sit at    z = +(h/2 - cover - d/2)
# Bottom bars sit at z = -(h/2 - cover - d/2)
# Bars on a face are spaced EQUALLY in y (across the width) between the two corner bars.
bw = 0.3
h = 0.5
cover = 0.025

# Reusable coordinates (corner-bar centres along width; top/bottom positions along depth)
_yL12 = -bw/2 + cover + 0.012/2          # left  D12 corner, along width (y)
_yR12 =  bw/2 - cover - 0.012/2          # right D12 corner, along width (y)
_yL8  = -bw/2 + cover + 0.008/2          # left  D8 web bar (y)
_yR8  =  bw/2 - cover - 0.008/2          # right D8 web bar (y)
_zT12 =  h/2 - cover - 0.012/2           # z of D12 top-row centre (along depth)
_zB12 = -h/2 + cover + 0.012/2           # z of D12 bottom-row centre


def _equispaced_y(n_bars):
    """Return list of y-coords for n_bars equally spaced between the two D12 corners (across width)."""
    if n_bars == 1:
        return [0.0]
    step = (_yR12 - _yL12) / (n_bars - 1)
    return [_yL12 + k * step for k in range(n_bars)]


# ---------- Section 1 : beams 1-5 / 2-6, support thirds ----------
# top:    D12, D16, D12   (3 bars)
# bottom: D12, D12        (2 bars)
_y_top = _equispaced_y(3)
_y_bot = _equispaced_y(2)
beam_15_26_support = [
    ['section', 'Fiber', 1, '-GJ', 1],
    # patches: (yI, zI, yJ, zJ) – y = width, z = depth
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],          # top cover
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],          # bottom cover
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],  # left side cover
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],          # right side cover
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],  # core
    # top bars: D12, D16, D12 (equally spaced in z)
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top[0], _zT12,  _y_top[0], _zT12],   # D12
    ['layer', 'straight', 6, 1, math.pi/4 * 0.016**2,  _y_top[1], h/2 - cover - 0.016/2,  _y_top[1], h/2 - cover - 0.016/2],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top[2], _zT12,  _y_top[2], _zT12],   # D12
    # bottom bars: D12, D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot[0], _zB12,  _y_bot[0], _zB12],   # D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot[1], _zB12,  _y_bot[1], _zB12],   # D12
    # web bars: 2 D8 at mid-depth
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

# ---------- Section 2 : beams 1-5 / 2-6, midspan third ----------
# top: D12,D12   bottom: D12,D12
_y_2bar = _equispaced_y(2)
beam_15_26_midspan = [
    ['section', 'Fiber', 2, '-GJ', 1],
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],
    # top bars: 2 × D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_2bar[0], _zT12,  _y_2bar[0], _zT12],
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_2bar[1], _zT12,  _y_2bar[1], _zT12],
    # bottom bars: 2 × D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_2bar[0], _zB12,  _y_2bar[0], _zB12],
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_2bar[1], _zB12,  _y_2bar[1], _zB12],
    # web bars: 2 × D8
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

opsv.plot_fiber_section(beam_15_26_support)
opsv.fib_sec_list_to_cmds(beam_15_26_support)
opsv.plot_fiber_section(beam_15_26_midspan)
opsv.fib_sec_list_to_cmds(beam_15_26_midspan)


# ---------- Section 3 : beams 3-4 1st floor, support thirds ----------
# top:    D12, D16, D16, D16, D12   (5 bars)
# bottom: D12, D16, D12             (3 bars)
_y_top5 = _equispaced_y(5)
_y_bot3 = _equispaced_y(3)
beams_34_support_1st = [
    ['section', 'Fiber', 3, '-GJ', 1],
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],
    # top bars: D12 | D16 | D16 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top5[0], _zT12,  _y_top5[0], _zT12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_top5[1], _zT12,  _y_top5[1], _zT12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_top5[2], _zT12,  _y_top5[2], _zT12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_top5[3], _zT12,  _y_top5[3], _zT12],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top5[4], _zT12,  _y_top5[4], _zT12],   # D12
    # bottom bars: D12 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot3[0], _zB12,  _y_bot3[0], _zB12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot3[1], _zB12,  _y_bot3[1], _zB12],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot3[2], _zB12,  _y_bot3[2], _zB12],   # D12
    # web bars
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

# ---------- Section 4 : beams 3-4 1st floor, midspan third ----------
# top:    D12, D12                       (2 bars)
# bottom: D12, D16, D16, D16, D16, D12   (6 bars)
_y_top2 = _equispaced_y(2)
_y_bot6 = _equispaced_y(6)
beams_34_midspan_1st = [
    ['section', 'Fiber', 4, '-GJ', 1],
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],
    # top bars: 2 × D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top2[0], _zT12,  _y_top2[0], _zT12],
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top2[1], _zT12,  _y_top2[1], _zT12],
    # bottom bars: D12 | D16 | D16 | D16 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot6[0], _zB12,  _y_bot6[0], _zB12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot6[1], _zB12,  _y_bot6[1], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot6[2], _zB12,  _y_bot6[2], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot6[3], _zB12,  _y_bot6[3], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot6[4], _zB12,  _y_bot6[4], _zB12],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot6[5], _zB12,  _y_bot6[5], _zB12],   # D12
    # web bars
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

opsv.plot_fiber_section(beams_34_support_1st)
opsv.fib_sec_list_to_cmds(beams_34_support_1st)
opsv.plot_fiber_section(beams_34_midspan_1st)
opsv.fib_sec_list_to_cmds(beams_34_midspan_1st)


# ---------- Section 5 : beams 3-4 2nd floor, support thirds ----------
# top:    D12, D16, D12          (3 bars)
# bottom: D12, D16, D16, D12     (4 bars)
_y_top3 = _equispaced_y(3)
_y_bot4 = _equispaced_y(4)
beam_34_support_2nd = [
    ['section', 'Fiber', 5, '-GJ', 1],
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],
    # top bars: D12 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top3[0], _zT12,  _y_top3[0], _zT12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_top3[1], h/2 - cover - 0.016/2,  _y_top3[1], h/2 - cover - 0.016/2],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top3[2], _zT12,  _y_top3[2], _zT12],   # D12
    # bottom bars: D12 | D16 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot4[0], _zB12,  _y_bot4[0], _zB12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot4[1], _zB12,  _y_bot4[1], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot4[2], _zB12,  _y_bot4[2], _zB12],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot4[3], _zB12,  _y_bot4[3], _zB12],   # D12
    # web bars
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

# ---------- Section 6 : beams 3-4 2nd floor, midspan third ----------
# top:    D12, D12                  (2 bars)
# bottom: D12, D16, D16, D16, D12   (5 bars)
_y_bot5 = _equispaced_y(5)
beam_34_midspan_2nd = [
    ['section', 'Fiber', 6, '-GJ', 1],
    ['patch', 'rect', 1, 30,  3, -bw/2,         h/2 - cover, bw/2,         h/2],
    ['patch', 'rect', 1, 30,  3, -bw/2,        -h/2,         bw/2,         -h/2 + cover],
    ['patch', 'rect', 1,  8, 24, -bw/2,        -h/2 + cover, -bw/2 + cover, h/2 - cover],
    ['patch', 'rect', 1,  8, 24,  bw/2 - cover, -h/2 + cover, bw/2,          h/2 - cover],
    ['patch', 'rect', 1, 24, 24, -bw/2 + cover, -h/2 + cover, bw/2 - cover,  h/2 - cover],
    # top bars: 2 × D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top2[0], _zT12,  _y_top2[0], _zT12],
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_top2[1], _zT12,  _y_top2[1], _zT12],
    # bottom bars: D12 | D16 | D16 | D16 | D12
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot5[0], _zB12,  _y_bot5[0], _zB12],   # D12
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot5[1], _zB12,  _y_bot5[1], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot5[2], _zB12,  _y_bot5[2], _zB12],   # D16
    ['layer', 'straight', 7, 1, math.pi/4 * 0.016**2,  _y_bot5[3], _zB12,  _y_bot5[3], _zB12],   # D16
    ['layer', 'straight', 5, 1, math.pi/4 * 0.012**2,  _y_bot5[4], _zB12,  _y_bot5[4], _zB12],   # D12
    # web bars
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yL8, 0,  _yL8, 0],
    ['layer', 'straight', 3, 1, math.pi/4 * 0.008**2,  _yR8, 0,  _yR8, 0],
]

opsv.plot_fiber_section(beam_34_support_2nd)
opsv.fib_sec_list_to_cmds(beam_34_support_2nd)
opsv.plot_fiber_section(beam_34_midspan_2nd)
opsv.fib_sec_list_to_cmds(beam_34_midspan_2nd)

# Columns 1st story
c_x = 0.3
c_y = 0.3
cover = 0.025

column_1st = [
    ['section', 'Fiber', 7, '-GJ', 1],
    # rectangle section
    ['patch', 'rect', 1, 30, 3, -c_x/2, c_y/2 - cover, c_x/2, c_y/2],
    ['patch', 'rect', 1, 30, 3, -c_x/2, -c_y/2, c_x/2, -c_y/2 + cover],
    ['patch', 'rect', 1, 8, 24, -c_x/2, -c_y/2 + cover, -c_x/2 + cover, c_y/2 - cover],
    ['patch', 'rect', 1, 8, 24, c_x/2 - cover, -c_y/2 + cover, c_x/2, c_y/2 - cover],
    ['patch', 'rect', 1, 24, 24, -c_x/2 + cover, -c_y/2 + cover, c_x/2 - cover, c_y/2 - cover],
    # top and bottom bar: layer straight of 2 bars, D14, D14
    ['layer', 'straight', 6, 2, math.pi/4 * 0.012**2, -c_x/2 + cover, c_y/2 - cover, c_x/2 - cover, c_y/2 - cover],   # top layer
    ['layer', 'straight', 6, 2, math.pi/4 * 0.012**2, -c_x/2 + cover, -c_y/2 + cover, c_x/2 - cover, -c_y/2 + cover],   # bottom layer
]
column_2nd = [
    ['section', 'Fiber', 8, '-GJ', 1],
    # rectangle section
    ['patch', 'rect', 1, 30, 3, -c_x/2, c_y/2 - cover, c_x/2, c_y/2],
    ['patch', 'rect', 1, 30, 3, -c_x/2, -c_y/2, c_x/2, -c_y/2 + cover],
    ['patch', 'rect', 1, 8, 24, -c_x/2, -c_y/2 + cover, -c_x/2 + cover, c_y/2 - cover],
    ['patch', 'rect', 1, 8, 24, c_x/2 - cover, -c_y/2 + cover, c_x/2, c_y/2 - cover],
    ['patch', 'rect', 1, 24, 24, -c_x/2 + cover, -c_y/2 + cover, c_x/2 - cover, c_y/2 - cover],
    # top and bottom bar: layer straight of 2 bars, D12, D12
    ['layer', 'straight', 5, 2, math.pi/4 * 0.012**2, -c_x/2 + cover, c_y/2 - cover, c_x/2 - cover, c_y/2 - cover],   # top layer
    ['layer', 'straight', 5, 2, math.pi/4 * 0.012**2, -c_x/2 + cover, -c_y/2 + cover, c_x/2 - cover, -c_y/2 + cover],   # bottom layer
]

opsv.plot_fiber_section(column_1st)
opsv.fib_sec_list_to_cmds(column_1st)
opsv.plot_fiber_section(column_2nd)
opsv.fib_sec_list_to_cmds(column_2nd)

# --- Geometric Transformations (3-D PDelta) with rigid joint offsets ---
# geomTransf 1: columns along z-axis, vecxz = global x
ops.geomTransf('PDelta', 1, 1.0, 0.0, 0.0)

# geomTransf 2: Y-axis beams, vecxz = global x (places depth vertically)
ops.geomTransf('PDelta', 2, 1.0, 0.0, 0.0)

# geomTransf 3: X-axis beams, vecxz = global y (places depth vertically)
ops.geomTransf('PDelta', 3, 0.0, 1.0, 0.0)

# --- Beam Integrations (Lobatto, 5 points, one per fiber section) ---
for _sec_id in range(1, 9):
    ops.beamIntegration('Lobatto', _sec_id, _sec_id, 5)

# --- Elements ---
_ele_tag = 1

# Section 1 – y-axis beams, support/end regions (1st & 2nd floor)
for _i, _j in [
    (7, 25), (26, 9), (9, 27), (28, 11),
    (8, 29), (30, 10), (10, 31), (32, 12),
    (13, 39), (40, 15), (15, 41), (42, 17),
    (14, 43), (44, 16), (16, 45), (46, 18),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 2, 1)
    _ele_tag += 1

# Section 2 – y-axis beams, midspan regions (1st & 2nd floor)
for _i, _j in [
    (25, 26), (27, 28), (29, 30), (31, 32),
    (39, 40), (41, 42), (43, 44), (45, 46),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 2, 2)
    _ele_tag += 1

# Section 3 – x-axis beams, 1st floor, support regions
for _i, _j in [
    (7, 19), (20, 8), (9, 21), (22, 10), (11, 23), (24, 12),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 3, 3)
    _ele_tag += 1

# Section 4 – x-axis beams, 1st floor, midspan
for _i, _j in [
    (19, 20), (21, 22), (23, 24),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 3, 4)
    _ele_tag += 1

# Section 5 – x-axis beams, 2nd floor, support regions
for _i, _j in [
    (13, 33), (34, 14), (15, 35), (36, 16), (17, 37), (38, 18),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 3, 5)
    _ele_tag += 1

# Section 6 – x-axis beams, 2nd floor, midspan
for _i, _j in [
    (33, 34), (35, 36), (37, 38),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 3, 6)
    _ele_tag += 1

# Section 7 – columns, 1st storey (base → 1st floor)
for _i, _j in [
    (1, 7), (3, 9), (5, 11), (2, 8), (4, 10), (6, 12),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 1, 7)
    _ele_tag += 1

# Section 8 – columns, 2nd storey (1st floor → 2nd floor)
for _i, _j in [
    (7, 13), (9, 15), (11, 17), (8, 14), (10, 16), (12, 18),
]:
    ops.element('forceBeamColumn', _ele_tag, _i, _j, 1, 8)
    _ele_tag += 1

opsv.plot_model()

# LOADS
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

# Self-weight + slab self-weight transferred via yield-line theory (no slab elements)
# ================================================================
# Beam self-weights: 0.3x0.5m beams -> 3.6 kN/m; 0.3x0.3m columns -> 2.16 kN/m
# Slab: gamma_c = 24 kN/m^3; 1st floor t=250mm -> w=6.0 kN/m^2; 2nd floor t=200mm -> w=4.8 kN/m^2
# Slab panels: Lx=4.7m (long, x-dir), Ly=2.85m (short, y-dir); 45-degree yield lines
#
# SHORT beams (y-dir): triangular UDL, peak = w*Ly/2
#   Sub-element averages (3 equal divisions of Ly=2.85m, each 0.95m):
#     1st floor: [2.850, 7.125, 2.850] kN/m (single panel)
#     2nd floor: [2.280, 5.700, 2.280] kN/m (single panel)
#
# LONG beams (x-dir): trapezoidal UDL, peak = w*Ly/2
#   Sub-element averages (3 equal divisions of Lx=4.7m, each ~1.567m):
#     1st floor edge   : [4.663, 8.550, 4.663] kN/m (single panel)
#     1st floor interior (y=2.85, both panels): [9.326, 17.100, 9.326] kN/m
#     2nd floor edge   : [3.730, 6.840, 3.730] kN/m (single panel)
#     2nd floor interior (y=2.85, both panels): [7.460, 13.680, 7.460] kN/m
#
# Sign convention (unchanged from original):
#   Y-axis beams: local y = +global Z -> gravity = Wy = -(beam_sw + slab)
#   X-axis beams: local y = -global Z -> gravity = Wy = +(beam_sw + slab)
# ================================================================

# --- Y-axis beams, 1st floor, x=0, Panel A (nodes 7-25-26-9) ---
ops.eleLoad('-ele', 1,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 7->25
ops.eleLoad('-ele', 17, '-type', '-beamUniform', -(3.6 + 7.125), 0.0, 0.0)  # 25->26
ops.eleLoad('-ele', 2,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 26->9
# --- Y-axis beams, 1st floor, x=0, Panel B (nodes 9-27-28-11) ---
ops.eleLoad('-ele', 3,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 9->27
ops.eleLoad('-ele', 18, '-type', '-beamUniform', -(3.6 + 7.125), 0.0, 0.0)  # 27->28
ops.eleLoad('-ele', 4,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 28->11
# --- Y-axis beams, 1st floor, x=4.7, Panel A (nodes 8-29-30-10) ---
ops.eleLoad('-ele', 5,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 8->29
ops.eleLoad('-ele', 19, '-type', '-beamUniform', -(3.6 + 7.125), 0.0, 0.0)  # 29->30
ops.eleLoad('-ele', 6,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 30->10
# --- Y-axis beams, 1st floor, x=4.7, Panel B (nodes 10-31-32-12) ---
ops.eleLoad('-ele', 7,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 10->31
ops.eleLoad('-ele', 20, '-type', '-beamUniform', -(3.6 + 7.125), 0.0, 0.0)  # 31->32
ops.eleLoad('-ele', 8,  '-type', '-beamUniform', -(3.6 + 2.850), 0.0, 0.0)  # 32->12

# --- Y-axis beams, 2nd floor, x=0, Panel C (nodes 13-39-40-15) ---
ops.eleLoad('-ele', 9,  '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 13->39
ops.eleLoad('-ele', 21, '-type', '-beamUniform', -(3.6 + 5.700), 0.0, 0.0)  # 39->40
ops.eleLoad('-ele', 10, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 40->15
# --- Y-axis beams, 2nd floor, x=0, Panel D (nodes 15-41-42-17) ---
ops.eleLoad('-ele', 11, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 15->41
ops.eleLoad('-ele', 22, '-type', '-beamUniform', -(3.6 + 5.700), 0.0, 0.0)  # 41->42
ops.eleLoad('-ele', 12, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 42->17
# --- Y-axis beams, 2nd floor, x=4.7, Panel C (nodes 14-43-44-16) ---
ops.eleLoad('-ele', 13, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 14->43
ops.eleLoad('-ele', 23, '-type', '-beamUniform', -(3.6 + 5.700), 0.0, 0.0)  # 43->44
ops.eleLoad('-ele', 14, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 44->16
# --- Y-axis beams, 2nd floor, x=4.7, Panel D (nodes 16-45-46-18) ---
ops.eleLoad('-ele', 15, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 16->45
ops.eleLoad('-ele', 24, '-type', '-beamUniform', -(3.6 + 5.700), 0.0, 0.0)  # 45->46
ops.eleLoad('-ele', 16, '-type', '-beamUniform', -(3.6 + 2.280), 0.0, 0.0)  # 46->18

# --- X-axis beams, 1st floor, y=0, edge (nodes 7-19-20-8) ---
ops.eleLoad('-ele', 25, '-type', '-beamUniform', +(3.6 + 4.663), 0.0, 0.0)  # 7->19
ops.eleLoad('-ele', 31, '-type', '-beamUniform', +(3.6 + 8.550), 0.0, 0.0)  # 19->20
ops.eleLoad('-ele', 26, '-type', '-beamUniform', +(3.6 + 4.663), 0.0, 0.0)  # 20->8
# --- X-axis beams, 1st floor, y=2.85, interior – both panels (nodes 9-21-22-10) ---
ops.eleLoad('-ele', 27, '-type', '-beamUniform', +(3.6 + 9.326), 0.0, 0.0)  # 9->21
ops.eleLoad('-ele', 32, '-type', '-beamUniform', +(3.6 + 17.10), 0.0, 0.0)  # 21->22
ops.eleLoad('-ele', 28, '-type', '-beamUniform', +(3.6 + 9.326), 0.0, 0.0)  # 22->10
# --- X-axis beams, 1st floor, y=5.7, edge (nodes 11-23-24-12) ---
ops.eleLoad('-ele', 29, '-type', '-beamUniform', +(3.6 + 4.663), 0.0, 0.0)  # 11->23
ops.eleLoad('-ele', 33, '-type', '-beamUniform', +(3.6 + 8.550), 0.0, 0.0)  # 23->24
ops.eleLoad('-ele', 30, '-type', '-beamUniform', +(3.6 + 4.663), 0.0, 0.0)  # 24->12

# --- X-axis beams, 2nd floor, y=0, edge (nodes 13-33-34-14) ---
ops.eleLoad('-ele', 34, '-type', '-beamUniform', +(3.6 + 3.730), 0.0, 0.0)  # 13->33
ops.eleLoad('-ele', 40, '-type', '-beamUniform', +(3.6 + 6.840), 0.0, 0.0)  # 33->34
ops.eleLoad('-ele', 35, '-type', '-beamUniform', +(3.6 + 3.730), 0.0, 0.0)  # 34->14
# --- X-axis beams, 2nd floor, y=2.85, interior – both panels (nodes 15-35-36-16) ---
ops.eleLoad('-ele', 36, '-type', '-beamUniform', +(3.6 + 7.460), 0.0, 0.0)  # 15->35
ops.eleLoad('-ele', 41, '-type', '-beamUniform', +(3.6 + 13.68), 0.0, 0.0)  # 35->36
ops.eleLoad('-ele', 37, '-type', '-beamUniform', +(3.6 + 7.460), 0.0, 0.0)  # 36->16
# --- X-axis beams, 2nd floor, y=5.7, edge (nodes 17-37-38-18) ---
ops.eleLoad('-ele', 38, '-type', '-beamUniform', +(3.6 + 3.730), 0.0, 0.0)  # 17->37
ops.eleLoad('-ele', 42, '-type', '-beamUniform', +(3.6 + 6.840), 0.0, 0.0)  # 37->38
ops.eleLoad('-ele', 39, '-type', '-beamUniform', +(3.6 + 3.730), 0.0, 0.0)  # 38->18

# Columns (ele 43-54): beam self-weight only
ops.eleLoad('-ele', *list(range(43, 55)), '-type', '-beamUniform', 0.0, 0.0, -2.16)

# ANALYSIS
ops.system('BandGeneral')
ops.constraints('Transformation')
ops.numberer('RCM')
ops.test('NormDispIncr', 1.0e-12, 10, 3)
ops.algorithm('ModifiedNewton', '-initial')
ops.integrator('LoadControl', 0.1)
ops.analysis('Static')
ops.analyze(10)

# --------------------------------------------------
# 1. Define the load pattern ONCE. Do not delete it.
# --------------------------------------------------
ops.loadConst('-time', 0.0)
ops.pattern('Plain', 2, 1)
# Define your reference load profile (6 DOFs: Fx Fy Fz Mx My Mz)
#x-direction
#ops.load(13, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
#ops.load(15, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
#ops.load(17, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
#y-direction – load all 6 second-floor nodes uniformly
ops.load(13, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
ops.load(14, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
ops.load(15, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
ops.load(16, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
ops.load(17, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
ops.load(18, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

# --------------------------------------------------
# 2. Initial Analysis Setup
# --------------------------------------------------
ops.system('UmfPack')
ops.constraints('Transformation')
ops.numberer('RCM')
ops.test('NormDispIncr', 1.0e-8, 100, 0)
ops.algorithm('Newton')
ops.analysis('Static')

# --------------------------------------------------
# 3. Adaptive pushover loop
# --------------------------------------------------
program = [159/7600]
disp = [0.0]
shear = [0.0]
currentDisp = 0.0

CTRL_NODE = 17
CTRL_DOF  = 2   # y-direction pushover
steps_per_phase = 500            # nominal step count (subdivided automatically on failure)
MIN_DU_FACTOR   = 1.0/64.0       # smallest sub-step = dU * this factor
TEST_TOL        = 1.0e-8
TEST_TOL_RELAX  = 1.0e-6
MAX_ITER        = 100


def _try_step(dU_try):
    """Attempt one DisplacementControl step of size dU_try with a fallback chain.
    Returns 0 on convergence, non-zero otherwise."""
    ops.integrator('DisplacementControl', CTRL_NODE, CTRL_DOF, dU_try)

    # Strategy chain: (algorithm_args, test_args)
    strategies = [
        (('Newton',),                       ('NormDispIncr', TEST_TOL,       MAX_ITER, 0)),
        (('ModifiedNewton',),               ('NormDispIncr', TEST_TOL,       MAX_ITER, 0)),
        (('Newton', '-initial'),            ('NormDispIncr', TEST_TOL,       MAX_ITER, 0)),
        (('KrylovNewton',),                 ('NormDispIncr', TEST_TOL,       2*MAX_ITER, 0)),
        (('Broyden', 8),                    ('NormDispIncr', TEST_TOL,       2*MAX_ITER, 0)),
        (('NewtonLineSearch', 0.8),         ('NormDispIncr', TEST_TOL,       2*MAX_ITER, 0)),
        (('Newton',),                       ('NormDispIncr', TEST_TOL_RELAX, 4*MAX_ITER, 0)),
        (('KrylovNewton',),                 ('EnergyIncr',   TEST_TOL_RELAX, 4*MAX_ITER, 0)),
    ]
    for algo, test in strategies:
        ops.test(*test)
        ops.algorithm(*algo)
        ok = ops.analyze(1)
        if ok == 0:
            # restore default for next call
            ops.test('NormDispIncr', TEST_TOL, MAX_ITER, 0)
            ops.algorithm('Newton')
            return 0
    return -1


def _adaptive_step(dU_target):
    """Take one nominal step of size dU_target, recursively halving on failure.
    Returns total displacement increment actually achieved."""
    stack = [dU_target]
    achieved = 0.0
    while stack:
        dU_try = stack[-1]
        ok = _try_step(dU_try)
        if ok == 0:
            achieved += dU_try
            stack.pop()
        else:
            # halve and retry
            half = dU_try / 2.0
            if abs(half) < abs(dU_target * MIN_DU_FACTOR):
                print(f"  ! sub-step {dU_try:.2e} failed below MIN_DU; aborting phase")
                return achieved, False
            print(f"  ! sub-step {dU_try:.2e} failed, halving to {half:.2e}")
            stack[-1] = half
            stack.append(half)  # take two halves to cover the original
    return achieved, True


# === PLASTIC HINGE TRACKING SETUP ===
# Model units: kN, m  →  E_steel = 210.0e6 kN/m²
# φ_y = (f_y / E) / (c)  where c = distance from NA to extreme bar
# Yield curvatures (φ_y) — equivalent to first-yield from a standalone M-κ analysis:
#   φ_y = ε_y / c  where  ε_y = f_y / E  and  c = distance from centroid to extreme bar
# Beams: D12 extreme bars → c = 500/2 - 25 - 12/2 = 219 mm
# Columns: D14 bars       → c = 300/2 - 25 - 14/2 = 118 mm
_phi_y_beam = (322.3e3 + 342.2e3) / 2.0 / (210.0e6 * (0.5/2 - 0.025 - 0.012/2))  # rad/m
_phi_y_col  = (334.1e3 + 348.1e3) / 2.0 / (210.0e6 * (0.3/2  - 0.025 - 0.014/2))  # rad/m

_elem_nodes = {
    # Section 1 – y-beams support thirds
    1:(7,25), 2:(26,9), 3:(9,27), 4:(28,11), 5:(8,29), 6:(30,10), 7:(10,31), 8:(32,12),
    9:(13,39), 10:(40,15), 11:(15,41), 12:(42,17), 13:(14,43), 14:(44,16), 15:(16,45), 16:(46,18),
    # Section 2 – y-beams midspan thirds
    17:(25,26), 18:(27,28), 19:(29,30), 20:(31,32), 21:(39,40), 22:(41,42), 23:(43,44), 24:(45,46),
    # Section 3 – x-beams 1F support thirds
    25:(7,19), 26:(20,8), 27:(9,21), 28:(22,10), 29:(11,23), 30:(24,12),
    # Section 4 – x-beams 1F midspan thirds
    31:(19,20), 32:(21,22), 33:(23,24),
    # Section 5 – x-beams 2F support thirds
    34:(13,33), 35:(34,14), 36:(15,35), 37:(36,16), 38:(17,37), 39:(38,18),
    # Section 6 – x-beams 2F midspan thirds
    40:(33,34), 41:(35,36), 42:(37,38),
    # Section 7 – columns 1st storey
    43:(1,7), 44:(3,9), 45:(5,11), 46:(2,8), 47:(4,10), 48:(6,12),
    # Section 8 – columns 2nd storey
    49:(7,13), 50:(9,15), 51:(11,17), 52:(8,14), 53:(10,16), 54:(12,18),
}
_col_eles   = set(range(43, 55))
_n_int_pts  = 5

_node_xyz = {
    1: (0.0, 0.0, 0.0),  2: (4.7, 0.0, 0.0),  3: (0.0, 2.85, 0.0),  4: (4.7, 2.85, 0.0),
    5: (0.0, 5.7, 0.0),  6: (4.7, 5.7, 0.0),
    7: (0.0, 0.0, 4.3),  8: (4.7, 0.0, 4.3),  9: (0.0, 2.85, 4.3),  10:(4.7, 2.85, 4.3),
    11:(0.0, 5.7, 4.3),  12:(4.7, 5.7, 4.3),
    13:(0.0, 0.0, 7.6),  14:(4.7, 0.0, 7.6),  15:(0.0, 2.85, 7.6),  16:(4.7, 2.85, 7.6),
    17:(0.0, 5.7, 7.6),  18:(4.7, 5.7, 7.6),
    19:(4.7/3, 0.0, 4.3),        20:(2*4.7/3, 0.0, 4.3),
    21:(4.7/3, 2.85, 4.3),       22:(2*4.7/3, 2.85, 4.3),
    23:(4.7/3, 5.7, 4.3),        24:(2*4.7/3, 5.7, 4.3),
    25:(0.0, 2.85/3, 4.3),       26:(0.0, 2*2.85/3, 4.3),
    27:(0.0, 2.85+2.85/3, 4.3),  28:(0.0, 2.85+2*2.85/3, 4.3),
    29:(4.7, 2.85/3, 4.3),       30:(4.7, 2*2.85/3, 4.3),
    31:(4.7, 2.85+2.85/3, 4.3),  32:(4.7, 2.85+2*2.85/3, 4.3),
    33:(4.7/3, 0.0, 7.6),        34:(2*4.7/3, 0.0, 7.6),
    35:(4.7/3, 2.85, 7.6),       36:(2*4.7/3, 2.85, 7.6),
    37:(4.7/3, 5.7, 7.6),        38:(2*4.7/3, 5.7, 7.6),
    39:(0.0, 2.85/3, 7.6),       40:(0.0, 2*2.85/3, 7.6),
    41:(0.0, 2.85+2.85/3, 7.6),  42:(0.0, 2.85+2*2.85/3, 7.6),
    43:(4.7, 2.85/3, 7.6),       44:(4.7, 2*2.85/3, 7.6),
    45:(4.7, 2.85+2.85/3, 7.6),  46:(4.7, 2.85+2*2.85/3, 7.6),
}

_snapshot_interval  = max(1, steps_per_phase // 5)

# Element lengths (m) from undeformed node coordinates.
# Used for plastic rotation: θ_p = φ_p × (w₁ × L) = φ_p × 0.1 × L
# where w₁ = 0.1 is the Gauss-Lobatto end-point weight for a 5-point scheme.
_elem_lengths = {}
for _et, (_ni, _nj) in _elem_nodes.items():
    _xi, _yi, _zi = _node_xyz[_ni]
    _xj, _yj, _zj = _node_xyz[_nj]
    _elem_lengths[_et] = math.sqrt((_xj - _xi)**2 + (_yj - _yi)**2 + (_zj - _zi)**2)

_total_pushover_steps = steps_per_phase * len(program)
_snapshot_steps     = set(range(_snapshot_interval, _total_pushover_steps + 1, _snapshot_interval))
hinge_snapshots     = []
_step_counter       = 0


for i, pct in enumerate(program):
    maxU = pct * 7.6                       # drift × building height
    delta_disp = maxU - currentDisp
    dU_nominal = delta_disp / steps_per_phase

    print(f"Pushing to {maxU:.4f} m (dU_nominal = {dU_nominal*1000:.3f} mm)...")

    phase_ok = True
    for step in range(steps_per_phase):
        inc, ok = _adaptive_step(dU_nominal)

        ops.reactions()
        currentDisp = (ops.nodeDisp(13, 2) + ops.nodeDisp(15, 2) + ops.nodeDisp(17, 2)) / 3
        V = -(ops.nodeReaction(1, 2) + ops.nodeReaction(2, 2) + ops.nodeReaction(3, 2)
              + ops.nodeReaction(4, 2) + ops.nodeReaction(5, 2) + ops.nodeReaction(6, 2))
        disp.append(currentDisp * 1000)
        shear.append(V)

        # --- snapshot for plastic hinge visualisation ---
        _step_counter += 1
        if _step_counter in _snapshot_steps:
            _snap_curvs = {}
            for _et in _elem_nodes:
                _sec_curvs = {}
                for _sn in range(1, _n_int_pts + 1):
                    try:
                        _def = ops.eleResponse(_et, 'section', _sn, 'deformation')
                        # resultant curvature from all bending components (indices 1+)
                        _sec_curvs[_sn] = math.sqrt(sum(_def[k]**2 for k in range(1, len(_def))))
                    except Exception:
                        _sec_curvs[_sn] = 0.0
                _snap_curvs[_et] = _sec_curvs
            hinge_snapshots.append({
                'step': _step_counter,
                'disp': currentDisp * 1000,
                'shear': V,
                'curvatures': _snap_curvs,
            })

        if not ok:
            print(f"  -> stalled at step {step}, u = {currentDisp*1000:.3f} mm")
            phase_ok = False
            break

        if step % 25 == 0:
            print(f"  step {step:4d}: u = {currentDisp*1000:7.3f} mm,  V = {V:8.3f} kN")

    if not phase_ok:
        break

print("Pushover Analysis Complete!")

# ============================================================
# PROGRESSIVE PLASTIC HINGE FORMATION  — 3D ISOMETRIC VIEW
# ============================================================
def _plot_hinge_frame_3d(ax, snap, n_pts):
    """Draw 3D isometric frame with colour-coded hinge markers."""
    # --- structural lines ---
    for et, (ni, nj) in _elem_nodes.items():
        xi, yi, zi = _node_xyz[ni]
        xj, yj, zj = _node_xyz[nj]
        ax.plot([xi, xj], [yi, yj], [zi, zj], 'k-', linewidth=1.2, zorder=1)

    # --- fixed-base markers ---
    for bn in [1, 2, 3, 4, 5, 6]:
        bx, by, bz = _node_xyz[bn]
        ax.scatter([bx], [by], [bz], marker='^', s=55, c='k', zorder=4)

    # --- hinge markers ---
    # Plastic rotation: θ_p = φ_p × (w₁ × L) = φ_p × 0.1 × L  (Lobatto end-point weight = 0.1)
    # φ_p = max(0, φ_total − φ_y)  (plastic curvature, positive only after yielding)
    # Thresholds:
    #   gold       :  0 < θ_p ≤  5 mrad  (onset of yielding)
    #   darkorange :  5 < θ_p ≤ 10 mrad  (moderate yielding)
    #   red        :       θ_p > 10 mrad  (significant plastic hinge)
    off = 0.10
    for et, (ni, nj) in _elem_nodes.items():
        phi_y = _phi_y_col if et in _col_eles else _phi_y_beam
        L = _elem_lengths[et]
        xi, yi, zi = _node_xyz[ni]
        xj, yj, zj = _node_xyz[nj]
        dx, dy, dz = xj - xi, yj - yi, zj - zi
        for sec_num, is_i in [(1, True), (n_pts, False)]:
            kappa   = snap['curvatures'][et][sec_num]
            phi_p   = max(0.0, kappa - phi_y)   # plastic curvature
            theta_p = phi_p * 0.1 * L           # plastic rotation (Lobatto w₁ = 0.1)
            if theta_p <= 0.0:
                continue
            if is_i:
                hx, hy, hz = xi + off*dx, yi + off*dy, zi + off*dz
            else:
                hx, hy, hz = xj - off*dx, yj - off*dy, zj - off*dz
            color = 'gold' if theta_p < 0.005 else ('darkorange' if theta_p < 0.010 else 'red')
            size  = 50    if theta_p < 0.005 else (90             if theta_p < 0.010 else 130)
            ax.scatter([hx], [hy], [hz], c=color, s=size,
                       edgecolors='black', linewidths=0.8, zorder=5)


if hinge_snapshots:
    n_snaps = len(hinge_snapshots)
    fig_h   = plt.figure(figsize=(3.0 * n_snaps, 6.5))
    for idx, snap in enumerate(hinge_snapshots):
        ax3d = fig_h.add_subplot(1, n_snaps, idx + 1, projection='3d')
        pct  = (snap['step'] / _total_pushover_steps) * 100
        title = (f"{pct:.0f}% Pushover\nStep {snap['step']}/{_total_pushover_steps}\n"
                 f"\u0394 = {snap['disp']:.1f} mm\nV = {snap['shear']:.2f} kN")
        _plot_hinge_frame_3d(ax3d, snap, _n_int_pts)
        ax3d.set_title(title, fontsize=7.5)
        ax3d.set_xlabel('x (m)', fontsize=6, labelpad=1)
        ax3d.set_ylabel('y (m)', fontsize=6, labelpad=1)
        ax3d.set_zlabel('z (m)', fontsize=6, labelpad=1)
        ax3d.tick_params(labelsize=5)
        ax3d.set_box_aspect([4.7, 5.7, 7.6])
        ax3d.view_init(elev=22, azim=-50)

    _legend_patches = [
        mpatches.Patch(facecolor='gold',       edgecolor='black', label='Onset of yielding (0 < \u03b8p \u2264 5 mrad)'),
        mpatches.Patch(facecolor='darkorange', edgecolor='black', label='Moderate yielding (5 < \u03b8p \u2264 10 mrad)'),
        mpatches.Patch(facecolor='red',        edgecolor='black', label='Plastic hinge (\u03b8p > 10 mrad)'),
    ]
    fig_h.legend(handles=_legend_patches, loc='lower center', ncol=3,
                 fontsize=8.5, bbox_to_anchor=(0.5, 0.0), framealpha=0.9)
    fig_h.suptitle("Progressive Plastic Hinge Formation — Di Sarno (2012)",
                   fontsize=11, fontweight='bold')
    fig_h.tight_layout(rect=[0, 0.09, 1, 0.96])
    fig_h.show()

x = [0,	3.43096234309621,	4.76987447698743,	8.61924686192468,	12.6359832635983,	16.4853556485356,	27.0292887029289,	34.8953974895398,	39.9163179916318,	41.7573221757323,	44.6025104602511,	47.9497907949791,	56.1506276150628,	63.8493723849373,	156.234309623431
]
y = [0,	33.4562211981567,	42.4884792626728,	58.7096774193549,	70.1382488479263,	79.3548387096774,	98.3410138248848,	109.032258064516,	114.746543778802,	114.930875576037,	118.433179723502,	118.433179723502,	123.225806451613,	123.594470046083,	115.852534562212
]

fig, ax = plt.subplots()
ax.plot(x, y, label="Experimental", linewidth=2, color='blue', marker='o', linestyle='--')
ax.plot(disp, shear, label="OpenSeesPy", linewidth=3, color='red')
ax.set_xlabel("Roof displacement (mm)")
ax.set_ylabel("Base shear (kN)")
# ax.set_xlim(-0.1, 0.1)
# ax.set_ylim(-60, 60)
ax.axhline(0, color='black')
ax.axvline(0, color='black')
ax.legend()
ax.grid()
ax.set_title("Di Sarno (2012) Pushover Curve")
fig.show()
# %%
