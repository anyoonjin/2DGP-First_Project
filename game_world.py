# world[0] : 백그라운드 객체들
# world[1] : foreground 객체들
world = [[],[]]

def add_object(o,depth):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return