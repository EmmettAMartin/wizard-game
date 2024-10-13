from weapon import *
import nebulatk as ntk
from math import sqrt

class Player:
  """
  Main Player class.
  Takes a butt ton of variables, and does a butt ton of stuff.
  Look at the individual functions for more information.
  """

  def __init__(self, root, name: str, player_colour: str, speed: int = 3, hotbar: list = [], health: int = 50):
    self.hotbar = hotbar
    self.vertical_direction = 0
    self.horizontal_direction = 0
    self.speed = speed
    self.health = health
    self.curr_x = 100
    self.curr_y = 100
    self.momentum_x = 0
    self.momentum_y = 0
    self.root = root

    if name == "Womzard":
      self.wizard_texture = "wizard.png"
    if name == "Wimzard":
      self.wizard_texture = "wizard2.png"

    self.player_frame = ntk.Label(root=root, width=30, height=30, image=self.wizard_texture).place(x = self.curr_x, y = self.curr_y)

    self.health_frame_border = ntk.Frame(root=root, fill = "white", width = self.health+4, height = 10, border_width=0)
    self.health_frame = ntk.Frame(root = self.health_frame_border, fill = player_colour, width = self.health, height = 6, border_width=0)
    self.health_frame_border.place(x = 1, y = 1)
    self.health_frame.place(x = 2, y = 2)

    self.can_attack = True
    self.name = name
    self.last_key_pressed = -1

    self.sword = Weapon(name = "sword", damage = 6, attack_range = 75, image_list = ["sword.png", "sword2.png"])
    self.hellsword = Weapon(name = "hellsword", damage = 10, attack_range = 90, image_list = ["hellsword.png"])
    #---------------------------------------------------------------------------------------------------------------------------------#
    self.cat = Weapon(name = "cat", damage = 10, attack_range = 500, image_list = ["cat.png"]) # DO NOT USE: TOO BUSTED AT THIS TIME! #
    #---------------------------------------------------------------------------------------------------------------------------------#
    self.dagger = Weapon(name = "dagger", damage = 4, attack_range = 45, image_list = ["dagger.png"])
    self.shield = Weapon(name = "shield", damage = 0, attack_range = 0, image_list = ["shield.png"])
    self.bow = Weapon(name = "bow", damage = 3, attack_range = 200, image_list = ["bow.png"])


  def load_hotbar(self):
    """
    Loads the items into the hotbar.
    """

    if len(self.hotbar) > 4:
      """
      Makes sure that there are only 4 items in the hotbar.
      Deletes every item after item 4.
      """
      print("ERROR: Impossible to have more than 4 items in hotbar at a time")
      while len(self.hotbar) > 4:
        del self.hotbar[4]

    self.hotbar_list = []
    spacer = 0
    for slot in self.hotbar:
      try:
        hotbar_frame = ntk.Label(root=self.root, width = 24, height = 24, border_width = 2, image = slot.chosen_image, border = "white").place(((self.health)+10)+spacer, 1)
      except FileNotFoundError:
        hotbar_frame = ntk.Label(root=self.root, width = 24, height = 24, border_width = 2, image = "0.png", border = "white").place(((self.health)+10)+spacer, 1)
      self.hotbar_list.append(hotbar_frame)
      spacer += 30


  def check_movement_y(self, curr_y: int):
    """
    Check if the current position of the player is within the allowed vertical area of the screen.
    """
    if (curr_y > 469) or (curr_y < 31):
      return False
    else: return True


  def check_movement_x(self, curr_x: int):
    """
    Check if the current position of the player is within the allowed horizontal area of the screen.
    """
    if (curr_x > 469) or (curr_x < 2):
      return False
    else: return True


  def move(self, key):
    """
    Adds or subtracts momentum to the player.
    """
    key = self.check_keys(key)

    match key:
      case "w":
        self.momentum_y = -1
      case "a":
        self.momentum_x = -1
      case "s":
        self.momentum_y = 1
      case "d":
        self.momentum_x = 1


  def check_keys(self, key):
    """
    Changes player 2 keys to player 1 keys for the move function.
    """
    if key == "i":
      return "w"
    elif key == "j":
      return "a"
    elif key == "k":
      return "s"
    elif key == "l":
      return "d"
    else:
      return key


  def reset_momentum(self):
    """
    Sets momentum to 0.
    """
    self.momentum_x, self.momentum_y = 0, 0
      

  def update_position(self):
    """
    Updates the position of the player.
    """
    if self.check_movement_x(self.curr_x + self.momentum_x):
      self.curr_x += self.momentum_x * self.speed

    if self.check_movement_y(self.curr_y + self.momentum_y):
      self.curr_y += self.momentum_y * self.speed

    self.player_frame.place(x = self.curr_x, y = self.curr_y)


  def is_target_in_range(self, x: int, y: int, target_x: int, target_y: int, attack_range: int):
    """
    Takes the current position of the player and the target, and the attack range of the weapon in use.
    Calculates whether or not player is in range to hit their target, using the Pythagorean theorem.

    Returns True or False.
    """
    # We need A, B and C. To find A and B, we just take the absolute of x-target_x and y-target_y.
    # From there, we can find C by using A^2 + B^2 = C^2. Then sqrt(C) and check that against attack range.
    a = (abs(y-target_y)) ** 2
    b = (abs(x-target_x)) ** 2
    c = a+b # Stay in school kids. It helps you make video games.

    if (sqrt(c) <= attack_range):
      return True
    else: return False


  def attack(self, target: object, damage: int, attack_range: int):
    """
    Takes a target, damage, and attack range. If it is possible to attack, will then damage target and
    update their health. Will prevent player from attacking if other player is dead or out of range.
    """
    within_range = self.is_target_in_range(x = self.curr_x, y = self.curr_y, target_x = target.curr_x, target_y = target.curr_y, attack_range = attack_range)
    if within_range and self.can_attack:
      target.health -= damage
      target.update_health()
    if target.health <= 0 and self.can_attack:
      self.can_attack = False
      print(f"Player health at: {self.health}")


  def melee(self, target: object):
    """
    Calls attack function, with minimal range and damage. Bound to 'c' and '.' by default.
    """
    self.attack(target = target, damage = 2, attack_range = 45)
  

  def deflection(self):
    print("Deflecting")


  def update_health(self):
    """
    Updates the health of the player. It resizes the player's health bar, and checks if the player has died, and will hide them if they have.
    """
    if self.health > 0:
      self.health_frame.configure(width = self.health)
    else:
      print(f"Player {self.name} has died.")
      self.can_attack = False
      self.health_frame.hide()
      self.curr_x = -100
      self.curr_y = -100
      self.update_position()


  def use_hotbar(self, key):
    """
    Takes keypress, and converts it to an int. Then it determines which hotbar slot should be selected.
    Converts (7,8,9,0) into (1,2,3,4).
    """
    key = int(key)
    if key in (7,8,9,0):
      if key == 0:
        """
        VSCode says this is unreachable. It's wrong. IDK why or how. EDIT: It has to do with setting the type of variable accepted by the
        function. Removing the ': str' from the arguments will fix it. However, gameplay is unaffected whatsoever.
        For now, the ': str' is removed (for visual reasons).
        """
        key = 4
      else: key -= 6
    self.hotbar_list[key-1].configure(fill = "green")
    self.last_key_pressed = key-1
    for i in range(len(self.hotbar_list)):
      if self.hotbar_list[i] != self.hotbar_list[key-1]:
        self.hotbar_list[i].configure(fill = "black")


  def use_item(self, target: object):
    """
    Uses the item in the selected hotbar slot.
    """
    if self.last_key_pressed != -1:
      self.attack(target = target, damage = self.hotbar[self.last_key_pressed].damage, attack_range = self.hotbar[self.last_key_pressed].attack_range)


  def reset(self):
    """
    Resets the position of the player.
    """
    self.reset_momentum()
    self.curr_x = 100
    self.curr_y = 100
    self.update_position()
    self.health = 50
    self.update_health()
    self.health_frame.show()
    self.can_attack = True
    print("Resetting " + self.name)