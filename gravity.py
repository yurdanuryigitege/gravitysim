import math
import numpy as np
from matplotlib import pyplot as plt

time = 0
class Particle:
    def __init__(self,mass,radius,position,velocity,acceleration):
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = velocity
        self.acceleration = acceleration
    def positionupdate(self,velocity):
        self.position = np.array([(self.position[0]+velocity[0]*time),(self.position[1]+velocity[1])])

#generatordan nasıl particle çekebileceğimi bulamadım 

def generator():
    counter = int(input("how much particles "))
    particles = []  
    for i in range(counter):
        
        name = input("particle name ")
        mass = int(input("particle mass "))
        radius = int(input("particle radius "))
        position = list(input("particle position ")) # list string olarak alınıyor bunu intlerden oluşacak şekild değiştirmeliyim
        velocity = 0
        acceleration = 0
        name = Particle(mass, radius, position, velocity, acceleration)
        particles.append(name)
    return particles 

   



class Force:
    def __init__(self,mass_1,mass_2,radius_1,radius_2):
        self.mass_1 = mass_1
        self.mass_2 = mass_2
        self.radius_1 = radius_1
        self.radius_2 = radius_2        
    def forceapplied(self):
        
        if self.mass_1 < self.mass_2:
            force_x = (self.mass_1 * self.mass_2)/(self.radius_1**2)
            force_y = (self.mass_1 *self.mass_2)/(self.radius_2**2)
        else:
            force_x = -(self.mass_2 * self.mass_1)/(self.radius_1**2)
            force_y = -(self.mass_2 *self.mass_1)/(self.radius_2**2)
        
        force = np.array([force_x,force_y])
        return force 
    
    
    
    
    
class PositionChange:
    def __init__ (self,mass,force_x,force_y,time):
        self.mass = mass
        self.force_x = force_x
        self.force_y = force_y
        self.time = time 
        
    def acceleration(self):
        acceleration_x = self.force_x / self.mass
        acceleration_y = self.force_y /self.mass
        acceleration = np.array([acceleration_x,acceleration_y])
        return acceleration
    
    
    
  
def velocity(acceleration,time):
    velocity_x = time * acceleration[0]
    velocity_y = time * acceleration[1]
    velocity_t = np.array([velocity_x,velocity_y])
    return velocity_t
    
def distancebetween(pos1,pos2):
    distance_x = math.sqrt(((pos1[0]-pos2[0])**2))
    distance_y = math.sqrt(((pos1[1]-pos2[1])**2))
    distance_t = np.array([distance_x,distance_y])
    return distance_t



planet_1 = Particle(9,10,[0,5],0,0)
planet_2 = Particle(10,10,[10,0],0,0)

planet_1_position_log_x = np.array([planet_1.position[0]])
planet_1_position_log_y = np.array([planet_1.position[1]])
planet_2_position_log_x = np.array([planet_2.position[0]])
planet_2_position_log_y = np.array([planet_2.position[1]])

array = np.array([])


while time < 10:
    time += 1
    planet_1_to_2_force_object = Force(planet_1.mass, planet_2.mass,distancebetween(planet_1.position, planet_2.position)[0],distancebetween(planet_1.position, planet_2.position)[1] )
    planet_2_to_1_force_object = Force(planet_2.mass, planet_1.mass,distancebetween(planet_2.position, planet_1.position)[0],distancebetween(planet_2.position, planet_1.position)[1] )
    planet_1_to_2_force = planet_1_to_2_force_object.forceapplied()
    planet_2_to_1_force = planet_2_to_1_force_object.forceapplied()
    planet_1_acceleration_object = PositionChange(planet_1.mass, planet_2_to_1_force[0], planet_2_to_1_force[1], time)
    planet_2_acceleration_object = PositionChange(planet_2.mass, planet_1_to_2_force[0], planet_1_to_2_force[1], time)
    planet_1_acceleration = planet_1_acceleration_object.acceleration()
    planet_2_acceleration = planet_2_acceleration_object.acceleration()
    planet_1_velocity = velocity(planet_1_acceleration,time)
    planet_2_velocity = velocity(planet_2_acceleration,time)
    planet_1.positionupdate(planet_1_velocity)
    planet_2.positionupdate(planet_2_velocity)
    np.append(array,time) 
    planet_1_position_log_x = np.append(planet_1_position_log_x, planet_1.position[0])
    planet_1_position_log_y =np.append(planet_1_position_log_y, planet_1.position[1])
    planet_2_position_log_x = np.append(planet_2_position_log_x, planet_1.position[0])
    planet_2_position_log_y =np.append(planet_2_position_log_y, planet_1.position[1])
    array = np.append(array,time)


plt.plot(planet_1_position_log_x, planet_1_position_log_y)
plt.plot(planet_2_position_log_x, planet_2_position_log_y)

plt.show()

