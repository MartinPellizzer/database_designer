import os
import json
import pygame
import subprocess

pygame.init()

screen_w = 1280
screen_h = 720

screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

running = True

font = pygame.font.Font(None, 24)
font_debug = pygame.font.Font(None, 24)

current_file = None

row_h = 34

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
    'node_drag': None,
    'node_focus': None,
    'field_focus': None,
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
    # screen_h = node['world_h'] * camera['scale']
    screen_h = row_h * (len(node['fields'])+1) * camera['scale']

    pygame.draw.rect(screen, background_color, (screen_x, screen_y, screen_w, screen_h))

    screen_h = row_h * camera['scale']
    pygame.draw.rect(screen, (0, 128, 0), (screen_x, screen_y, screen_w, screen_h))

    # screen_h = node['world_h'] * camera['scale']
    screen_h = row_h * (len(node['fields'])+1) * camera['scale']
    pygame.draw.rect(screen, border_color, (screen_x, screen_y, screen_w, screen_h), 1*int(camera['scale']))

    # SELECTED
    if node == interaction['node_focus'] and interaction['field_focus'] == 'title':
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, row_h), 2*int(camera['scale']))
    elif node == interaction['node_focus'] and interaction['field_i_focus'] != None:
        pygame.draw.rect(
            screen, (0, 0, 255), 
            (screen_x, screen_y + row_h*interaction['field_i_focus'], screen_w, row_h), 
            2*int(camera['scale'])
        )
    elif node == interaction['node_focus']:
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
        world_y = node['world_y'] + 10 + (i * row_h)
        screen_x, screen_y = world_to_screen(world_x, world_y)

        text = font.render(field['name'], True, (255, 255, 255))
        screen.blit(text, (screen_x, screen_y))

        world_x = node['world_x'] + node['world_w'] - 35
        screen_x, screen_y = world_to_screen(world_x, world_y)
        if 'key' not in field: field['key'] = ''
        if field['key'] == 'primary_key':
            text = font.render('PK', True, (255, 255, 255))
            screen.blit(text, (screen_x, screen_y))
        elif field['key'] == 'foreign_key':
            text = font.render('FK', True, (255, 255, 255))
            screen.blit(text, (screen_x, screen_y))

    '''
    pygame.draw.rect(screen, (0, 128, 0), (screen_x, screen_y + row_h*(i-1), row_h, row_h))
    text = font.render('+', True, (255, 255, 255))
    screen.blit(text, (screen_x, screen_y))
    '''

def project_new():
    global current_file
    global nodes
    filename = subprocess.run(
        [
            "zenity",
            "--file-selection",
            "--save",
            "--confirm-overwrite",
            "--file-filter=JSON files | *.json",
            "--filename=project.json",
        ],
        capture_output=True,
        text=True
    ).stdout.strip()
    if filename:
        if not filename.endswith(".json"):
            filename += ".json"
        nodes = []
        current_file = filename
        with open(filename, "w") as f:
            json.dump(nodes, f, indent=4)

def project_save():
    if current_file:
        with open(current_file, "w") as f:
            json.dump(nodes, f, indent=4)
    else:
        project_new()

def project_open():
    global current_file
    global nodes
    project_dir = os.path.dirname(os.path.abspath(__file__))
    filename = subprocess.run(
        [
            "zenity",
            "--file-selection",
            f"--filename=file://{project_dir}/",
            "--file-filter=JSON files | *.json",
        ],
        capture_output=True,
        text=True
    ).stdout.strip()
    if filename:
        with open(filename, "r") as f:
            nodes = json.load(f)
        current_file = filename

# ============================================================
# MAIN LOOP
# ============================================================

