# %%
# Model #1: Jayaramappa (2015)

import openseespy.opensees as ops
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import opsvis as opsv
import math

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

# Main nodes
ops.node(1, 0, 0)
ops.node(2, 0, 1)
ops.node(3, 0, 2)
ops.node(4, 1, 0)
ops.node(5, 1, 1)
ops.node(6, 1, 2)

ops.fix(1, 1, 1, 1)
ops.fix(4, 1, 1, 1)

# Columns
# ops.uniaxialMaterial('Concrete02', 1, 20e3, 0.002, 0.0038, 4700e3 * math.sqrt(20), 0.62e3 * math.sqrt(20), 0.62/4700, 0.1)
ops.uniaxialMaterial('Concrete02', 11, -28.3e3, -0.002, -28.3e3 * 0.2, -0.0038, 0.1, 0.62e3 * math.sqrt(28.3), 0.05 * 4700e3 * math.sqrt(28.3))
ops.uniaxialMaterial('Steel02', 12, 456e3, 210.0e6, 0.18, 18.0, 0.925, 0.15)

# Minmax material
ops.uniaxialMaterial('MinMax', 1, 11, '-min', -0.01)
ops.uniaxialMaterial('MinMax', 2, 12, '-min', -0.1, '-max', 0.1)

# CROSS-SECTIONS
c_x = 100e-3
c_y = 70e-3
cc_col = 20e-3
d_b = 8e-3
column = [
    ['section', 'Fiber', 1, '-GJ', 1],
    ['patch', 'rect', 1, 30, 3, -c_x/2, c_y/2 - cc_col, c_x/2, c_y/2],
    ['patch', 'rect', 1, 30, 3, -c_x/2, -c_y/2, c_x/2, -c_y/2 + cc_col],
    ['patch', 'rect', 1, 8, 24, -c_x/2, -c_y/2 + cc_col, -c_x/2 + cc_col, c_y/2 - cc_col],
    ['patch', 'rect', 1, 8, 24, c_x/2 - cc_col, -c_y/2 + cc_col, c_x/2, c_y/2 - cc_col],
    ['patch', 'rect', 1, 24, 24, -c_x/2 + cc_col, -c_y/2 + cc_col, c_x/2 - cc_col, c_y/2 - cc_col],
    ['layer', 'straight', 2, 2, math.pi/4 * d_b**2, -c_x/2 + cc_col, c_y/2 - cc_col, c_x/2 - cc_col, c_y/2 - cc_col],
    ['layer', 'straight', 2, 2, math.pi/4 * d_b**2, -c_x/2 + cc_col, -c_y/2 + cc_col, c_x/2 - cc_col, -c_y/2 + cc_col],
]
opsv.plot_fiber_section(column)
opsv.fib_sec_list_to_cmds(column)

# Columns
# ops.geomTransf('PDelta', 1, 0, -1, 0, '-jntOffset', 0, 0.1/2, 0, -0.07/2)
# ops.geomTransf('PDelta', 1, '-jntOffset', 0, 0.1/2, 0, -0.07/2)
ops.geomTransf('PDelta', 1)
ops.beamIntegration('Lobatto', 1, 1, 5)
ops.element('forceBeamColumn', 1, 1, 2, 1, 1)
ops.element('forceBeamColumn', 2, 2, 3, 1, 1)
ops.element('forceBeamColumn', 3, 4, 5, 1, 1)
ops.element('forceBeamColumn', 4, 5, 6, 1, 1)

# Beams
# ops.geomTransf('PDelta', 2, -1, 0, 0, '-jntOffset', 0.1/2, 0, -0.1/2, 0)
ops.geomTransf('PDelta', 2, '-jntOffset', 0.1/2, 0, -0.1/2, 0)
ops.beamIntegration('Lobatto', 2, 1, 5)
ops.element('forceBeamColumn', 5, 2, 5, 2, 2)
ops.element('forceBeamColumn', 6, 3, 6, 2, 2)

