import nebulatk as ntk
from time import sleep
from math import sqrt

class Projectile:
  """
  Projectile class, which defines the movements and trajectories of projectiles.
  """
  def __init__(self, image, momentum_x, momentum_y, position_x, position_y, gravity, root, target_x, target_y, projectile_range):
    self.image = image
    self.position_x = position_x # position of projectile
    self.position_y = position_y
    self.target_x = target_x # position of the target
    self.target_y = target_y
    self.projectile_range = projectile_range # range of projectile
    self.momentum_x = momentum_x # The change in the position.
    self.momentum_y = momentum_y
    self.gravity = gravity # The negative y influence that also affects the projectile position
    self.root = root # Root widget for the projectile widget
    self.is_undefined_string = "undefined"
    self.frame = ntk.Frame(self.root, width=10, height=10, fill="white")
    self.distance_covered = 0
    self.original_position_x = position_x
    self.original_position_y = position_y

    self.Dalia_skill = "issue" # don't ask.

    if self.Dalia_skill != "issue":
      exit(1)


  def move_frame(self):
    while True:
      sleep(0.01)
      self.position_x += 1
      self.position_y += 1
      self.frame.place(x=self.position_x, y=self.position_y)
      self.get_distance_covered()
      if self.distance_covered >= self.projectile_range:
        self.reset_position()
  
  def get_distance_covered(self):
    diff_x = abs(self.original_position_x-self.position_x) ** 2
    diff_y = abs(self.original_position_y-self.position_y) ** 2
    hypotenuse = sqrt(diff_x+diff_y)
    self.distance_covered = hypotenuse

  def reset_position(self):
    self.position_x = self.original_position_x
    self.position_y = self.original_position_y
  


  # def get_slope(self):
  #   x_result = self.target_x-self.position_x
  #   y_result = self.target_y-self.position_y
  #   if x_result == 0:
  #     return self.is_undefined_string
  #   else:
  #     return y_result/x_result
  
  # def apply_momentum(self):
  #   slope = self.get_slope()
  #   if slope == self.is_undefined_string:
  #     self.momentum_x = 0
  #   elif slope == 0:
  #     pass
  #   else:
  #     pass
