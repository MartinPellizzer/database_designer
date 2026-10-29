import os
import json
import pygame
import subprocess

pygame.init()

screen_w = 1600
screen_h = 900

screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

core = {
    'running': True,
}


current_file = None

row_h = 2

camera = {
    'world_x': 0,
    'world_y': 0,
    'scale': 16,
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
    'drag_offset_x': 0,
    'drag_offset_y': 0,
    'camera_x_start': 0,
    'camera_y_start': 0,
    'mouse_x_start': 0,
    'mouse_y_start': 0,
    'button_visible': False,
}

font_size_base = 1
font_comment_size_base = 16

font = pygame.font.Font(None, font_size_base*int(camera['scale']))
font_debug = pygame.font.Font(None, 24)
font_ui = pygame.font.Font(None, 16)
font_comment = pygame.font.Font(None, font_comment_size_base*int(camera['scale']))

frame_left = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': screen_h,
}

frame_center = {
    'x': 0 + frame_left['x'],
    'y': 0,
    'w': screen_w - frame_left['w'],
    'h': screen_h,
}

menu_context = {
    'name': 'viewport',
    'x': 0,
    'y': 0,
    'items': [
        {'name': 'Add Node'},
        {'name': 'Add Comment'},
    ]
}
menu_context_visible = False

nodes = []

def button_create(text):
    item = {
        'screen_x': 0,
        'screen_y': 0,
        'screen_w': 100,
        'screen_h': 24,
        'text': text,
    }
    return item

button_1 = button_create('Add Node')
button_2 = button_create('Add Comment')

buttons = []
buttons.append(button_1)
buttons.append(button_2)

# ============================================================
# NODES
# ============================================================