opsv.plot_model()

# LOADS
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

# Apply self-weight (Gravity) BEFORE pushover
# Concrete density approx 24 kN/m^3. Section area = 100mm x 70mm = 0.007 m^2
# w = 24 * 0.007 = 0.168 kN/m
# Beams (elements 5, 6): horizontal, local y is vertical.
ops.eleLoad('-ele', 5, 6, '-type', '-beamUniform', -0.168)
# Columns (elements 1, 2, 3, 4): vertical, local x is vertical (upwards).
ops.eleLoad('-ele', 1, 2, 3, 4, '-type', '-beamUniform', 0.0, -0.168)

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
# Define your reference load profile
ops.load(6, 2.5/2, 0.0, 0.0)
ops.load(5, 2.5/2, 0.0, 0.0)

# --------------------------------------------------
# 2. Initial Analysis Setup
# --------------------------------------------------
ops.system('UmfPack')
ops.constraints('Transformation')
ops.numberer('RCM')
ops.test('NormDispIncr', 1.0e-8, 100, 0) # Slightly relaxed tolerance for RC
ops.algorithm('Newton')
ops.analysis('Static')

# --------------------------------------------------
# 3. The Corrected Cyclic Loop
# --------------------------------------------------
# program = [0.002, -0.002, 0.002, -0.002, 0.002, -0.002, 0.006, -0.006, 0.006, -0.006, 0.006, -0.006, 0.012, -0.012, 0.012, -0.012, 0.012, -0.012, 0.016, -0.016]
program = [61.93/2000]
disp = [0.0]
shear = [0.0]
currentDisp = 0.0

steps_per_phase = 50 # How many steps to take to reach each peak

# === PLASTIC HINGE TRACKING SETUP ===
# Reference node coordinates (undeformed geometry)
node_coords_ref = {
    1: [0.0, 0.0], 2: [0.0, 1.0], 3: [0.0, 2.0],
    4: [1.0, 0.0], 5: [1.0, 1.0], 6: [1.0, 2.0],
}
# Element connectivity and type
elem_info = {
    1: {'nodes': (1, 2), 'type': 'column'},
    2: {'nodes': (2, 3), 'type': 'column'},
    3: {'nodes': (4, 5), 'type': 'column'},
    4: {'nodes': (5, 6), 'type': 'column'},
    5: {'nodes': (2, 5), 'type': 'beam'},
    6: {'nodes': (3, 6), 'type': 'beam'},
}
# Yield curvature (φ_y) — equivalent to first-yield from a standalone M-κ analysis:
#   ε_y = f_y / E  (yield strain of extreme tension steel reaching f_y)
#   c   = c_y/2 - cc_col  (distance from section centroid to extreme bar centre)
#   φ_y = ε_y / c   (curvature at which extreme steel first reaches yield)
_eps_y  = 456e3 / 210.0e6              # yield strain ~ 0.00217
_c_steel = c_y / 2.0 - cc_col         # 0.035 - 0.020 = 0.015 m
phi_y = _eps_y / _c_steel             # ~ 0.145 rad/m

# Element lengths (m) from undeformed node coordinates.
# Used for plastic rotation: θ_p = φ_p × (w₁ × L)
# where w₁ = 0.1 is the Gauss-Lobatto end-point weight for a 5-point scheme.
elem_lengths = {}
for _et, _info in elem_info.items():
    _in, _jn = _info['nodes']
    _xi, _yi = node_coords_ref[_in]
    _xj, _yj = node_coords_ref[_jn]
    elem_lengths[_et] = math.sqrt((_xj - _xi)**2 + (_yj - _yi)**2)

