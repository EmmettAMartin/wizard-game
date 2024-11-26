import nebulatk as ntk
from time import sleep
from math import sqrt

class Projectile:
  """
  Projectile class, which defines the movements and trajectories of projectiles.
  """
  def __init__(self, root, target, image, position_x, position_y, speed = 3, projectile_range=500, damage=0, check=None):
    self.image = image
    self.position_x = position_x # position of projectile
    self.position_y = position_y

    self.target = target # target of projectile
    self.target_x = target.curr_x # initial position of the target
    self.target_y = target.curr_y
    self.damage = damage # damage of projectile
    self.check = check # function to check if projectile hit anything

    self.projectile_range = projectile_range # range of projectile
    self.root = root # Root widget for the projectile widget
    self.is_undefined_string = "undefined"
    if self.image:
      self.frame = ntk.Label(self.root, width=10, height=10, image=self.image).place(x = self.position_x, y = self.position_y)
    else:
      self.frame = ntk.Label(self.root, width=10, height=10, image="0.png").place(x = self.position_x, y = self.position_y)
    self.distance_covered = 0
    self.original_position_x = position_x
    self.original_position_y = position_y
    self.static_inc = 0

    self.speed = speed
    self.y_offset = self.target_y - self.original_position_y
    self.x_offset = self.target_x - self.original_position_x
    self.lifetime = 1/self.projectile_range
    
    # logic to solve divide by zeros
    if self.x_offset > 0:
      self.direction = 1 
    elif self.x_offset < 0:
      self.direction = -1
    else:
      self.direction = -1 if self.y_offset >= 0 else 1
    
    if self.x_offset == 0:
      self.angle = 100000 # if the player is directly above or below the target, just shoot at a really high angle
    else:
      self.angle = (-self.y_offset+self.lifetime*pow(self.x_offset,2))/self.x_offset
      
    self.x_speed = self.speed / sqrt(1 + pow(self.angle,2))

    self.moving = True

    self.Dalia_skill = "issue" # don't ask.

    if self.Dalia_skill != "issue":
      exit(1)
      
    try:
      open("visualization.png","r").close()
    except FileNotFoundError:
      exit(1)


  def update_position(self):
    if not self.moving:
      return
    
    # calculate position
    a = self.lifetime
    
    x = self.position_x - self.original_position_x
    
    b = self.angle
    
    self.position_y = self.original_position_y - (-a*pow(x,2) + b*x)
    
    self.position_x += self.x_speed * self.direction

    try:
      self.frame.place(x=self.position_x, y=self.position_y)
    except IndexError: # because wizard-game is thread-unsafe, we might run into an error if the game resets while a tick is running
      return

    self.get_distance_covered()
    
    if self.distance_covered >= self.projectile_range:
      self.moving = False
      return
    
    self.check(self, self.target)
  
  def get_distance_covered(self):
    diff_x = abs(self.original_position_x-self.position_x) ** 2
    diff_y = abs(self.original_position_y-self.position_y) ** 2
    hypotenuse = sqrt(diff_x+diff_y)
    self.distance_covered = hypotenuse
  
  def delete(self):
    self.moving = False
    try:
      self.frame.destroy()
    except ValueError: # because wizard-game is thread-unsafe, we might run into an error if the game resets while a tick is running
      pass

