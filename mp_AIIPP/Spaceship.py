'''
Created on Aug 20, 2014

@author: victorzhao
'''

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# presets for controlling keys
accel_val = 10
angle_vel = 0.1
missile_accel_val = 5
#control_keys_methods = {'up' : ship_accelerate, 'left' : ship_turn, 'right' : ship_turn}
control_values = {'up' : accel_val, 'left' : -angle_vel, 'right' : angle_vel}

c = 0.02 
rock_ang_vel_level_range = 5
rock_hori_vel_level_range = 5
rock_verti_vel_level_range = 5


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
# boosting ship image
ship_info_thrust = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            ship_thrust_sound.play()
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)     
        else:
            ship_thrust_sound.rewind()
            ship_thrust_sound.pause()
            
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.vel[0] + self.pos[0]) % WIDTH
        self.pos[1] = (self.vel[1] + self.pos[1]) % HEIGHT 
        self.angle += self.angle_vel
        if self.thrust != True: 
            self.vel[0] *= (1 - c)
            self.vel[1] *= (1 - c)
        
    def ship_turn(self, angle_vel):
        """ Control the orientation """
        self.angle_vel = angle_vel;    
    
    def ship_accelerate(self, accel_val):
        """ Controle the acceleration """
        # Flag of thruster
        if accel_val > 0:
            self.thrust = True
        else:
            self.thrust = False
        forward = angle_to_vector(self.angle)
        self.vel[0] += accel_val * forward[0]
        self.vel[1] += accel_val * forward[1]
     
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)        
        pos_missile = [(self.pos[0] + 45 * forward[0]) % WIDTH, (self.pos[1] + 45 * forward[1]) % HEIGHT]  
        missile_vel = [self.vel[0] + missile_accel_val * forward[0], self.vel[1] + missile_accel_val * forward[1]]
        a_missile = Sprite(pos_missile, missile_vel, 0, 0, missile_image, missile_info, missile_sound)

    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.vel[0] + self.pos[0]) % WIDTH
        self.pos[1] = (self.vel[1] + self.pos[1]) % HEIGHT 
        self.angle += self.angle_vel        


def key_down_handler(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.ship_accelerate(accel_val)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.ship_turn(-angle_vel)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.ship_turn(angle_vel)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    else:
        pass
    
def key_up_handler(key):  
    if key == simplegui.KEY_MAP['up']:
        my_ship.ship_accelerate(0)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.ship_turn(0)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.ship_turn(0)
    else:
        pass
    
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and lives
    canvas.draw_text('Score:'+ str(score), (WIDTH * 0.8, HEIGHT * 0.1), 20, 'White', 'serif')
    canvas.draw_text('Lives:' + str(lives), (WIDTH * 0.1, HEIGHT * 0.1), 20, 'White', 'serif')
    
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    rand_direction = random.choice([1, -1])
    rand_pos_rock = [random.randrange(0, WIDTH) % WIDTH, random.randrange(0, HEIGHT) % HEIGHT]
    rand_vel_rock = [random.randrange(0, rock_hori_vel_level_range) * rand_direction, random.randrange(0, rock_hori_vel_level_range) * rand_direction]
    rand_ang_vel = random.randrange(0, rock_ang_vel_level_range) / 10.0 * rand_direction
    a_rock = Sprite(rand_pos_rock, rand_vel_rock, 0, rand_ang_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
a_missile = Sprite([(my_ship.pos[0] + 45) % WIDTH, (my_ship.pos[1]) % HEIGHT], [0, 0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
