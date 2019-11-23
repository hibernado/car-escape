from pyglet.gl import *

window = pyglet.window.Window(width=600, height=600)
grid = pyglet.sprite.Sprite(pyglet.image.load('images/grid.jpg'))

xarr = [65, 85, 84, 83, 84, 84]
yarr = [65, 84, 84, 84, 84, 84]
w = 50
h = 50

# x_block_number = 6
# y_block_number = 1

vlists = []
for x_block_number in range(1, 7):
    for y_block_number in range(1, 7):
        x = sum(xarr[0:x_block_number])
        y = sum(yarr[0:y_block_number])
        vlist = pyglet.graphics.vertex_list(4, ('v2f', [x, y, x, y + h, x + w, y + h, x + w, y]))
        vlists.append(vlist)


@window.event
def on_draw():
    window.clear()
    grid.draw()
    glColor3f(1, 0, 0)
    for vlist in vlists:
        vlist.draw(GL_QUADS)


pyglet.app.run()
