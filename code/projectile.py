class Projectile:
  """
  Projectile class, which handles all the projectiles made.
  """
  def __init__(self, image, momentum, gravity):
    self.momentum = momentum
    self.image = image
    self.gravity = gravity