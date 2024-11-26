import nebulatk as ntk
from math import sqrt

from projectile import Projectile
import weapon

class Player:
  """
  Main Player class.
  Takes a crap ton of variables, and does a crap ton of stuff.
  Look at the individual functions for more information.
  """

  def __init__(self, root, name: str, player_colour: str, speed: int = 2, hotbar: list = [], health: int = 50):
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

    self.projectiles = []

    self.player_frame = ntk.Label(root=root, width=30, height=30, image=self.wizard_texture).place(x = self.curr_x, y = self.curr_y)

    self.health_frame_border = ntk.Frame(root=root, fill = "white", width = self.health+4, height = 10, border_width=0)
    self.health_frame = ntk.Frame(root = self.health_frame_border, fill = player_colour, width = self.health, height = 6, border_width=0)
    self.health_frame_border.place(x = 1, y = 1)
    self.health_frame.place(x = 2, y = 2)

    self.can_attack = True
    self.name = name
    self.last_key_pressed = -1


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

  def update_projectiles(self):
    for projectile in self.projectiles:
      if projectile.moving:
        projectile.update_position()
      else:
        projectile.delete()
        self.projectiles.remove(projectile)

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

  def deal_damage(self, target: object, damage: int):
    target.health -= damage
    target.update_health()
    if target.health <= 0 and self.can_attack:
      self.can_attack = False
      print(f"Player health at: {self.health}")
    
  def attack(self, target: object, damage: int, attack_range: int):
    """
    Takes a target, damage, and attack range. If it is possible to attack, will then damage target and
    update their health. Will prevent player from attacking if other player is dead or out of range.
    """
    within_range = self.is_target_in_range(x = self.curr_x, y = self.curr_y, target_x = target.curr_x, target_y = target.curr_y, attack_range = attack_range)
    if within_range and self.can_attack:
      self.deal_damage(target, damage)


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

  def check_hit(self, projectile, target):
    if (projectile.position_x >= target.curr_x 
        and projectile.position_x + 10 <= target.curr_x + 30
        and projectile.position_y + 10 >= target.curr_y
        and projectile.position_y <= target.curr_y + 30):
      self.deal_damage(target, projectile.damage)
      projectile.delete()
      self.projectiles.remove(projectile)

  def use_item(self, target: object):
    """
    Uses the item in the selected hotbar slot.
    """
    if self.last_key_pressed == -1:
      return
    
    current_weapon = self.hotbar[self.last_key_pressed]
    
    if not self.can_attack:
      return
    
    if current_weapon.attack_type == weapon.MELEE:
      self.attack(target = target, damage = current_weapon.damage, attack_range = current_weapon.attack_range)
    elif current_weapon.attack_type == weapon.RANGED:
      projectile = Projectile(
        root = self.root,
        target = target,
        
        image = current_weapon.projectile_image, 
        
        position_x=self.curr_x, 
        position_y=self.curr_y,
        
        speed=current_weapon.projectile_speed,
        
        projectile_range=current_weapon.attack_range,
        damage = current_weapon.damage,
        
        check = self.check_hit,
      )
      self.projectiles.append(projectile)


  def reset(self):
    """
    Resets the position of the player.
    """
    for projectile in self.projectiles:
      projectile.delete()
    self.projectiles = []
    
    self.reset_momentum()
    self.curr_x = 100
    self.curr_y = 100
    self.update_position()
    self.health = 50
    self.update_health()
    self.health_frame.show()
    self.can_attack = True
    print("Resetting " + self.name)
