import nebulatk as ntk

import projectile

root = ntk.Window(width = 500, height = 500, resizable = False, title = "Wizard Game")

c = ntk.Frame(root = root, width = 500, height = 500, fill = "black", border_width = 0)

c.place()

projectile1 = projectile.Projectile(None, None, None, 100, 100, None, root, 300, 300, 500)

projectile1.move_frame()