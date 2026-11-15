### TODO
"""
implement left sidebar. include entries for inserting RAW relationship term and RESOLVED relationship term.
if RESOLVED term is not filled, the node graph shows the RAW term in red.
include also a field for the count of the frequency.
"""

import os
import json
import pygame
import subprocess

from lib import g
from lib import io

input_filepath = f'{g.VAULT_FOLDERPATH}/ozonogroup/data/parse/pubmed/terms/ozone/test.json'
input_data = io.json_read(input_filepath)

pygame.init()

screen_w = 1600
screen_h = 900

screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

font_sidebar_size = 24

font = pygame.font.Font(None, 24)
font_debug = pygame.font.Font(None, font_sidebar_size)
font_sidebar = pygame.font.Font(None, 18)
font_bottom = pygame.font.Font(None, 24)

current_file = None

row_h = 34

terms_2_index = 0

core = {
    'running': True,
}

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

interaction = {
    'action': None,
    'node_drag': None,
    'node_focus': None,
    'field_focus': None,
    'field_i_focus': None,
    'edge_focus': None,
    'drag_offset_x': 0,
    'drag_offset_y': 0,
    'camera_x_start': 0,
    'camera_y_start': 0,
    'mouse_x_start': 0,
    'mouse_y_start': 0,
}

nodes = []
edges = []

frame_bottom = {
    'x': 0,
    'y': screen_h - 240,
    'w': screen_w,
    'h': 240,
}

frame_left = {
    'x': 0,
    'y': 0,
    'w': 480,
    'h': screen_h - 240,
}

frame_center = {
    'x': 0 + frame_left['w'],
    'y': 0,
    'w': screen_w - frame_left['w'],
    'h': screen_h - frame_bottom['h'],
}

definitions_focus = []

################################################################################
# PROJ UTILS
################################################################################

def project_new():
    global current_file
    global nodes
    global edges
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
        edges = []
        current_file = filename
        with open(filename, "w") as f:
            output = {
                'nodes': nodes,
                'edges': edges,
            }
            json.dump(output, f, indent=4)

def project_save():
    if current_file:
        with open(current_file, "w") as f:
            output = {
                'nodes': nodes,
                'edges': edges,
            }
            json.dump(output, f, indent=4)
    else:
        project_new()

def project_open(filename=''):
    global current_file
    global nodes
    global edges
    project_dir = os.path.dirname(os.path.abspath(__file__)) + '/uncategorized'
    if filename == '':
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
            data = json.load(f)
            nodes = data['nodes']
            edges = data['edges']
        current_file = filename
    for edge in edges:
        for node in nodes: 
            if edge['edge_start']['node'] == node:
                edge['edge_start']['node'] = node
                # edge['edge_start']['node']['fields'] = node['fields']
            if edge['edge_end']['node'] == node:
                edge['edge_end']['node'] = node
                # edge['edge_end']['node']['fields'] = node['fields']

project_open(filename='kg.json')

# ============================================================
# NODES
# ============================================================

def node_create(x, y, w, h, text):
    node = {
        'world_x': x,
        'world_y': y,
        'world_w': w,
        'world_h': h,
        'text': text,
    }
    nodes.append(node)
    return node

