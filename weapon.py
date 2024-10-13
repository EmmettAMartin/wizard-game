from random import randint

class Weapon:
  def __init__(self, damage: int, image_list: list, name: str, attack_range: int):
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

