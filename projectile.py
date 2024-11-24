# The projectile moves on a slope
# The slope is determined by (y2-y1)/(x2-x1)
# Where y2 and x2 are the target x and y,
# while y1 and x1 are the player x and y.
# So -> step 1. We need to get our new X value and Y value. Just add the offsets.
#       step 2. We then get the slope. IF the slope is 0, then we don't do anything involving y rotation.
#               IF the slope is undefined, then we don't do anything with the x rotation, and set the x momentum to 0.
#       step 3. We then add the speed to the x (unless we can't, see step 2)
#       step 4. Add the upwards momentum to the y (again, unless we can't, see step 2)
#       step 5. Finally, we check if our projectile can go any farther (has it reached it's maximum distance), and then update the position!

class Projectile:
  """
  Projectile class, which defines the movements and trajectories of projectiles.
  """
  def __init__(self, image, momentum_x, momentum_y, position_x, position_y, gravity, root, x_offset, y_offset, target_x, target_y):
    self.root = root
    self.momentum_x = momentum_x
    self.momentum_y = momentum_y
    self.position_x = position_x
    self.position_y = position_y
    self.image = image
    self.gravity = gravity
    self.x_offset = x_offset
    self.y_offset = y_offset
    self.target_x = target_x
    self.target_y = target_y
    self.is_undefined_string = "undefined"

  def set_offsets(self):
    self.position_x += self.x_offset
    self.position_y += self.y_offset
  
  def get_slope(self):
    x_result = self.target_x-self.position_x
    y_result = self.target_y-self.position_y
    if x_result == 0:
      return self.is_undefined_string
    else:
      return y_result/x_result
  
  def apply_momentum(self):
    slope = self.get_slope()
    if slope == self.is_undefined_string:
      self.momentum_x = 0
    elif slope == 0:
      pass
    else:
      pass