def node_width_by_text(node):
    text_width, text_height = font.size(node['text'])
    text_width_scale = text_width * camera['scale']
    text_height_scale = text_height * camera['scale']
    node['world_w'] = text_width_scale
    node['world_h'] = text_height_scale
    node['world_w'] += 10 + 10
    node['world_h'] += 10 + 10

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
    ### Get visible world boundaries
    left, top = screen_to_world(0, 0)
    right, bottom = screen_to_world(screen_w, screen_h)
    ### Find first grid line
    start_x = int(left // grid_size) * grid_size
    start_y = int(top // grid_size) * grid_size
    ### Find last grid line
    end_x = int(right // grid_size + 1) * grid_size
    end_y = int(bottom // grid_size + 1) * grid_size
    ###
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

def draw_edges():
    for edge in edges:
        ### LINE
        node_start_x = edge['edge_start']['node']['world_x']
        node_start_y = edge['edge_start']['node']['world_y']
        node_start_w = edge['edge_start']['node']['world_w']
        node_start_h = edge['edge_start']['node']['world_h']
        node_end_x = edge['edge_end']['node']['world_x']
        node_end_y = edge['edge_end']['node']['world_y']
        node_end_w = edge['edge_end']['node']['world_w']
        node_end_h = edge['edge_end']['node']['world_h']
        node_start_x_mid = node_start_x + (node_start_w // 2)
        node_start_y_mid = node_start_y + (node_start_h // 2)
        node_end_x_mid = node_end_x + (node_end_w // 2)
        node_end_y_mid = node_end_y + (node_end_h // 2)
        edge['world_x1'] = node_start_x_mid
        edge['world_y1'] = node_start_y_mid
        edge['world_x2'] = node_end_x_mid
        edge['world_y2'] = node_end_y_mid
        edge_screen_x1, edge_screen_y1 = world_to_screen(node_start_x_mid, node_start_y_mid)
        edge_screen_x2, edge_screen_y2 = world_to_screen(node_end_x_mid, node_end_y_mid)
        points = [
            (edge_screen_x1, edge_screen_y1),
            (edge_screen_x2, edge_screen_y2),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
        ### RELATIONSHIP TEXT
        edge_center_screen_x = (edge['world_x1'] + edge['world_x2']) // 2
        edge_center_screen_y = (edge['world_y1'] + edge['world_y2']) // 2
        ###
        ### TODO is // camera['scale'] the right way to get font base size? how node text managed bbox?
        text_width, text_height = font.size(edge['edge_relationship'])
        edge['text_world_x1'] = edge_center_screen_x - (text_width // camera['scale']) // 2
        edge['text_world_y1'] = edge_center_screen_y
        edge['text_world_x2'] = edge['text_world_x1'] + (text_width // camera['scale'])
        edge['text_world_y2'] = edge['text_world_y1'] + (text_height // camera['scale'])
        ###
        edge_text_screen_x1, edge_text_screen_y1 = world_to_screen(edge['text_world_x1'], edge['text_world_y1'])
        text = font.render(edge['edge_relationship'], True, (255, 255, 255))
        screen.blit(text, (edge_text_screen_x1, edge_text_screen_y1))
        ###
        if edge == interaction['edge_focus']:
            screen_x = edge_text_screen_x1
            screen_y = edge_text_screen_y1
            screen_w = text_width
            screen_h = text_height
            pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, screen_h), 2*int(camera['scale']))
        # print(json.dumps(edge, indent=4))
        continue
        ### TODO background color on text relationship
        text_width, text_height = font.size(edge['edge_relationship'])
        edge_center_screen_x -= text_width // 2
        edge_center_screen_y -= text_height // 2
        ###
        background_color = (40, 40, 40)
        screen_x = edge_center_screen_x 
        screen_y = edge_center_screen_y
        screen_w = text_width
        screen_h = text_height
        pygame.draw.rect(screen, background_color, (screen_x, screen_y, screen_w, screen_h))
        ###
        ###
        text_width, text_height = font.size(node['text'])
        text_width_scale = text_width * camera['scale']
        text_height_scale = text_height * camera['scale']

def draw_nodes():
    for node in nodes:
        ### RECT
        background_color = (65, 65, 65)
        border_color = (26, 26, 26)
        screen_x, screen_y = world_to_screen(node['world_x'], node['world_y'])
        screen_w = node['world_w'] * camera['scale']
        screen_h = node['world_h'] * camera['scale']
        pygame.draw.rect(screen, background_color, (screen_x, screen_y, screen_w, screen_h))
        pygame.draw.rect(screen, border_color, (screen_x, screen_y, screen_w, screen_h), 1*int(camera['scale']))
        ###
        if node == interaction['node_focus']:
            pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, screen_h), 2*int(camera['scale']))
        ### TEXT
        world_x = node['world_x'] + 10
        world_y = node['world_y'] + 10
        screen_x, screen_y = world_to_screen(world_x, world_y)
        text = font.render(node['text'], True, (255, 255, 255))
        screen.blit(text, (screen_x, screen_y))

################################################################################
# EDGES
################################################################################

def edge_start():
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
            interaction['node_focus'] = node
            interaction['action'] = 'edge'
            interaction['edge_x1'] = mouse['screen_x']
            interaction['edge_y1'] = mouse['screen_y']
            interaction['node_start'] = node
            break

def edge_end():
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
            interaction['node_focus'] = node
            interaction['node_end'] = node
            if interaction['node_start'] == interaction['node_end']: break
            edge = {
                'edge_start': {
                    'node': interaction['node_start'],
                },
                'edge_end': {
                    'node': interaction['node_end'],
                },
                'edge_relationship': '???',
            }
            edges.append(edge)
            # print(edges)
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

"""
x = -200
y = 0
text = 'ozone'
node = node_create(x, y, 0, 0, text)
node_width_by_text(node)

x = 100
y = 0
text = 'o3'
node = node_create(x, y, 0, 0, text)
node_width_by_text(node)
"""


def inputs_mouse_click_right():
    x = mouse['world_x']
    y = mouse['world_y']
    text = '???'
    node = node_create(x, y, 0, 0, text)
    node_width_by_text(node)

def inputs_key_press(event):
    if event.key == pygame.K_ESCAPE:
        core['running'] = False
    # Ctrl+N
    elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
        project_new()
    # Ctrl+S
    elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        project_save()
    # Ctrl+O
    elif event.key == pygame.K_o and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        project_open()
    # Ctrl+D
    elif event.key == pygame.K_d and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        # edge_delete()
        pass
    # Editor
    elif event.key == pygame.K_BACKSPACE:
        if interaction['node_focus'] != None:
            interaction['node_focus']['text'] = interaction['node_focus']['text'][:-1]
            node_width_by_text(interaction['node_focus'])
        elif interaction['edge_focus'] != None:
            # if len(interaction['edge_focus']['edge_relationship']) > 1:
            interaction['edge_focus']['edge_relationship'] = interaction['edge_focus']['edge_relationship'][:-1]
    else:
        if (pygame.K_a <= event.key <= pygame.K_z or 
            pygame.K_0 <= event.key <= pygame.K_9 or 
            event.unicode == '_'
        ):
            letter = event.unicode
            if interaction['node_focus'] != None:
                interaction['node_focus']['text'] += letter
                node_width_by_text(interaction['node_focus'])
            elif interaction['edge_focus'] != None:
                interaction['edge_focus']['edge_relationship'] += letter

def main_inputs():
    global font
    global terms_2_index
    global definitions_focus 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            core['running'] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    edge_start()
                    ####
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
                            interaction['node_focus'] = node
                elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    interaction['node_focus'] = None
                    interaction['field_focus'] = None
                    interaction['field_i_focus'] = None
                    for node in reversed(nodes):
                        if (
                            mouse['world_x'] >= node['world_x'] and 
                            mouse['world_y'] >= node['world_y'] and 
                            mouse['world_x'] <= node['world_x'] + node['world_w'] and 
                            mouse['world_y'] <= node['world_y'] + node['world_h']
                        ):
                            nodes.remove(node)
                            nodes.append(node)
                            interaction['node_focus'] = node
                            interaction['action'] = 'drag_snap'
                            interaction['node_drag'] = node
                            interaction['drag_offset_x'] = mouse['world_x'] - node['world_x']
                            interaction['drag_offset_y'] = mouse['world_y'] - node['world_y']
                            break
                else:
                    for term in lst_terms_lvl2:
                        y = term['y'] - terms_2_index * font_sidebar_size
                        if (
                            mouse['screen_x'] >= term['x'] and 
                            mouse['screen_y'] >= y and 
                            mouse['screen_x'] <= term['x'] + term['w'] and 
                            mouse['screen_y'] <= y + term['h']
                        ):
                            print(term)
                            definitions_focus = term['term_definitions']
                    interaction['node_focus'] = None
                    interaction['edge_focus'] = None
                    for node in reversed(nodes):
                        if (
                            mouse['world_x'] >= node['world_x'] and 
                            mouse['world_y'] >= node['world_y'] and 
                            mouse['world_x'] <= node['world_x'] + node['world_w'] and 
                            mouse['world_y'] <= node['world_y'] + node['world_h']
                        ):
                            nodes.remove(node)
                            nodes.append(node)
                            interaction['node_focus'] = node
                            interaction['action'] = 'drag'
                            interaction['node_drag'] = node
                            interaction['drag_offset_x'] = mouse['world_x'] - node['world_x']
                            interaction['drag_offset_y'] = mouse['world_y'] - node['world_y']
                            break
                    for edge in reversed(edges):
                        pass
                        # print(json.dumps(edge, indent=4))
                        if (
                            mouse['world_x'] >= edge['text_world_x1'] and 
                            mouse['world_y'] >= edge['text_world_y1'] and 
                            mouse['world_x'] <= edge['text_world_x2'] and 
                            mouse['world_y'] <= edge['text_world_y2'] 
                        ):
                            interaction['edge_focus'] = edge
            elif event.button == 2:
                interaction['action'] = 'pan'
                interaction['camera_x_start'] = camera['world_x']
                interaction['camera_y_start'] = camera['world_y']
                interaction['mouse_x_start'] = event.pos[0]
                interaction['mouse_y_start'] = event.pos[1]
            elif event.button == 3:
                inputs_mouse_click_right()

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
            if (
                mouse['screen_x'] > frame_center['x'] and
                mouse['screen_y'] > frame_center['y'] and
                mouse['screen_x'] < frame_center['x'] + frame_center['w'] and
                mouse['screen_y'] < frame_center['y'] + frame_center['h']
            ):
                if event.y == 1:
                    if camera['scale'] < 16:
                        camera['scale'] *= 2
                elif event.y == -1:
                    if camera['scale'] > 1:
                        camera['scale'] /= 2
                font = pygame.font.Font(None, 24*int(camera['scale']))
            elif (
                mouse['screen_x'] > frame_left['x'] and
                mouse['screen_y'] > frame_left['y'] and
                mouse['screen_x'] < frame_left['x'] + frame_left['w'] and
                mouse['screen_y'] < frame_left['y'] + frame_left['h']
            ):
                if event.y == 1:
                    if terms_2_index > 0:
                        terms_2_index -= 1
                elif event.y == -1:
                    terms_2_index += 1

        elif event.type == pygame.KEYDOWN:
            inputs_key_press(event)

    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = screen_to_world(mouse['screen_x'], mouse['screen_y'])

def main_update():
    if interaction['action'] == 'pan':
        dx = mouse['screen_x'] - interaction['mouse_x_start']
        dy = mouse['screen_y'] - interaction['mouse_y_start']
        camera['world_x'] = interaction['camera_x_start'] - dx / camera['scale']
        camera['world_y'] = interaction['camera_y_start'] - dy / camera['scale']

    if interaction['action'] == 'drag':
        interaction['node_drag']['world_x'] = (mouse['world_x'] - interaction['drag_offset_x'])
        interaction['node_drag']['world_y'] = (mouse['world_y'] - interaction['drag_offset_y'])

    if interaction['action'] == 'drag_snap':
        interaction['node_drag']['world_x'] = (mouse['world_x'] - interaction['drag_offset_x']) // 100 * 100
        interaction['node_drag']['world_y'] = (mouse['world_y'] - interaction['drag_offset_y']) // 100 * 100

    clock.tick(60)

def draw_debug():
    i = 1
    offset_x = screen_w - 320
    text = font_debug.render(f"mouse screen x:{mouse['screen_x']} y:{mouse['screen_y']}", True, (255, 0, 255))
    screen.blit(text, (offset_x, 24 * i))
    i += 1
    text = font_debug.render(f"mouse world x:{mouse['world_x']:.2f} y:{mouse['world_y']:.2f}", True, (255, 0, 255))
    screen.blit(text, (offset_x, 24 * i))
    i += 1
    text = font_debug.render(f"camera world x:{camera['world_x']:.2f} y:{camera['world_y']:.2f}", True, (255, 0, 255))
    screen.blit(text, (offset_x, 24 * i))
    i += 1
    text = font_debug.render(f"screen center x:{screen_w // 2} y:{screen_h // 2}", True, (255, 0, 255))
    screen.blit(text, (offset_x, 24 * i))
    i += 1
    text = font_debug.render(f"scale: {camera['scale']}", True, (255, 0, 255))
    screen.blit(text, (offset_x, 24 * i))
    i += 1

def draw_background():
    screen.fill((40, 40, 40))

def lst_item_create(x=0, y=0, w=0, h=0, text='???', term_definitions=[]):
    item = {
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'text': text,
        'term_definitions': term_definitions,
    }
    return item

"""
lst_terms_lvl2 = []
for i in range(100):
    text = f'???{i}'
    x = 0
    y = font_sidebar_size * i
    w, h = font.size(text)
    item = lst_item_create(
        x=x,
        y=y,
        w=w,
        h=h,
        text=text,
    )
    lst_terms_lvl2.append(item)
"""

lst_terms_lvl2 = []
for i, item in enumerate(input_data):
    # for key, value in item.items():
        # print(key)
    # quit()
    # print(json.dumps(item, indent=4))
    # quit()
    term = item['term_name']
    term_definitions = item['term_definitions'][:8]
    text = f'{term}'
    x = 0
    y = font_sidebar_size * i
    w, h = font.size(text)
    item = lst_item_create(
        x=x,
        y=y,
        w=w,
        h=h,
        text=text,
        term_definitions=term_definitions,
    )
    lst_terms_lvl2.append(item)

def draw_lst_item():
    # offset_y_counter = 1
    for i in range(len(lst_terms_lvl2)):
        if i < terms_2_index: continue
        item = lst_terms_lvl2[i]
        # offset_y = 24 * offset_y_counter
        term = item['text']
        x = item['x']
        y = item['y'] - terms_2_index * font_sidebar_size
        if y > frame_left['h']: break
        text = font_sidebar.render(f'{i} - {term}', True, (255, 255, 255))
        screen.blit(text, (x, y))
    return
    ###
    offset_x = 128
    offset_y = 32
    for i, item in enumerate(lst_terms_lvl2):
        term = item['text']
        x = item['x']
        y = item['y']
        text = font_sidebar.render(f'{i} - {term}', True, (255, 255, 255))
        screen.blit(text, (x, y))
    ###
    offset_y_counter = 1
    offset_x = 128
    for i in range(len(input_data)):
        offset_y = 24 * offset_y_counter
        if i < terms_2_index: continue
        offset_y_counter += 1
        if offset_y > screen_h: break
        ###
        input_item = input_data[i]
        term = input_item['term']
        count = input_item['count']
        text = font_sidebar.render(f'{i} - {term}', True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y))

def draw_frame_left():
    global terms_2_index
    frame_x = frame_left['x']
    frame_y = frame_left['y']
    frame_w = frame_left['w']
    frame_h = frame_left['h']
    pygame.draw.rect(screen, (60, 60, 60), (frame_x, frame_y, frame_w, frame_h))
    draw_lst_item()
    return

    list_1 = [
        'ozone',
    ]
    offset_y_counter = 1
    offset_x = 32
    for i in range(len(list_1)):
        offset_y = 24 * offset_y_counter
        offset_y_counter += 1
        if offset_y > screen_h: break
        ###
        input_item = list_1[i]
        term = input_item
        text = font_sidebar.render(f'{term}', True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y))

    # terms_2_index = 0

    offset_y_counter = 1
    offset_x = 128
    for i in range(len(input_data)):
        offset_y = 24 * offset_y_counter
        if i < terms_2_index: continue
        offset_y_counter += 1
        if offset_y > screen_h: break
        ###
        input_item = input_data[i]
        term = input_item['term']
        count = input_item['count']
        text = font_sidebar.render(f'{i} - {term}', True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y))
        # if i > 10: break

    # print(json.dumps(input_data[:10], indent=4))
    # quit()

def draw_frame_bottom():
    frame = frame_bottom
    frame_x = frame['x']
    frame_y = frame['y']
    frame_w = frame['w']
    frame_h = frame['h']
    pygame.draw.rect(screen, (72, 72, 72), (frame_x, frame_y, frame_w, frame_h))
    ###
    for definition_i, definition in enumerate(definitions_focus):
        offset_x = 24
        offset_y = 24 + frame_bottom['y'] + (definition_i * 24)
        text = font_bottom.render(f'{definition}', True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y))

def main_draw():
    draw_background()
    draw_grid()

    if interaction['action'] == 'edge':
        pygame.draw.line(screen, (255, 255, 255), (interaction['edge_x1'], interaction['edge_y1']), (mouse['screen_x'], mouse['screen_y']))

    draw_edges()
    draw_nodes()
    draw_debug()

    draw_frame_left()
    draw_frame_bottom()

    pygame.display.flip()

def main():
    while core['running']:
        main_inputs()
        main_update()
        main_draw()

    pygame.quit()


main()
