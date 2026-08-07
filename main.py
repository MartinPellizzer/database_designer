import json
import pygame


pygame.init()

screen_w = 1280
screen_h = 720

screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

running = True

font = pygame.font.Font(None, 24)
font_debug = pygame.font.Font(None, 24)

camera = {
    'world_x': 0,
    'world_y': 0,
    'scale': 1,
}

mouse = {
    'screen_x': 0,
    'screen_y': 0,
    'world_x': 0,
    'world_y': 0,
}

nodes = []

interaction = {
    'action': None,
    'node': None,
    'node_focus': None,
    'drag_offset_x': 0,
    'drag_offset_y': 0,
    'camera_x_start': 0,
    'camera_y_start': 0,
    'mouse_x_start': 0,
    'mouse_y_start': 0,
}

# ============================================================
# NODES
# ============================================================

def node_create(x, y, w, h, title, kind, description, fields):
    types_allowed = ['data', 'linking', 'subset', 'validation']
    '''
    DESCRIPTION GUIDELINES: Write 1 short sentence explaining WHAT is this table (definition) and 1 short sentence explaining WHY this table is important.
    '''
    node = {
        'world_x': x,
        'world_y': y,
        'world_w': w,
        'world_h': h,
        'title': title,
        'kind': kind,
        'description': description,
        'fields': fields,
    }
    nodes.append(node)

# ============================================================
# COORDINATE CONVERSION
# ============================================================

def world_to_screen(x, y):
    return (
        (x - camera['world_x']) * camera['scale'] + screen_w / 2,
        (y - camera['world_y']) * camera['scale'] + screen_h / 2,
    )


def screen_to_world(x, y):
    return (
        (x - screen_w / 2) / camera['scale'] + camera['world_x'],
        (y - screen_h / 2) / camera['scale'] + camera['world_y'],
    )


# ============================================================
# GRID
# ============================================================

