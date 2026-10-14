import math
import numpy as np

v = 2.0
L = 2.5
delta = math.radians(20)
dt = 0.1

def update_state(q, v, delta, L, dt):
    x, y, theta = q

    return np.array([
        x + v * math.cos(theta) * dt,
        y + v * math.sin(theta) * dt,
        theta + (v / L) * math.tan(delta) * dt
    ])


q = np.array([0.0, 0.0, 0.0])

for _ in range(50):
    q = update_state(q, v, delta, L, dt)

print(q)