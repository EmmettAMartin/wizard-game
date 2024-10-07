"""
LORE: The Blue Wizard is named Wimzard, and the Red Wizard is named Womzard.
It all started when Wimzard and Womzard were having tea together, and discussing what their ideal tea was.
Wimzard enjoyed lemon in his tea, while Womzard preferred milk. Not only this, but Wimzard was more of a coffee person,
and believes that's where milk belongs. Womzard was appalled at this revelation, and the situation deteriorated from there.

Thanks to my friend, Sergeant_Ranger (Reuben), for helping me port NebulaTK into the game, and for helping me with some of the functions and code.
He also made NebulaTK, and it's great! Check it out when it releases!

Thanks to my Sister, Madeleine, for helping me with the lore, and naming the characters.

Thanks to my friend, Rowan, for playing it with me, even when it was literally just 2 cubes and 2 bars at the top of the screen,
and to listening to my dev updates.

CODING PROTOCOLS:
Please use descriptive function names, even if they are long and annoying to type.
Please add function descriptions, and try to add preffered types for the variables that are being passed.
Please ALWAYS have a space before and after an equals sign: " = "
Try to not have too much complicated and very specific math, but I'm guilty of it too, so it's ok if you do have some.
If you do have complicated math with hard-coded values, then just make sure to add a description.
"""


import nebulatk as ntk

from random import randint

from math import sqrt

import time

root = ntk.Window(width = 500, height = 500, resizable = False, title = "Wizard Game")

c = ntk.Frame(root = root, width = 500, height = 500, fill = "black", border_width = 0)

c.place()


