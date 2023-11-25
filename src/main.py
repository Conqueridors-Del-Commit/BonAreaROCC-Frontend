import csv
from datetime import datetime, timedelta

import OpenGL.GLUT.fonts

import map
from graphic import *
from customer import *
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

alpha_angle = 45.0
beta_angle = 30.0
radius = 450
multi = 0.60
speed_multipliers = [-500, -100, -10, -1, 1, 10, 100, 500, 1000]
speed_mult_index = 4
table_scroll = 0


def convert_to_datetime(date_string):
    try:
        # Parse the input date string into a datetime object
        datetime_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return datetime_object
    except ValueError:
        # Handle the case where the input string is not in the expected format
        print("Invalid date format. Please provide a date string in the format 'YYYY-MM-DD HH:MM:SS'")
        return None


def read_path_csv(filename):
    with open(filename, "r", errors="ignore", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        distinct_customers = []
        for row in reader:
            if row['customer_id'] not in distinct_customers:
                distinct_customers.append(row['customer_id'])

    customers = []
    for customer_id in distinct_customers:
        with open(filename, "r", errors="ignore", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")

            movements = []
            picking = []
            timestamps = []

            total_articles = []
            for r in reader:
                if r['customer_id'] == customer_id:
                    ticket_id = r['ticket_id']
                    movements.append((int(r['x']), int(r['y'])))
                    if r['picking'] == '1':
                        if (int(r['x']), int(r['y'])) not in total_articles:
                            total_articles.append((int(r['x']), int(r['y'])))
                        picking.append(True)
                    else:
                        picking.append(False)
                    timestamps.append(convert_to_datetime(r['x_y_date_time']))
            customers.append(
                Customer(customer_id, ticket_id, movements, picking, timestamps, total_articles=len(total_articles)))
    return customers


def read_store_csv(filename):
    with open(filename, "r", errors="ignore", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        grid = []
        max_width = 0
        max_height = 0
        for row in reader:
            if int(row['x']) > max_height:
                max_height = int(row['x'])
            if int(row['y']) > max_width:
                max_width = int(row['y'])
            if row['description'] == "almacen":
                representation = "a"
            elif row['description'] == "paso":
                representation = "-"
            elif row['description'] == "paso-entrada":
                representation = "n"
            elif row['description'] == "paso-salida":
                representation = "s"
            elif row['description'] == "escaleras":
                representation = "e"
            elif row['description'] == "cestas":
                representation = "c"
            elif row['description'].startswith('caja'):
                representation = "j"
            else:
                representation = "p"
            grid.append(map.Node(int(row['x']),
                                 int(row['y']),
                                 row['description'],
                                 representation))
    storemap = map.Map(max_width, max_height, grid)
    with open(filename, "r", errors="ignore", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            if r['picking_x'] != '':
                pick_x = int(r['picking_x'])
                pick_y = int(r['picking_y'])
                node = storemap.get_node_by_coordinates(pick_x, pick_y)
                node.picking_neighbour_x = int(r['x'])
                node.picking_neighbour_y = int(r['y'])
                storemap.set_node_by_coordinates(pick_x, pick_y, node)
    return storemap


def write_store_map(store_map: map.Map):
    print("#" * (store_map.width + 2))
    for x in range(1, store_map.height + 1):
        print("#", end="")
        for y in range(1, store_map.width + 1):
            try:
                print(store_map.get_node_by_coordinates(x, y).representation, end="")
            except AttributeError:
                print("-", end="")
        print("#")
    print("#" * (store_map.width + 2))


def graphics_procedure(store_map):
    global customers_data, current_time
    for x in range(1, store_map.height + 1):
        for y in range(1, store_map.width + 1):
            node = store_map.get_node_by_coordinates(x, y)
            height = 0
            if node.representation == "a":
                color = (0.2, 0.2, 0.2)
                height = 2
            elif node.representation == "p":
                color = (0.5, 0.1, 0.1)
                height = 2
            elif node.representation == "e":
                color = (0.1, 0.1, 0.9)
                height = 0
            elif node.representation == "c":
                color = (0.9, 0.1, 0.1)
                height = 1
            elif node.representation == "j":
                color = (0.1, 0.9, 0.1)
                height = 1
            else:
                color = (0.9, 0.9, 0.9)
                height = 0
            if height != 0:
                draw_prism((x * SQUARE_SIZE, 0, y * SQUARE_SIZE),
                           (SQUARE_SIZE, SQUARE_SIZE * height, SQUARE_SIZE),
                           color)
            else:
                draw_rectangle((x * SQUARE_SIZE, 0, y * SQUARE_SIZE), (SQUARE_SIZE, 0, SQUARE_SIZE),
                               color)
    for customer in customers_data:
        if customer.active:
            draw_prism((customer.current_x * SQUARE_SIZE, 0, customer.current_y * SQUARE_SIZE),
                       (SQUARE_SIZE, math.ceil(SQUARE_SIZE * 1.5), SQUARE_SIZE),
                       (0.0, 0.0, 1.0))
        if customer.picking_rn:
            if customer.active:
                draw_prism(
                    (customer.current_pick_x * SQUARE_SIZE, SQUARE_SIZE * 3, customer.current_pick_y * SQUARE_SIZE),
                    (SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    (0.0, 1.0, 0.0))
                draw_prism(
                    (customer.current_pick_x * SQUARE_SIZE + math.floor(SQUARE_SIZE / 4), 0,
                     customer.current_pick_y * SQUARE_SIZE + math.floor(SQUARE_SIZE / 4)),
                    (math.floor(SQUARE_SIZE / 2), SQUARE_SIZE * 3, math.floor(SQUARE_SIZE / 2)),
                    (0.0, 1.0, 0.0))

    glLoadIdentity()

    word = current_time.strftime('%Y-%m-%d %H:%M:%S')
    draw_text(word, (-400, 300), True)
    draw_text("Speed: ", (320, 300))
    draw_text(f"{speed_multipliers[speed_mult_index]}x", (400, 300), True)

    # Dibuixar la table
    glLoadIdentity()
    # glPushMatrix()
    # glTranslatef(XOFFSET, 0, ZOFFSET)
    # glRotatef(-90.0, 1.0, 0.0, 0.0)
    # glRotatef(90.0 - alpha_angle, 0.0, 0.0, 1.0)
    # glScalef(0.5, 0.5, 0.5)
    # glTranslatef(-105 * 0.5, 0.0, 0.0)
    # glTranslatef(0.0, 0.0, 100.0)
    # glRotatef(90 - beta_angle, 1.0, 0.0, 0.0)
    draw_prism((0, -470, 180), (1200, 300, 20), (0.2, 0.2, 0.2))
    draw_prism((0, -510, 200), (1200, 300, 20), (1.0, 1.0, 1.0))
    # glPopMatrix()

    draw_header("Estado Ruta", (-470, -200), True)
    draw_header("Nº Cliente", (-350, -200), True)
    draw_header("Hora Entrada", (-250, -200), True)
    draw_header("Hora Salida", (-120, -200), True)
    draw_header("Duración", (0, -200), True)
    draw_header("Nº Tiquet", (100, -200), True)
    draw_header("Cantidad de artículos", (200, -200), True)

    for i, customer in enumerate(customers_data[table_scroll:]):
        # 4 estats: Espera, En Ruta, Picking, Completat
        if not customer.active and not customer.completed:
            draw_semaphore((-470, -210 - 20 * (i + 1)), (240, 76, 70))
            draw_table_text("Espera", (-440, -210 - 20 * (i + 1)))
        elif not customer.active:
            draw_semaphore((-470, -210 - 20 * (i + 1)), (27, 227, 110))
            draw_table_text("Completo", (-440, -210 - 20 * (i + 1)))
        elif customer.active and customer.picking_rn:
            draw_semaphore((-470, -210 - 20 * (i + 1)), (255, 225, 83))
            draw_table_text("Picking", (-440, -210 - 20 * (i + 1)))
        elif customer.active and not customer.picking_rn:
            draw_semaphore((-470, -210 - 20 * (i + 1)), (39, 158, 242))
            draw_table_text("En ruta", (-440, -210 - 20 * (i + 1)))
        draw_table_text(customer.customer_id, (-350, -210 - 20 * (i + 1)))
        draw_table_text(customer.timestamps[0].strftime("%H:%M:%S"), (-250, -210 - 20 * (i + 1)))
        draw_table_text(customer.timestamps[-1].strftime("%H:%M:%S"), (-120, -210 - 20 * (i + 1)))
        draw_table_text(str(customer.timestamps[-1] - customer.timestamps[0])[:8], (0, -210 - 20 * (i + 1)))
        draw_table_text(customer.ticket_id, (100, -210 - 20 * (i + 1)))
        draw_table_text(f"{customer.picked_articles} ({customer.total_articles})", (200, -210 - 20 * (i + 1)))


def displayFunc():
    global store_map, alpha_angle, beta_angle, multi, radius
    idleFunc()

    glClearColor(0.54, 0.8, 0.98, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    position_observer(alpha_angle, beta_angle, radius)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WIDTH * multi, WIDTH * multi, -HEIGHT * multi, HEIGHT * multi, -100, 2000)

    glMatrixMode(GL_MODELVIEW)

    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_LINE)

    graphics_procedure(store_map)

    glutSwapBuffers()


def keyboardFunc(key, x, y):
    global alpha_angle, beta_angle, multi, speed_mult_index, table_scroll, customers_data
    t = key.decode()
    if t == "w":
        beta_angle = min(80.0, beta_angle + 5)
    elif t == "s":
        beta_angle = max(10.0, beta_angle - 5)
    if t == "a":
        alpha_angle = (alpha_angle + 5) % 360.0
    elif t == "d":
        alpha_angle = (alpha_angle - 5) % 360.0
    elif t == "e":
        if len(customers_data) > 8:
            table_scroll = min(len(customers_data) - 8, table_scroll + 1)
        else:
            pass
    elif t == "q":
        table_scroll = max(0, table_scroll - 1)
    elif t == "z":
        speed_mult_index = max(0, speed_mult_index - 1)
    elif t == "c":
        speed_mult_index = min(len(speed_multipliers) - 1, speed_mult_index + 1)
    elif t == "x":
        speed_mult_index = 4


def idleFunc():
    global current_time, last_update, customers_data, store_map
    elapsed_ms = glutGet(GLUT_ELAPSED_TIME)
    elapsed_time = elapsed_ms - last_update
    if elapsed_time > abs(1000 / speed_multipliers[speed_mult_index]):
        last_update = elapsed_ms
        for _ in range(math.floor(elapsed_time / abs(1000 / speed_multipliers[speed_mult_index]))):
            if speed_multipliers[speed_mult_index] < 0:
                current_time = current_time - timedelta(seconds=1)
            else:
                current_time = current_time + timedelta(seconds=1)
            t2 = (
                current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute,
                current_time.second)
            for customer in customers_data:
                for i, timestamp in enumerate(customer.timestamps):
                    t1 = (
                        timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                        timestamp.second)
                    if t1 == t2:
                        customer.active = True
                        customer.current_x = customer.movements[i][0]
                        customer.current_y = customer.movements[i][1]
                        if customer.picking[i]:
                            if not customer.picking_rn and speed_multipliers[speed_mult_index] > 0:
                                customer.picked_articles += 1
                            customer.picking_rn = True
                            customer_node = store_map.get_node_by_coordinates(customer.current_x, customer.current_y)
                            customer.current_pick_x = customer_node.picking_neighbour_x
                            customer.current_pick_y = customer_node.picking_neighbour_y
                        else:
                            if customer.picking_rn and speed_multipliers[speed_mult_index] < 0:
                                customer.picked_articles -= 1
                            customer.picking_rn = False
                        break
                else:
                    if customer.active:
                        customer.active = False
                        customer.completed = True
                    customer.active = False


if __name__ in "__main__":
    customers_data = read_path_csv('output_utf.csv')
    store_map = read_store_csv('planogram_utf.csv')
    t = 0
    last_update = 0
    current_time = convert_to_datetime('2023-11-02 09:00:00')
    # write_store_map(store_map)
    init_graphics()
    glutDisplayFunc(displayFunc)
    glutIdleFunc(displayFunc)
    glutKeyboardFunc(keyboardFunc)
    glutMainLoop()
