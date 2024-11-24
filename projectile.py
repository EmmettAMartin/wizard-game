class Projectile:
  """
  Projectile class, which handles all the projectiles made.
  """
  def __init__(self, image, momentum_x, momentum_y, curr_x, curr_y, gravity, root, x_offset, y_offset):
    self.root = root
    self.momentum_x = momentum_x
    self.momentum_y = momentum_y
    self.curr_x = curr_x
    self.curr_y = curr_y
    self.image = image
    self.gravity = gravity
    self.x_offset = x_offset
    self.y_offset = y_offset

  

  