def node_create(x, y, w, h, title, kind, description, fields):
    types_allowed = ['data', 'linking', 'subset', 'validation']
    '''
    DESCRIPTION GUIDELINES: Write 1 short sentence explaining WHAT is this table (definition) and 1 short sentence explaining WHY this table is important.
    '''
    node_id_last = -1
    for node in nodes:
        if node_id_last < node['id']: node_id_last = node['id']
    node_id_new = node_id_last + 1
    node = {
        'id': node_id_new,
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

    ### RECT
    screen_x, screen_y = world_to_screen(node['world_x'], node['world_y'])
    screen_w = node['world_w'] * camera['scale']
    screen_h = row_h * (len(node['fields'])+1) * camera['scale']
    pygame.draw.rect(screen, background_color, (screen_x, screen_y, screen_w, screen_h))

    ### TITLE RECT
    title_screen_h = row_h * camera['scale']
    pygame.draw.rect(screen, (0, 128, 0), (screen_x, screen_y, screen_w, title_screen_h))

    ### OUTLINE
    screen_h = row_h * (len(node['fields'])+1) * camera['scale']
    pygame.draw.rect(screen, border_color, (screen_x, screen_y, screen_w, screen_h), 1*int(camera['scale']//8))

    # SELECTED
    if node == interaction['node_focus'] and interaction['field_focus'] == 'title':
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, title_screen_h), 2*int(camera['scale']//8))
    elif node == interaction['node_focus'] and interaction['field_i_focus'] != None:
        pygame.draw.rect(
            screen, (0, 0, 255), 
            (screen_x, screen_y + title_screen_h*interaction['field_i_focus'], screen_w, title_screen_h), 
            2*int(camera['scale']//8)
        )
    elif node == interaction['node_focus']:
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_w, screen_h), 2*int(camera['scale']//8))

    ### TEXT TITLE
    world_x = node['world_x'] + 0.75
    world_y = node['world_y'] + 0.75
    screen_x, screen_y = world_to_screen(world_x, world_y)
    text = font.render(node['title'], True, (255, 255, 255))
    screen.blit(text, (screen_x, screen_y))

    ### TEXT FIELDS
    i = 0
    for field in node['fields']:
        i += 1
        world_x = node['world_x'] + 0.75
        world_y = node['world_y'] + 0.75 + (i * row_h)
        screen_x, screen_y = world_to_screen(world_x, world_y)

        text = font.render(field['name'], True, (255, 255, 255))
        screen.blit(text, (screen_x, screen_y))

        world_x = node['world_x'] + node['world_w'] - 2
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
    if filename == '':
        ### LINUX
        filename = os.path.dirname(os.path.abspath(__file__)) + '/uncategorized'
        filename = os.path.dirname(os.path.abspath(__file__)) + '/terrawhisper'
        filename = subprocess.run(
            [
                "zenity",
                "--file-selection",
                f"--filename={filename}",
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
                edge['edge_start']['node']['fields'] = node['fields']
            if edge['edge_end']['node'] == node:
                edge['edge_end']['node'] = node
                edge['edge_end']['node']['fields'] = node['fields']

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
                    if interaction['node_start'] == interaction['node_end']:
                        break
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

"""
x = 0
y = 0
w = 20
h = 0
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
    'edge_type': '1:N',
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
edges.append(edge_1)
# edges.append(edge_2)
"""

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
    if 'edge_type' not in edge: edge['edge_type'] = '1:N'

    ### DRAW 1:N
    if edge['edge_type'] == '1:N':
        line_start_x = node_start_x
        line_start_y = node_start_y
        line_end_x = node_end_x
        line_end_y = node_end_y
        if node_start_x < node_end_x:
            line_start_x1 = line_start_x + 2
            line_start_y1 = line_start_y + 1
            line_start_x2 = line_start_x + 2
            line_start_y2 = line_start_y - 1
            line_end_x1_1 = line_end_x - 2
            line_end_y1_1 = line_end_y
            line_end_x2_1 = line_end_x
            line_end_y2_1 = line_end_y + 1
            line_end_x1_2 = line_end_x - 2
            line_end_y1_2 = line_end_y
            line_end_x2_2 = line_end_x
            line_end_y2_2 = line_end_y - 1
        else:
            line_start_x1 = line_start_x - 20
            line_start_y1 = line_start_y + 10
            line_start_x2 = line_start_x - 20
            line_start_y2 = line_start_y - 10
            line_end_x1_1 = line_end_x + 20
            line_end_y1_1 = line_end_y
            line_end_x2_1 = line_end_x
            line_end_y2_1 = line_end_y + 10
            line_end_x1_2 = line_end_x + 20
            line_end_y1_2 = line_end_y
            line_end_x2_2 = line_end_x
            line_end_y2_2 = line_end_y - 10
        ### TODO
        screen_line_start_x1, screen_line_start_y1 = world_to_screen(line_start_x1, line_start_y1)
        screen_line_start_x2, screen_line_start_y2 = world_to_screen(line_start_x2, line_start_y2)
        screen_line_end_x1_1, screen_line_end_y1_1 = world_to_screen(line_end_x1_1, line_end_y1_1)
        screen_line_end_x2_1, screen_line_end_y2_1 = world_to_screen(line_end_x2_1, line_end_y2_1)
        screen_line_end_x1_2, screen_line_end_y1_2 = world_to_screen(line_end_x1_2, line_end_y1_2)
        screen_line_end_x2_2, screen_line_end_y2_2 = world_to_screen(line_end_x2_2, line_end_y2_2)
        points = [
            (screen_line_start_x1, screen_line_start_y1),
            (screen_line_start_x2, screen_line_start_y2),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
        points = [
            (screen_line_end_x1_1, screen_line_end_y1_1),
            (screen_line_end_x2_1, screen_line_end_y2_1),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
        points = [
            (screen_line_end_x1_2, screen_line_end_y1_2),
            (screen_line_end_x2_2, screen_line_end_y2_2),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
    ### RELATIONSHIP TEXT
    text = font.render(edge['edge_type'], True, (255, 255, 255))
    screen.blit(text, (screen_x2, (screen_y2 + screen_y3) / 2))

    ### DRAW 1:1
    if edge['edge_type'] == '1:1':
        line_start_x = node_start_x
        line_start_y = node_start_y
        line_end_x = node_end_x
        line_end_y = node_end_y
        if node_start_x < node_end_x:
            line_start_x1 = line_start_x + 20
            line_start_y1 = line_start_y + 10
            line_start_x2 = line_start_x + 20
            line_start_y2 = line_start_y - 10
            line_end_x1 = line_end_x - 20
            line_end_y1 = line_end_y + 10
            line_end_x2 = line_end_x - 20
            line_end_y2 = line_end_y - 10
        else:
            line_start_x1 = line_start_x - 20
            line_start_y1 = line_start_y + 10
            line_start_x2 = line_start_x - 20
            line_start_y2 = line_start_y - 10
            line_end_x1 = line_end_x + 20
            line_end_y1 = line_end_y + 10
            line_end_x2 = line_end_x + 20
            line_end_y2 = line_end_y - 10
        ### TODO
        screen_line_start_x1, screen_line_start_y1 = world_to_screen(line_start_x1, line_start_y1)
        screen_line_start_x2, screen_line_start_y2 = world_to_screen(line_start_x2, line_start_y2)
        screen_line_end_x1, screen_line_end_y1 = world_to_screen(line_end_x1, line_end_y1)
        screen_line_end_x2, screen_line_end_y2 = world_to_screen(line_end_x2, line_end_y2)
        points = [
            (screen_line_start_x1, screen_line_start_y1),
            (screen_line_start_x2, screen_line_start_y2),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
        points = [
            (screen_line_end_x1, screen_line_end_y1),
            (screen_line_end_x2, screen_line_end_y2),
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points)
    ### RELATIONSHIP TEXT
    text = font.render(edge['edge_type'], True, (255, 255, 255))
    screen.blit(text, (screen_x2, (screen_y2 + screen_y3) / 2))

def inputs_key_down(event):
    global nodes
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

    # Ctrl+Q
    elif event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        print('################################################################')
        for node in nodes:
            print(json.dumps(node, indent=4))
            print('---')
        print('------------------------------------------------------------------')
        for node in nodes:
            print(json.dumps(node, indent=4))
            print('---')
        print('################################################################')

    # Ctrl+G -> Generate SQL
    elif event.key == pygame.K_g and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        sql_all = []
        for node in nodes:
            print(json.dumps(node, indent=4))
            table_name = node['title']
            sql_fields = []
            for field in node['fields']:
                sql_field = ''
                if field['key'] == 'primary_key':
                    sql_field = f'''{field['name']} INTEGER PRIMARY KEY'''
                else:
                    sql_field = f'''{field['name']} TEXT'''
                sql_fields.append(sql_field)
            sql_fields = ',\n'.join(sql_fields)
            sql = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {sql_fields}
                );
            '''
            def format_sql(sql):
                lines = sql.strip().splitlines()
                result = []
                indent = 0
                for line in lines:
                    line = line.strip()
                    if line.endswith(")"):
                        indent -= 1
                    result.append("    " * indent + line)
                    if line.endswith("("):
                        indent += 1
                return "\n".join(result)
            sql = format_sql(sql)
            sql_all.append(sql)
        print(sql_all)
        with open(f'sql_output.txt', 'w') as f: 
            for sql in sql_all:
                sql_format = f'{sql.strip()}\n\n'
                f.write(sql_format)

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
            node = interaction['node_focus']
            if i < len(node['fields'])-1:
                node = interaction['node_focus']
                node['fields'][i], node['fields'][i+1] = node['fields'][i+1], node['fields'][i]
                interaction['field_i_focus'] = i + 2
    # Ctrl+RIGHT
    elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL:
        if interaction['field_i_focus'] != None:
            i = interaction['field_i_focus']
            node = interaction['node_focus']
            print(i)
            for edge in edges:
                found = False
                if not found:
                    if edge['edge_end']['node'] == node and edge['edge_end']['field_i'] == i:
                        found = True
                        print('here 1')
                if not found:
                    if edge['edge_start']['node'] == node and edge['edge_start']['field_i'] == i:
                        found = True
                        print('here 2')
                if found:
                    if edge['edge_type'] == '1:1':
                        edge['edge_type'] = '1:N'
                    elif edge['edge_type'] == '1:N':
                        edge['edge_type'] = 'M:N'
                    elif edge['edge_type'] == 'M:N':
                        edge['edge_type'] = '1:1'
                    break
        else:
            interaction['node_focus']['world_w'] += 10
    # Ctrl+LEFT
    elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
        if interaction['field_i_focus'] != None:
            pass
        else:
            interaction['node_focus']['world_w'] -= 10
    # Ctrl+DELETE
    elif event.key == pygame.K_DELETE and pygame.key.get_mods() & pygame.KMOD_CTRL:
        print('delete')
        if interaction['node_focus'] != None:
            nodes = [node for node in nodes if node["id"] != interaction['node_focus']['id']]
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
        if (pygame.K_a <= event.key <= pygame.K_z or 
            pygame.K_0 <= event.key <= pygame.K_9 or 
            event.unicode == '_'
        ):
            letter = event.unicode
            if interaction['node_focus'] != None:
                if interaction['field_focus'] == 'title':
                    interaction['node_focus']['title'] += letter
                else:
                    if interaction['field_i_focus'] != None:
                        i = interaction['field_i_focus']-1
                        interaction['node_focus']['fields'][i]['name'] += letter

def inputs_mouse_wheel(event):
    global font
    global font_comment
    if event.y == 1:
        if camera['scale'] < 256:
            camera['scale'] *= 2
    elif event.y == -1:
        if camera['scale'] > 1:
            camera['scale'] /= 2
    font = pygame.font.Font(None, font_size_base*int(camera['scale']))
    font_comment = pygame.font.Font(None, font_comment_size_base*int(camera['scale']))

def menu_context_open():
    global menu_context_visible
    menu_context_visible = True
    menu_context['x'] = mouse['screen_x']
    menu_context['y'] = mouse['screen_y']
    return

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

def node_create_from_mouse():
    x = mouse['world_x']
    y = mouse['world_y']
    w = 20
    h = 0
    title = 'table_name'
    kind = 'data'
    description = ''
    fields = [
        {'name': 'id', 'key': 'none'}, 
        {'name': 'name', 'key': 'none'}, 
    ]
    node_create(x, y, w, h, title, kind, description, fields)

comments = []

def comment_create(world_x, world_y, text):
    item = {
        'world_x': world_x,
        'world_y': world_y,
        'text': text,
    }
    comments.append(item)

def comment_create_from_mouse():
    x = mouse['world_x']
    y = mouse['world_y']
    title = 'comment'
    comment_create(x, y, title)

def main_inputs():
    global font
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            core['running'] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    edge_start()
                    ####
                    interaction['node_focus'] = None
                    interaction['field_focus'] = None
                    interaction['field_i_focus'] = None
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
                            if (
                                mouse['world_x'] >= node['world_x'] and 
                                mouse['world_y'] >= node['world_y'] and 
                                mouse['world_x'] <= node['world_x'] + node['world_w']//2 and 
                                mouse['world_y'] <= node['world_y'] + row_h
                            ):
                                interaction['field_focus'] = 'title'
                                break
                elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    interaction['node_focus'] = None
                    interaction['field_focus'] = None
                    interaction['field_i_focus'] = None
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
                            interaction['action'] = 'drag_snap'
                            interaction['node_drag'] = node
                            interaction['drag_offset_x'] = mouse['world_x'] - node['world_x']
                            interaction['drag_offset_y'] = mouse['world_y'] - node['world_y']
                            break
                else:
                    ### CONTEXT MENU (buttons)
                    if interaction['button_visible'] == True:
                        interaction['button_visible'] = False
                        for item in buttons:
                            if (
                                mouse['screen_x'] >= item['screen_x'] and 
                                mouse['screen_y'] >= item['screen_y'] and 
                                mouse['screen_x'] <= item['screen_x'] + item['screen_w'] and 
                                mouse['screen_y'] <= item['screen_y'] + item['screen_h']
                            ):
                                if item['text'] == 'Add Node':
                                    node_create_from_mouse()
                                elif item['text'] == 'Add Comment':
                                    comment_create_from_mouse()
                        
                    interaction['node_focus'] = None
                    interaction['field_focus'] = None
                    interaction['field_i_focus'] = None
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
                for i, item in enumerate(buttons):
                    item['screen_x'] = mouse['screen_x']
                    item['screen_y'] = mouse['screen_y'] + (24 * i)
                interaction['button_visible'] = True
                # menu_context_open()

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
            inputs_mouse_wheel(event)

        elif event.type == pygame.KEYDOWN:
            inputs_key_down(event)

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

def draw_background():
    screen.fill((40, 40, 40))

def draw_edge_tmp():
    if interaction['action'] == 'edge':
        pygame.draw.line(screen, (255, 255, 255), (interaction['edge_x1'], interaction['edge_y1']), (mouse['screen_x'], mouse['screen_y']))

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

def draw_frame_left():
    frame_x = frame_left['x']
    frame_y = frame_left['y']
    frame_w = frame_left['w']
    frame_h = frame_left['h']
    pygame.draw.rect(screen, (60, 60, 60), (frame_x, frame_y, frame_w, frame_h))
    ###
    i = 1
    if interaction['node_focus'] != None:
        node_id = interaction['node_focus']['id']
        offset_x = 32
        text = font_debug.render(f"node_id: {node_id}", True, (255, 0, 255))
        screen.blit(text, (offset_x, 24 * i))

def draw_viewport_menu_context():
    if menu_context_visible == True:
        padding = 8
        gap = 24
        ### RECT
        x = menu_context['x']
        y = menu_context['y']
        w = 100
        font_w, font_h = font_ui.size('test text')
        h = 0
        h = h + font_h
        h = h + (padding * 2)
        h = h + (gap * (len(menu_context['items'])-1))
        color_gray = 60
        pygame.draw.rect(screen, (color_gray, color_gray, color_gray), (x, y, w, h))
        ### TEXT
        i = 0
        for item in menu_context['items']:
            x = menu_context['x'] + padding
            y = menu_context['y'] + (gap * i) + padding
            name = item['name']
            text = font_ui.render(f"{name}", True, (255, 255, 255))
            screen.blit(text, (x, y))
            i += 1

def draw_button():
    if interaction['button_visible'] == True:
        screen_x = button_1['screen_x']
        screen_y = button_1['screen_y']
        screen_w = button_1['screen_w']
        screen_h = button_1['screen_h']
        color_gray = 60
        pygame.draw.rect(screen, (color_gray, color_gray, color_gray), (screen_x, screen_y, screen_w, screen_h))
        ### TEXT
        padding = 6 
        text = button_1['text']
        text_surface = font_ui.render(f"{text}", True, (255, 255, 255))
        screen.blit(text_surface, (screen_x + padding, screen_y + padding))

def draw_buttons():
    if interaction['button_visible'] == True:
        for item in buttons:
            screen_x = item['screen_x']
            screen_y = item['screen_y']
            screen_w = item['screen_w']
            screen_h = item['screen_h']
            color_gray = 60
            pygame.draw.rect(screen, (color_gray, color_gray, color_gray), (screen_x, screen_y, screen_w, screen_h))
            ### TEXT
            padding = 6 
            text = item['text']
            text_surface = font_ui.render(f"{text}", True, (255, 255, 255))
            screen.blit(text_surface, (screen_x + padding, screen_y + padding))

def draw_comments():
    for item in comments:
        world_x = item['world_x']
        world_y = item['world_y']
        text = item['text']
        screen_x, screen_y = world_to_screen(world_x, world_y)
        text_surface = font_comment.render(f"{text}", True, (255, 255, 255))
        screen.blit(text_surface, (screen_x, screen_y))

def main_draw():
    draw_background()

    draw_grid()

    draw_edge_tmp()

    for edge in edges:
        draw_edge(edge)

    for node in nodes:
        draw_node(node)
    
    draw_frame_left()

    draw_viewport_menu_context()

    draw_debug()

    # draw_button()
    draw_buttons()
    draw_comments()


    pygame.display.flip()

def main():
    project_open(filename=f'/home/ubuntu/proj/database_designer/terrawhisper/databases.json')

    ### MANUAL UPDATES
    '''
    for node in nodes:
        node_id_last = -1
        for _node in nodes:
            try: 
                if node_id_last < _node['id']: 
                    node_id_last = _node['id']
            except: break
        node_id_new = node_id_last + 1
        node['id'] = node_id_new
    '''

    '''
    for i, node in enumerate(nodes):
        node['id'] = i
    '''

    ### RUNNING
    while core['running']:
        main_inputs()
        main_update()
        main_draw()

        clock.tick(60)

    pygame.quit()

main()