def edge_start():
    interaction['node_focus'] = None
    interaction['field_focus'] = None
    interaction['field_i_focus'] = None
    ### CLICKED ON NODE?
    for node in reversed(nodes):
        if (
            mouse['world_x'] >= node['world_x'] and 
            mouse['world_y'] >= node['world_y'] and 
            mouse['world_x'] <= node['world_x'] + node['world_w'] and 
            mouse['world_y'] <= node['world_y'] + row_h * (len(node['fields'])+1)
        ):
            nodes.remove(node)
            nodes.append(node)
            interaction['node_focus'] = node
            ### CLICKED ON FIELD?
            for field_i in range(len(node['fields'])+1):
                if (
                    mouse['world_x'] >= node['world_x'] and 
                    mouse['world_y'] >= node['world_y'] + row_h and 
                    mouse['world_x'] <= node['world_x'] + node['world_w']//2 and 
                    mouse['world_y'] <= node['world_y'] + row_h + (row_h*field_i)
                ):
                    interaction['action'] = 'edge'
                    interaction['edge_x1'] = mouse['screen_x']
                    interaction['edge_y1'] = mouse['screen_y']
                    interaction['node_start'] = node
                    interaction['field_start_i'] = field_i
                    found = True
                    break

def edge_end():
    interaction['node_focus'] = None
    interaction['field_focus'] = None
    interaction['field_i_focus'] = None
    ### CLICKED ON NODE?
    for node in reversed(nodes):
        if (
            mouse['world_x'] >= node['world_x'] and 
            mouse['world_y'] >= node['world_y'] and 
            mouse['world_x'] <= node['world_x'] + node['world_w'] and 
            mouse['world_y'] <= node['world_y'] + row_h * (len(node['fields'])+1)
        ):
            nodes.remove(node)
            nodes.append(node)
            interaction['node_focus'] = node
            ### CLICKED ON FIELD?
            for field_i in range(len(node['fields'])+1):
                if (
                    mouse['world_x'] >= node['world_x'] and 
                    mouse['world_y'] >= node['world_y'] + row_h and 
                    mouse['world_x'] <= node['world_x'] + node['world_w']//2 and 
                    mouse['world_y'] <= node['world_y'] + row_h + (row_h*field_i)
                ):
                    interaction['field_i_focus'] = field_i
                    ###
                    interaction['node_end'] = node
                    interaction['field_end_i'] = field_i
                    edge = {
                        'edge_start': {
                            'node': interaction['node_start'],
                            'field_i': interaction['field_start_i'],
                        },
                        'edge_end': {
                            'node': interaction['node_end'],
                            'field_i': interaction['field_end_i'],
                        },
                    }
                    edges.append(edge)
                    break

def edge_delete():
    if interaction['field_i_focus'] != None:
        for edge in edges:
            if edge['edge_start']['node'] == interaction['node_focus']:
                if edge['edge_start']['field_i'] == interaction['field_i_focus']:
                    edges.remove(edge)
                    return
            if edge['edge_end']['node'] == interaction['node_focus']:
                if edge['edge_end']['field_i'] == interaction['field_i_focus']:
                    edges.remove(edge)
                    return

################################################################################
# TEST
################################################################################

x = -200
y = 0
w = 200
h = 100
title = 'table_name'
kind = 'data'
description = ''
fields = [
    {'name': 'id', 'key': 'none'}, 
    {'name': 'name', 'key': 'none'}, 
]
node_create(x, y, w, h, title, kind, description, fields)

x = 100
y = 0
w = 200
h = 100
title = 'table_name'
kind = 'data'
description = ''
fields = [
    {'name': 'id', 'key': 'none'}, 
    {'name': 'name', 'key': 'none'}, 
]
node_create(x, y, w, h, title, kind, description, fields)

edge_1 = {
    'edge_start': {
        'node': nodes[0],
        'field_i': 1,
    },
    'edge_end': {
        'node': nodes[1],
        'field_i': 1,
    },
}

edge_2 = {
    'edge_start': {
        'node': nodes[0],
        'field_i': 2,
    },
    'edge_end': {
        'node': nodes[1],
        'field_i': 2,
    },
}