class Player:
  """
  Main Player class.
  Takes a butt ton of variables, and does a butt ton of stuff.
  Look at the individual functions for more information.
  """

  def __init__(self, name: str, player_colour: str, speed: int = 10, hotbar: list = [], health: int = 50):
    self.hotbar = hotbar
    self.vertical_direction = 0
    self.horizontal_direction = 0
    self.speed = speed
    self.health = health
    self.curr_x = 100
    self.curr_y = 100
    self.momentum_x = 0
    self.momentum_y = 0

    if name == "Womzard":
      self.wizard_texture = "wizard.png"
    if name == "Wimzard":
      self.wizard_texture = "wizard2.png"

    self.player_frame = ntk.Label(root, width=30, height=30, image=self.wizard_texture).place(x = self.curr_x, y = self.curr_y)

    self.health_frame_border = ntk.Frame(root, fill = "white", width = self.health+4, height = 10, border_width=0)
    self.health_frame = ntk.Frame(self.health_frame_border, fill = player_colour, width = self.health, height = 6, border_width=0)
    self.health_frame_border.place(x = 1, y = 1)
    self.health_frame.place(x = 3, y = 3)

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
        hotbar_frame = ntk.Label(root, width = 24, height = 24, border_width = 2, image = slot.chosen_image, border = "white").place(((self.health)+10)+spacer, 1)
      except FileNotFoundError:
        hotbar_frame = ntk.Label(root, width = 24, height = 24, border_width = 2, image = "0.png", border = "white").place(((self.health)+10)+spacer, 1)
      self.hotbar_list.append(hotbar_frame)
      spacer += 30


  def check_movement_y(self, curr_y: int):
    """
    Check if the current position of the player is within the allowed vertical area of the screen.
    """
    if (curr_y > 470) or (curr_y < 30):
      return False
    else: return True


  def check_movement_x(self, curr_x: int):
    """
    Check if the current position of the player is within the allowed horizontal area of the screen.
    """
    if (curr_x > 470) or (curr_x < 0):
      return False
    else: return True


  def move(self, key):
    key = self.check_keys(key)

    # Change to Match-Case later on
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


  def destroy_class(self):
    """
    Destroys health bar and player.
    """
    self.player_frame.destroy()
    self.health_frame.destroy()
    for i in range(len(self.hotbar_list)):
      self.hotbar_list[i].destroy()
    
    self.health_frame.destroy()
    self.health_frame_border.destroy()


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
    EDIT: Buggy and does not work.
    EDIT 2: Just doesn't work. Not buggy anymore though.
    """
    self.chosen_image = self.image_list[randint(0, len(self.image_list)-1)]
    if len(self.image_list) == 0:
      self.chosen_image = "0.png"
    self.chosen_image = str(self.chosen_image)


class Projectile:
  """
  
  """
  def __init__(self, image, velocity):
    self.velocity = velocity
    self.image = image


def player_2_setup():
  """
  Sets up the player2 position, as well as the hotbar and health bar position.
  """
  p2.curr_x = 400
  p2.health_frame_border.place(x = 445, y = 1)
  p2.health_frame.place(x = 447, y = 3)
  p2.update_position()
  for j in range(len(p2.hotbar)):
    p2.hotbar[j].regenerate_image()
  for i in range(4):
    """
    This is more or less the same as the code in the __init__, but here it has to be modified
    to fit the needs of player 2. We need to take 500, the outer limit of the screen size, and
    subtract the length of the frame size. After that we can take -100, and add 30*i, and add that
    result back into our original calculation.
    Since we never update the position of the hotbar frames, we can use the length of the health bar as if it was a static value.
    """
    p2.hotbar_list[i].place(x = 500-p2.health-28-100+(30*i), y = 1) # This needs to change sometime in the future.


def reset():
  """
  Resets the visuals of the game, and resets player health and position.
  """
  print("Resetting!")
  global p1
  global p2
  p1.destroy_class()
  p2.destroy_class()
  p1 = Player(name = "Womzard", player_colour = "orange")
  p1.hotbar = [p1.sword, p1.bow, p1.hellsword, p1.dagger]
  p1.load_hotbar()
  p2 = Player(name = "Wimzard", player_colour = "violet")
  p2.hotbar = [p2.sword, p2.bow, p2.hellsword, p2.dagger]
  p2.load_hotbar()
  p1.curr_x, p1.curr_y = 100, 100
  p1.update_position()
  player_2_setup()
  p1.last_key_pressed = -1
  p2.last_key_pressed = -1


def get_keypress(event):
  """
  Handles all keypresses necessary to run the game. Needs to change.
  """
  key = str.lower(event.char)

  if key in ("i","j","k","l"):
    p2.move(key)
  if key == ".":
    p2.melee(p1)
  if key in ("7","8","9","0"):
    p2.use_hotbar(key)
  if key == "o":
    p2.use_item(p1)

  if key in ("w","a","s","d"):
    p1.move(key)
  if key == "c":
    p1.melee(p2)
  if key in ("1","2","3","4"):
    p1.use_hotbar(key)
  if key == "e":
    p1.use_item(p2)

  if key == "t":
    reset()


def initial_player_creation():
  global p1
  global p2
  # Paves the way for menu creation later on by not having the objects created as soon as the file is ran.
  # Just making life easier for future me.
  p1 = Player(name = "Womzard", player_colour = "orange")
  p1.hotbar = [p1.sword, p1.bow, p1.hellsword, p1.dagger]
  p1.load_hotbar()
  p2 = Player(name = "Wimzard", player_colour = "violet")
  p2.hotbar = [p2.sword, p2.bow, p2.hellsword, p2.dagger]
  p2.load_hotbar()
  player_2_setup()


initial_player_creation()

def reset_momentum(event):
  key = str.lower(event.char)

  if key in ("w","a","s","d"):
    p1.reset_momentum()
  if key in ("i","j","k","l"):
    p2.reset_momentum()

root.bind("<KeyPress>", get_keypress)
root.bind("<KeyRelease>", reset_momentum)

# LKDJSFA;LKDJFA;LSJ IDK how to "main game loop"

game_running = True

i = 0
while game_running:
  time.sleep(0.05)
  p1.update_position()
  p2.update_position()
  
