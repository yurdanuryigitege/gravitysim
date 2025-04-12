import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Global time step
dt = 0.1

class Particle:
    def __init__(self, mass, radius, position, velocity, acceleration):
        self.mass = mass
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)

    def position_update(self, dt):
        self.position += self.velocity * dt

    def velocity_update(self, acceleration, dt):
        self.velocity += acceleration * dt

class Force:
    def __init__(self, mass_1, mass_2, position_1, position_2):
        self.mass_1 = mass_1
        self.mass_2 = mass_2
        self.position_1 = position_1
        self.position_2 = position_2

    def force_applied(self):
        r = self.position_2 - self.position_1
        distance = np.linalg.norm(r)
        if distance == 0:
            return np.array([0.0, 0.0])  # Avoid division by zero
        force_magnitude = (self.mass_1 * self.mass_2) / (distance ** 2)
        force_direction = r / distance
        return force_magnitude * force_direction

class PositionChange:
    def __init__(self, mass, force, dt):
        self.mass = mass
        self.force = force
        self.dt = dt

    def acceleration(self):
        return self.force / self.mass

# Initial planet setup
planet_1 = Particle(9, 10, [0, 5], [0, 0], [0, 0])
planet_2 = Particle(10, 10, [10, 0], [0, 0], [0, 0])

planet_1_position_log = [planet_1.position.copy()]
planet_2_position_log = [planet_2.position.copy()]

# Precompute positions for animation
time = 0
max_time = 10
while time < max_time:
    time += dt

    force_1_on_2 = Force(planet_1.mass, planet_2.mass, planet_1.position, planet_2.position).force_applied()
    force_2_on_1 = Force(planet_2.mass, planet_1.mass, planet_2.position, planet_1.position).force_applied()

    acc_1 = PositionChange(planet_1.mass, force_2_on_1, dt).acceleration()
    acc_2 = PositionChange(planet_2.mass, force_1_on_2, dt).acceleration()

    planet_1.velocity_update(acc_1, dt)
    planet_2.velocity_update(acc_2, dt)

    planet_1.position_update(dt)
    planet_2.position_update(dt)

    planet_1_position_log.append(planet_1.position.copy())
    planet_2_position_log.append(planet_2.position.copy())

# Convert logs to NumPy arrays
planet_1_position_log = np.array(planet_1_position_log)
planet_2_position_log = np.array(planet_2_position_log)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_title('Planetary Motion Simulation')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.grid(True)

line1, = ax.plot([], [], 'b-', label='Planet 1 Trail')
line2, = ax.plot([], [], 'r-', label='Planet 2 Trail')
point1, = ax.plot([], [], 'bo')  # Planet 1 current position
point2, = ax.plot([], [], 'ro')  # Planet 2 current position
ax.legend()

# Update function for animation
def update(frame):
    line1.set_data(planet_1_position_log[:frame, 0], planet_1_position_log[:frame, 1])
    line2.set_data(planet_2_position_log[:frame, 0], planet_2_position_log[:frame, 1])
    point1.set_data([planet_1_position_log[frame, 0]], [planet_1_position_log[frame, 1]])
    point2.set_data([planet_2_position_log[frame, 0]], [planet_2_position_log[frame, 1]])
    return line1, line2, point1, point2


# Create animation
ani = FuncAnimation(fig, update, frames=len(planet_1_position_log), interval=50, blit=True)

plt.show()
