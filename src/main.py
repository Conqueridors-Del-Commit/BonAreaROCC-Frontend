import csv
import map
import graphic


def read_path_csv(filename):
    with open(filename, "r", errors="ignore", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            print(row)


def read_store_csv(filename):
    with open(filename, "r", errors="ignore", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        grid = []
        print(reader.fieldnames)
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
                                 representation,
                                 []))
    return map.Map(max_width, max_height, grid)


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


if __name__ in "__main__":
    # read_path_csv('output_utf.csv')
    store_map = read_store_csv('planogram_utf.csv')
    # write_store_map(store_map)ç
    graphic.init_graphics()
