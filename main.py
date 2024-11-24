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

import time

import player

import weapon

from subprocess import *

import projectile

root = ntk.Window(width = 500, height = 500, resizable = False, title = "Wizard Game")

def close():
  global game_running
  game_running = False
root.closing_command = close

c = ntk.Frame(root = root, width = 500, height = 500, fill = "black", border_width = 0)

c.place()

def player_2_setup():
  """
  Sets up the player2 position, as well as the hotbar and health bar position.
  """
  p2.curr_x = 400
  p2.health_frame_border.place(x = 445, y = 1)
  p2.health_frame.place(x = 2, y = 2)
  p2.update_position()
  for j in range(len(p2.hotbar)):
    p2.hotbar[j].regenerate_image()
  for i in range(4):
    """
    We need to take 500, the outer limit of the screen size, and
    subtract the length of the frame size. After that we can take -100, and add 30*i,
    and add that result back into our original calculation.
    Since we never update the position of the hotbar frames,
    we can use the length of the health bar as if it was a static value.
    """
    p2.hotbar_list[i].place(x = 500-p2.health-24-100+(30*i), y = 1) # This needs to change sometime in the future.


def get_keypress(event):
  """
  Handles all keypresses necessary to run the game. Needs to change.
  """
  key = str.lower(event.char)

  if key in ("i","j","k","l"):
    p2.move(key)
  elif key == ".":
    p2.melee(p1)
  elif key in ("7","8","9","0"):
    p2.use_hotbar(key)
  elif key == "o":
    p2.use_item(p1)

  elif key in ("w","a","s","d"):
    p1.move(key)
  elif key == "c":
    p1.melee(p2)
  elif key in ("1","2","3","4"):
    p1.use_hotbar(key)
  elif key == "e":
    p1.use_item(p2)

  elif key == "t":
    p1.reset()
    p2.reset()
    player_2_setup()


def initial_player_creation():
  global p1
  global p2
  # Paves the way for menu creation later on by not having the objects created as soon as the file is ran.
  # Just making life easier for future me.
  p1 = player.Player(root=root, name = "Womzard", player_colour = "orange")
  p1.hotbar = [sword, bow, hellsword, dagger]
  p1.load_hotbar()
  p2 = player.Player(root=root, name = "Wimzard", player_colour = "violet")
  p2.hotbar = [sword, bow, hellsword, dagger]
  p2.load_hotbar()
  player_2_setup()


sword = weapon.Weapon(name = "sword", damage = 6, attack_range = 75, image_list = ["sword.png", "sword2.png"])
hellsword = weapon.Weapon(name = "hellsword", damage = 10, attack_range = 90, image_list = ["hellsword.png"])
#-----------------------------------------------------------------------------------------------------------------------------------#
cat = weapon.Weapon(name = "cat", damage = 10, attack_range = 500, image_list = ["cat.png"]) # DO NOT USE: TOO BUSTED AT THIS TIME! #
#-----------------------------------------------------------------------------------------------------------------------------------#
dagger = weapon.Weapon(name = "dagger", damage = 4, attack_range = 45, image_list = ["dagger.png"])
shield = weapon.Weapon(name = "shield", damage = 0, attack_range = 0, image_list = ["shield.png"])
bow = weapon.Weapon(name = "bow", damage = 3, attack_range = 200, image_list = ["bow.png"])

initial_player_creation()

def get_keyups(event):
  key = str.lower(event.char)

  if key in ("w","a","s","d"):
    p1.reset_momentum()
  elif key in ("i","j","k","l"):
    p2.reset_momentum()


root.bind("<KeyPress>", get_keypress)
root.bind("<KeyRelease>", get_keyups)

game_running = True

tps = 50
while game_running:
  start_tick = time.time()

  p1.update_position()
  p2.update_position()

  completed_in = time.time()-start_tick
  if completed_in < (1/tps):
    time.sleep(1/tps - completed_in)