n_int_pts = 5  # Lobatto integration points per element
# Take 5 equally-spaced snapshots across the full pushover
snapshot_interval = max(1, steps_per_phase // 5)
snapshot_steps_set = set(
    range(snapshot_interval, steps_per_phase * len(program) + 1, snapshot_interval)
)
hinge_snapshots = []
step_counter = 0

for i, pct in enumerate(program):
    # Calculate target displacement for this peak
    maxU = pct * 2 * 1

    # Calculate the exact displacement increment needed per step
    delta_disp = maxU - currentDisp
    dU = delta_disp / steps_per_phase

    # Update the integrator.
    # OpenSees will figure out whether the loads need to be positive or negative!
    ops.integrator('DisplacementControl',6, 1, dU)

    print(f"Pushing to {maxU:.4f} m...")

    # Take the required number of steps to exactly hit the target
    for step in range(steps_per_phase):
        ok = ops.analyze(1)

        # Robust convergence handling for RC frames
        if ok != 0:
            print(f"Failed at step {step}, trying Broyden...")
            ops.algorithm('Broyden', 8)
            ok = ops.analyze(1)
            ops.algorithm('Newton') # Switch back to Newton if it succeeds
            if ok != 0:
                print("Analysis completely failed. Terminating.")
                break

        # Record data
        ops.reactions()
        currentDisp = (ops.nodeDisp(3, 1) + ops.nodeDisp(6, 1))/2

        # Sum base shear from all fixed supports (Nodes 1, 2, 3, 4)
        V = -(ops.nodeReaction(1, 1) + ops.nodeReaction(4, 1))

        disp.append(currentDisp * 1000)
        shear.append(V)

        # --- Snapshot for plastic hinge visualisation ---
        step_counter += 1
        if step_counter in snapshot_steps_set:
            snap_curvs = {}
            for ele_tag in elem_info:
                sec_curvs = {}
                for sec_num in range(1, n_int_pts + 1):
                    deform = ops.eleResponse(ele_tag, 'section', sec_num, 'deformation')
                    sec_curvs[sec_num] = abs(deform[1])   # index 1 = curvature (index 0 = axial strain)
                snap_curvs[ele_tag] = sec_curvs
            hinge_snapshots.append({
                'step': step_counter,
                'disp': currentDisp * 1000,
                'shear': V,
                'curvatures': snap_curvs,
            })

        print(rf"current displacement: {currentDisp:.4f} m, base shear: {V:.4f} kN")

    if ok != 0:
        break # Exit the main loop if convergence failed entirely

print("Cyclic Analysis Complete!")

# ============================================================
# PROGRESSIVE PLASTIC HINGE FORMATION VISUALISATION
# ============================================================

def _plot_hinge_frame(ax, node_coords, elem_info, curvatures, phi_y, elem_lengths, n_pts, title_str):
    """Draw the frame with colour-coded plastic hinge markers for one snapshot."""
    # --- frame lines ---
    for ele_tag, info in elem_info.items():
        i_n, j_n = info['nodes']
        xi, yi = node_coords[i_n]
        xj, yj = node_coords[j_n]
        ax.plot([xi, xj], [yi, yj], 'k-', linewidth=2.5, zorder=1)

    # --- fixed-base symbols (filled triangles + baseline) ---
    for base_node in [1, 4]:
        bx, by = node_coords[base_node]
        tri_x = [bx - 0.07, bx + 0.07, bx, bx - 0.07]
        tri_y = [by - 0.10, by - 0.10, by, by - 0.10]
        ax.fill(tri_x, tri_y, 'k', zorder=3)
        ax.plot([bx - 0.10, bx + 0.10], [by - 0.10, by - 0.10], 'k-', linewidth=2, zorder=3)

    # --- free nodes ---
    for node_tag, (nx, ny) in node_coords.items():
        if node_tag not in [1, 4]:
            ax.plot(nx, ny, 'ko', markersize=5, zorder=3)

    # --- hinge indicators ---
    #   Section 1  -> i-end of element
    #   Section n  -> j-end of element
    #   Marker is offset 8% of element length inward so it doesn't
    #   overlap the joint when multiple elements meet at the same node.
    #
    # Plastic rotation at each end IP:
    #   φ_p     = max(0, φ_total − φ_y)          (plastic curvature)
    #   θ_p     = φ_p × (w₁ × L) = φ_p × 0.1 × L (plastic rotation, Lobatto w₁=0.1)
    #
    # Colour thresholds:
    #   gold       :  0 < θ_p ≤  5 mrad  (onset of yielding)
    #   darkorange :  5 < θ_p ≤ 10 mrad  (moderate yielding)
    #   red        :      θ_p > 10 mrad  (significant plastic hinge)
    end_offset = 0.08
    for ele_tag, info in elem_info.items():
        i_n, j_n = info['nodes']
        xi, yi = node_coords[i_n]
        xj, yj = node_coords[j_n]
        L = elem_lengths[ele_tag]
        for sec_num, end_label in [(1, 'i'), (n_pts, 'j')]:
            kappa   = curvatures[ele_tag][sec_num]
            phi_p   = max(0.0, kappa - phi_y)   # plastic curvature
            theta_p = phi_p * 0.1 * L           # plastic rotation (Lobatto w₁ = 0.1)
            if theta_p <= 0.0:
                continue  # still elastic – no marker
            if end_label == 'i':
                hx = xi + end_offset * (xj - xi)
                hy = yi + end_offset * (yj - yi)
            else:
                hx = xj + end_offset * (xi - xj)
                hy = yj + end_offset * (yi - yj)
            # colour and size scale with plastic rotation magnitude
            if theta_p < 0.005:
                color, ms = 'gold', 10
            elif theta_p < 0.010:
                color, ms = 'darkorange', 13
            else:
                color, ms = 'red', 16
            ax.plot(hx, hy, 'o', markersize=ms, color=color,
                    markeredgecolor='black', markeredgewidth=1.2, zorder=5)

    ax.set_title(title_str, fontsize=8.5)
    ax.set_aspect('equal')
    ax.set_xlim(-0.30, 1.30)
    ax.set_ylim(-0.30, 2.45)
    ax.axis('off')


if hinge_snapshots:
    n_snaps = len(hinge_snapshots)
    fig_h, axes = plt.subplots(1, n_snaps, figsize=(2.8 * n_snaps, 5.8))
    if n_snaps == 1:
        axes = [axes]

    total_steps = steps_per_phase * len(program)
    for idx, snap in enumerate(hinge_snapshots):
        pct = (snap['step'] / total_steps) * 100
        title = (
            f"{pct:.0f}% Pushover\n"
            f"Step {snap['step']} / {total_steps}\n"
            f"\u0394 = {snap['disp']:.1f} mm\n"
            f"V = {snap['shear']:.2f} kN"
        )
        _plot_hinge_frame(
            axes[idx], node_coords_ref, elem_info,
            snap['curvatures'], phi_y, elem_lengths, n_int_pts, title
        )

    legend_patches = [
        mpatches.Patch(facecolor='gold',       edgecolor='black', label='Onset of yielding  (0 < \u03b8p \u2264 5 mrad)'),
        mpatches.Patch(facecolor='darkorange', edgecolor='black', label='Moderate yielding  (5 < \u03b8p \u2264 10 mrad)'),
        mpatches.Patch(facecolor='red',        edgecolor='black', label='Plastic hinge       (\u03b8p > 10 mrad)'),
    ]
    fig_h.legend(handles=legend_patches, loc='lower center', ncol=3,
                 fontsize=8.5, bbox_to_anchor=(0.5, 0.0), framealpha=0.9)
    fig_h.tight_layout(rect=[0, 0.09, 1, 0.96])
    fig_h.show()

x = [0.1191544098979378, 1.1861279894385852, 6.1317130138957054, 19.66386270162314, 31.287510789905724, 54.423776720884184, 61.955215544234385]
y = [0.01370452589135951, 2.5106464911883295, 7.500566302722783, 12.004032075386219, 14.985729171385856, 20.461536719068548, 22.45503556381099]

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
ax.set_title("Jayaramappa (2015) Pushover Curve")
fig.show()
# %%
