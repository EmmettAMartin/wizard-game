from random import randint


MELEE = 0

RANGED = 1

class Weapon:
  def __init__(self, damage: int, image_list: list, name: str, attack_range: int, attack_type: int):
    """
    Basically just a placeholder for variables. All necessary weapon variables go here.
    Also handles which image is used.
    All Weapon textures must be 20x20 pixels.
    """
    self.name = name
    self.attack_range = attack_range
    self.damage = damage
    self.image_list = image_list
    self.chosen_image = self.image_list[randint(0, len(self.image_list)-1)]
    self.attack_type = attack_type

    if len(self.image_list) == 0:
      self.chosen_image = "0.png"
    self.chosen_image = str(self.chosen_image)
    

  def regenerate_image(self): 
    """
    Same image code as in the __init__. Just rechooses the image randomly.
    """
    self.chosen_image = self.image_list[randint(0, len(self.image_list)-1)]
    if len(self.image_list) == 0:
      self.chosen_image = "0.png"
    self.chosen_image = str(self.chosen_image)

class MeleeWeapon(Weapon):
  def __init__(self, damage: int, image_list: list, name: str, attack_range: int):
    """
    Basically just a placeholder for variables. All necessary weapon variables go here.
    Also handles which image is used.
    All Weapon textures must be 20x20 pixels.
    """
    super().__init__(damage, image_list, name, attack_range, MELEE)

class RangedWeapon(Weapon):
  def __init__(self, damage: int, image_list: list, name: str, attack_range: int, projectile_speed: int = 3, projectile_image: any = None):
    """
    Basically just a placeholder for variables. All necessary weapon variables go here.
    Also handles which image is used.
    All Weapon textures must be 20x20 pixels.
    """
    super().__init__(damage, image_list, name, attack_range, RANGED)
    
    self.projectile_image = projectile_image
    self.projectile_speed = projectile_speed
    

