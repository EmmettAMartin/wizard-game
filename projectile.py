class Projectile:
  """
  Projectile class, which handles all the projectiles made.
  """
  def __init__(self, image, momentum_x, momentum_y, curr_x, curr_y, gravity, root):
    self.root = root
    self.momentum_x = momentum_x
    self.momentum_y = momentum_y
    self.curr_x = curr_x
    self.curr_y = curr_y
    self.image = image
    self.gravity = gravity


  def update_position(self):
    """
    Updates the position of the player.
    """
    if self.check_movement_x(self.curr_x + self.momentum_x):
      self.curr_x += self.momentum_x * self.speed

    if self.check_movement_y(self.curr_y + self.momentum_y):
      self.curr_y += self.momentum_y * self.speed

    self.player_frame.place(x = self.curr_x, y = self.curr_y)