edges = []
# edges.append(edge_1)
# edges.append(edge_2)

def draw_edge(edge):
    ### LINE
    node_start_x = edge['edge_start']['node']['world_x']
    node_start_y = edge['edge_start']['node']['world_y'] + (row_h/2) + (edge['edge_start']['field_i'] * row_h)
    node_end_x = edge['edge_end']['node']['world_x']
    node_end_y = edge['edge_end']['node']['world_y'] + (row_h/2) + (edge['edge_end']['field_i'] * row_h)
    if node_start_x < node_end_x:
        node_start_x += edge['edge_start']['node']['world_w']
    else:
        node_end_x += edge['edge_end']['node']['world_w']
    screen_x1, screen_y1 = world_to_screen(node_start_x, node_start_y)
    screen_x4, screen_y4 = world_to_screen(node_end_x, node_end_y)
    screen_x2 = (screen_x1 + screen_x4) / 2
    screen_y2 = screen_y1
    screen_x3 = (screen_x1 + screen_x4) / 2
    screen_y3 = screen_y4
    points = [
        (screen_x1, screen_y1),
        (screen_x2, screen_y2),
        (screen_x3, screen_y3),
        (screen_x4, screen_y4),
    ]
    pygame.draw.lines(screen, (255, 255, 255), False, points)
    ### RELATIONSHIP TEXT
    text = font.render('1:N', True, (255, 255, 255))
    screen.blit(text, (screen_x2, (screen_y2 + screen_y3) / 2))
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    edge_start()
                else:
                    interaction['node_focus'] = None
                    interaction['field_focus'] = None
                    interaction['field_i_focus'] = None
                    for node in reversed(nodes):
                        if (
                            mouse['world_x'] >= node['world_x'] and 
                            mouse['world_y'] >= node['world_y'] and 
                            mouse['world_x'] <= node['world_x'] + node['world_w'] and 
                            # mouse['world_y'] <= node['world_y'] + node['world_h']
                            mouse['world_y'] <= node['world_y'] + row_h * (len(node['fields'])+1)
                        ):
                            nodes.remove(node)
                            nodes.append(node)
                            interaction['node_focus'] = node
                            if (
                                mouse['world_x'] >= node['world_x'] and 
                                mouse['world_y'] >= node['world_y'] and 
                                mouse['world_x'] <= node['world_x'] + node['world_w']//2 and 
                                mouse['world_y'] <= node['world_y'] + row_h
                            ):
                                interaction['field_focus'] = 'title'
                                break
                            found = False
                            # print(len(node['fields']))
                            for field_i in range(len(node['fields'])+1):
                                if (
                                    mouse['world_x'] >= node['world_x'] and 
                                    mouse['world_y'] >= node['world_y'] + row_h and 
                                    mouse['world_x'] <= node['world_x'] + node['world_w']//2 and 
                                    mouse['world_y'] <= node['world_y'] + row_h + (row_h*field_i)
                                ):
                                    interaction['field_i_focus'] = field_i
                                    # print(interaction['field_i_focus'])
                                    found = True
                                    break
                            if found: break
                            interaction['action'] = 'drag'
                            interaction['node_drag'] = node
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
                fields = [
                    {'name': 'id', 'key': 'none'}, 
                    {'name': 'name', 'key': 'none'}, 
                ]
                node_create(x, y, w, h, title, kind, description, fields)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if interaction['action'] == 'edge':
                    edge_end()
                interaction['action'] = None
                interaction['node_drag'] = None
            elif event.button == 2:
                interaction['action'] = None
                interaction['node_drag'] = None

        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                if camera['scale'] < 16:
                    camera['scale'] *= 2
            elif event.y == -1:
                if camera['scale'] > 1:
                    camera['scale'] /= 2
            font = pygame.font.Font(None, 24*int(camera['scale']))

        elif event.type == pygame.KEYDOWN:
            # Ctrl+N
            if event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                project_new()
            # Ctrl+S
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                project_save()
            # Ctrl+O
            elif event.key == pygame.K_o and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                project_open()
            # Ctrl+D
            elif event.key == pygame.K_d and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                edge_delete()
            # Ctrl+P
            elif event.key == pygame.K_p and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                if interaction['field_i_focus'] != None:
                    i = interaction['field_i_focus']-1
                    if interaction['node_focus']['fields'][i]['key'] != 'primary_key':
                        interaction['node_focus']['fields'][i]['key'] = 'primary_key'
                    else:
                        interaction['node_focus']['fields'][i]['key'] = ''
            # Ctrl+F
            elif event.key == pygame.K_f and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                if interaction['field_i_focus'] != None:
                    i = interaction['field_i_focus']-1
                    if interaction['node_focus']['fields'][i]['key'] != 'foreign_key':
                        interaction['node_focus']['fields'][i]['key'] = 'foreign_key'
                    else:
                        interaction['node_focus']['fields'][i]['key'] = ''
            # Reorder Fields
            elif event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if interaction['field_i_focus'] != None:
                    i = interaction['field_i_focus']-1
                    if i > 0:
                        node = interaction['node_focus']
                        node['fields'][i], node['fields'][i-1] = node['fields'][i-1], node['fields'][i]
                        interaction['field_i_focus'] = i
            elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if interaction['field_i_focus'] != None:
                    i = interaction['field_i_focus']-1
                    if i < len(node['fields'])-1:
                        node = interaction['node_focus']
                        node['fields'][i], node['fields'][i+1] = node['fields'][i+1], node['fields'][i]
                        interaction['field_i_focus'] = i + 2
            # Editor
            elif event.unicode == '+':
                if interaction['node_focus'] != None:
                    interaction['node_focus']['fields'].append({'name': 'field'})
            # Editor
            elif event.key == pygame.K_BACKSPACE:
                if interaction['node_focus'] != None:
                    if interaction['field_focus'] == 'title':
                        interaction['node_focus']['title'] = interaction['node_focus']['title'][:-1]
                    else:
                        if interaction['field_i_focus'] != None:
                            i = interaction['field_i_focus']-1
                            interaction['node_focus']['fields'][i]['name'] = interaction['node_focus']['fields'][i]['name'][:-1]
            else:
                if pygame.K_a <= event.key <= pygame.K_z or event.unicode == '_':
                    letter = event.unicode
                    if interaction['node_focus'] != None:
                        if interaction['field_focus'] == 'title':
                            interaction['node_focus']['title'] += letter
                        else:
                            if interaction['field_i_focus'] != None:
                                i = interaction['field_i_focus']-1
                                interaction['node_focus']['fields'][i]['name'] += letter

    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()

    mouse['world_x'], mouse['world_y'] = screen_to_world(mouse['screen_x'], mouse['screen_y'])
    if interaction['action'] == 'pan':
        dx = mouse['screen_x'] - interaction['mouse_x_start']
        dy = mouse['screen_y'] - interaction['mouse_y_start']
        camera['world_x'] = interaction['camera_x_start'] - dx / camera['scale']
        camera['world_y'] = interaction['camera_y_start'] - dy / camera['scale']

    if interaction['action'] == 'drag':
        interaction['node_drag']['world_x'] = mouse['world_x'] - interaction['drag_offset_x']
        interaction['node_drag']['world_y'] = mouse['world_y'] - interaction['drag_offset_y']



    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    screen.fill((40, 40, 40))

    draw_grid()
    # draw_objects()

    if interaction['action'] == 'edge':
        pygame.draw.line(screen, (255, 255, 255), (interaction['edge_x1'], interaction['edge_y1']), (mouse['screen_x'], mouse['screen_y']))

    for edge in edges:
        draw_edge(edge)

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

### TODO: create 2 nodes manually on startup, include a demo edge in the nodes struct between 2 fields, draw the edge