def draw_grid():
    grid_size = 100
    color = (28, 28, 28)

    # Get visible world boundaries
    left, top = screen_to_world(0, 0)
    right, bottom = screen_to_world(screen_w, screen_h)

    # Find first grid line
    start_x = int(left // grid_size) * grid_size
    start_y = int(top // grid_size) * grid_size

    # Find last grid line
    end_x = int(right // grid_size + 1) * grid_size
    end_y = int(bottom // grid_size + 1) * grid_size

    for x in range(start_x, end_x + grid_size, grid_size):
        x1, y1 = world_to_screen(x, top)
        x2, y2 = world_to_screen(x, bottom)
        pygame.draw.line(screen, color, (x1, y1), (x2, y2))

    for y in range(start_y, end_y + grid_size, grid_size):
        x1, y1 = world_to_screen(left, y)
        x2, y2 = world_to_screen(right, y)
        pygame.draw.line(screen, color, (x1, y1), (x2, y2))


# ============================================================
# WORLD OBJECTS
# ============================================================

def draw_node(node):
    ### RECT
    background_color = (65, 65, 65)
    border_color = (26, 26, 26)

    screen_x, screen_y = world_to_screen(node['world_x'], node['world_y'])
    screen_w = node['world_w'] * camera['scale']
    screen_h = node['world_h'] * camera['scale']

    pygame.draw.rect(screen, background_color, (screen_x, screen_y, screen_w, screen_h))

    screen_h = 30 * camera['scale']
    pygame.draw.rect(screen, (0, 128, 0), (screen_x, screen_y, screen_w, screen_h))

    screen_h = node['world_h'] * camera['scale']
    pygame.draw.rect(screen, border_color, (screen_x, screen_y, screen_w, screen_h), 1*int(camera['scale']))

    # SELECTED
    if node == interaction['node_focus']:
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, screen_h), 2*int(camera['scale']))

    ### TEXT
    world_x = node['world_x'] + 10
    world_y = node['world_y'] + 10

    screen_x, screen_y = world_to_screen(world_x, world_y)

    text = font.render(node['title'], True, (255, 255, 255))
    screen.blit(text, (screen_x, screen_y))

    i = 0
    for field in node['fields']:
        i += 1
        world_x = node['world_x'] + 10
        world_y = node['world_y'] + 10 + (i * 30)
        screen_x, screen_y = world_to_screen(world_x, world_y)

        text = font.render(field['name'], True, (255, 255, 255))
        screen.blit(text, (screen_x, screen_y))

# ============================================================
# MAIN LOOP
# ============================================================

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                interaction['node_focus'] = None
                for node in reversed(nodes):
                    if (
                        mouse['world_x'] >= node['world_x'] and 
                        mouse['world_y'] >= node['world_y'] and 
                        mouse['world_x'] <= node['world_x'] + node['world_w'] and 
                        mouse['world_y'] <= node['world_y'] + node['world_h']
                    ):
                        nodes.remove(node)
                        nodes.append(node)
                        interaction['action'] = 'drag'
                        interaction['node'] = node
                        interaction['node_focus'] = node
                        interaction['drag_offset_x'] = mouse['world_x'] - node['world_x']
                        interaction['drag_offset_y'] = mouse['world_y'] - node['world_y']
                        break
            elif event.button == 2:
                interaction['action'] = 'pan'
                interaction['camera_x_start'] = camera['world_x']
                interaction['camera_y_start'] = camera['world_y']
                interaction['mouse_x_start'] = event.pos[0]
                interaction['mouse_y_start'] = event.pos[1]
            elif event.button == 3:
                x = mouse['world_x']
                y = mouse['world_y']
                w = 200
                h = 100
                title = 'table_name'
                kind = 'data'
                description = ''
                fields = [{'name': 'id'}, {'name': 'name'}]
                node_create(x, y, w, h, title, kind, description, fields)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                interaction['action'] = None
                interaction['node'] = None
            elif event.button == 2:
                interaction['action'] = None
                interaction['node'] = None

        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                if camera['scale'] < 16:
                    camera['scale'] *= 2
            elif event.y == -1:
                if camera['scale'] > 1:
                    camera['scale'] /= 2
            font = pygame.font.Font(None, 24*int(camera['scale']))

        elif event.type == pygame.KEYDOWN:
            # Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                with open("nodes.json", "w") as f:
                    json.dump(nodes, f, indent=4)
            # Ctrl+O
            elif event.key == pygame.K_o and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                try:
                    with open("nodes.json", "r") as f:
                        nodes = json.load(f)
                except FileNotFoundError:
                    print("nodes.json not found")
            # Editor
            elif event.key == pygame.K_BACKSPACE:
                interaction['node_focus']['title'] = interaction['node_focus']['title'][:-1]
            else:
                # interaction['node_focus']['title'] += event.unicode
                if pygame.K_a <= event.key <= pygame.K_z:
                    letter = chr(event.key)
                    if interaction['node_focus'] != None:
                        interaction['node_focus']['title'] += letter

    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()

    mouse['world_x'], mouse['world_y'] = screen_to_world(mouse['screen_x'], mouse['screen_y'])
    if interaction['action'] == 'pan':
        dx = mouse['screen_x'] - interaction['mouse_x_start']
        dy = mouse['screen_y'] - interaction['mouse_y_start']
        camera['world_x'] = interaction['camera_x_start'] - dx / camera['scale']
        camera['world_y'] = interaction['camera_y_start'] - dy / camera['scale']

    if interaction['action'] == 'drag':
        interaction['node']['world_x'] = mouse['world_x'] - interaction['drag_offset_x']
        interaction['node']['world_y'] = mouse['world_y'] - interaction['drag_offset_y']



    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    screen.fill((40, 40, 40))

    draw_grid()
    # draw_objects()

    for node in nodes:
        draw_node(node)

    # --------------------------------------------------------
    # DEBUG UI
    # --------------------------------------------------------

    i = 1

    text = font_debug.render(f"mouse screen x:{mouse['screen_x']} y:{mouse['screen_y']}", True, (255, 0, 255))
    screen.blit(text, (32, 24 * i))
    i += 1
    text = font_debug.render(f"mouse world x:{mouse['world_x']:.2f} y:{mouse['world_y']:.2f}", True, (255, 0, 255))
    screen.blit(text, (32, 24 * i))
    i += 1
    text = font_debug.render(f"camera world x:{camera['world_x']:.2f} y:{camera['world_y']:.2f}", True, (255, 0, 255))
    screen.blit(text, (32, 24 * i))
    i += 1
    text = font_debug.render(f"screen center x:{screen_w // 2} y:{screen_h // 2}", True, (255, 0, 255))
    screen.blit(text, (32, 24 * i))
    i += 1
    text = font_debug.render(f"scale: {camera['scale']}", True, (255, 0, 255))
    screen.blit(text, (32, 24 * i))
    i += 1

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
