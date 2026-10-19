"""Stop the Darkness — a clone-with-a-twist of flori9's itch.io game, in Pygame.

Core loop copied from the original: a grid of land tiles, four resources,
click-to-upgrade where the next upgrade depends on neighboring tiles, and a
Stone Circle that can halt and then reverse the spreading darkness.
New on top of the original: a Darkness Wisp that hunts your buildings and
that you must click to kill before it reaches them.
"""

import random

import pygame

# ---------- Config ----------
GRID_COLS = 16
GRID_ROWS = 12
TILE_SIZE = 48
PANEL_W = 190
MSG_BOX_H = 80

GRID_W = GRID_COLS * TILE_SIZE
GRID_H = GRID_ROWS * TILE_SIZE
WINDOW_W = GRID_W + PANEL_W
WINDOW_H = GRID_H + MSG_BOX_H

GRASS_COLOR = (176, 213, 140)
GRASS_DOT_COLOR = (158, 198, 120)
WATER_COLOR = (131, 186, 224)
WATER_LINE_COLOR = (160, 206, 235)
DARKNESS_COLOR = (28, 22, 38)
PANEL_COLOR = (214, 203, 170)
PANEL_BORDER = (120, 108, 80)
MSG_BOX_COLOR = (235, 228, 205)
TEXT_DARK = (60, 48, 30)
GRID_LINE_COLOR = (150, 193, 115)

# Fixed offsets (within a tile) for the grass/water stipple texture.
TEXTURE_DOTS = [(10, 12), (26, 8), (44, 20), (54, 34), (16, 46), (40, 52)]

TICK_FRAMES = 60              # resources produced once per second at 60 FPS
DARKNESS_INTERVAL_FRAMES = 300  # darkness spreads/retreats every 5 seconds
SPREAD_CHANCE = 0.35
RETREAT_PER_INTERVAL = 2
RESEARCH_WIN_TARGET = 150
LOSE_DARKNESS_RATIO = 0.6

WISP_INTERVAL_FRAMES = 900    # a wisp tries to spawn every 15 seconds
WISP_SPEED = 2.5
WISP_CLICK_RADIUS = 18
WISP_KILL_REWARD = {"wood": 5}

START_RESOURCES = {"wood": 10, "stone": 0, "magic": 0, "research": 0}

# ---------- Tile types ----------
FIELD = 0
FOREST = 1
LUMBER_CAMP = 2
STONE = 3
QUARRY = 4
WATER = 5
PORT = 6
MAINPORT = 7
VILLAGE = 8
TOWN = 9
CITY = 10
MAGIC_GROVE = 11
CIRCLE_DORMANT = 12
CIRCLE_AWAKE = 13
CIRCLE_EMPOWERED = 14
DARKNESS = 15

VALUABLE_TARGETS = {
    LUMBER_CAMP, QUARRY, VILLAGE, TOWN, CITY, PORT, MAINPORT, MAGIC_GROVE,
}

# Clicking one of these upgrades it in place (no menu needed).
UPGRADES = {
    FOREST: {"result": LUMBER_CAMP, "cost": {},
              "requires": lambda r, c: True,
              "label": "Claim Forest"},
    STONE: {"result": QUARRY, "cost": {},
             "requires": lambda r, c: True,
             "label": "Claim Stone"},
    VILLAGE: {"result": TOWN, "cost": {"wood": 15, "stone": 10},
               "requires": lambda r, c: has_adjacent_later(r, c, {QUARRY}),
               "label": "Village -> Town"},
    TOWN: {"result": CITY, "cost": {"wood": 20, "stone": 20, "research": 10},
            "requires": lambda r, c: has_adjacent_later(r, c, {TOWN, CITY}),
            "label": "Town -> City"},
    PORT: {"result": MAINPORT, "cost": {"stone": 15, "magic": 15},
            "requires": lambda r, c: port_count_later() >= 3,
            "label": "Port -> Mainport"},
    CIRCLE_DORMANT: {"result": CIRCLE_AWAKE, "cost": {"stone": 30, "magic": 20},
                       "requires": lambda r, c: True,
                       "label": "Awaken Stone Circle"},
    CIRCLE_AWAKE: {"result": CIRCLE_EMPOWERED,
                    "cost": {"stone": 40, "magic": 40, "research": 20},
                    "requires": lambda r, c: True,
                    "label": "Empower Stone Circle"},
}

# Clicking a FIELD tile uses whichever of these is selected in the bottom menu.
FIELD_BUILD_OPTIONS = [
    {"name": "Village", "result": VILLAGE, "cost": {"wood": 10},
     "requires": lambda r, c: has_adjacent_later(r, c, {LUMBER_CAMP})},
    {"name": "Port", "result": PORT, "cost": {"wood": 8},
     "requires": lambda r, c: has_adjacent_later(r, c, {WATER})},
    {"name": "Magic Grove", "result": MAGIC_GROVE, "cost": {"wood": 10, "research": 5},
     "requires": lambda r, c: count_adjacent_later(r, c, {LUMBER_CAMP}) >= 2},
]

PRODUCTION = {
    VILLAGE: {"research": 1},
    TOWN: {"research": 2},
    CITY: {"research": 4},
    PORT: {"magic": 1},
    MAINPORT: {"magic": 3, "research": 2},
    CIRCLE_EMPOWERED: {"research": 2},
}
BOOST_RESOURCE = {LUMBER_CAMP: "wood", QUARRY: "stone", MAGIC_GROVE: "magic"}
BASE_YIELD = {LUMBER_CAMP: 1, QUARRY: 1, MAGIC_GROVE: 2}

RESOURCE_ORDER = ["wood", "stone", "magic", "research"]
RESOURCE_LABELS = {"wood": "Wood", "stone": "Stone", "magic": "Magic", "research": "Research"}

# ---------- State ----------
grid = [[FIELD for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
circle_pos = (GRID_ROWS // 2, GRID_COLS // 2)
resources = dict(START_RESOURCES)
last_tick_rates = {res: 0 for res in RESOURCE_ORDER}
frame_counter = 0
darkness_frame_counter = 0
wisp_frame_counter = 0
wisp = None  # {"x": float, "y": float, "target": (row, col)}
selected_type = 0
message, message_timer = "", 0
win_reason = ""
game_state = "START"  # START -> PLAYING -> WON / LOST

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Stop the Darkness")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)
big_small_font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 46)

start_button = pygame.Rect(WINDOW_W // 2 - 100, WINDOW_H // 2 + 20, 200, 60)
restart_button = pygame.Rect(WINDOW_W // 2 - 100, WINDOW_H // 2 + 20, 200, 60)

PANEL_X = GRID_W
menu_buttons = [
    pygame.Rect(PANEL_X + 10, 346, PANEL_W - 20, 38),
    pygame.Rect(PANEL_X + 10, 392, PANEL_W - 20, 38),
    pygame.Rect(PANEL_X + 10, 438, PANEL_W - 20, 38),
]


# ---------- Grid helpers ----------
def is_valid(row, col):
    return 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS


def pixel_to_tile(pos):
    x, y = pos
    return y // TILE_SIZE, x // TILE_SIZE


def get_neighbors(row, col):
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return [(r, c) for r, c in candidates if is_valid(r, c)]


def has_adjacent_later(row, col, type_set):
    return any(grid[r][c] in type_set for r, c in get_neighbors(row, col))


def count_adjacent_later(row, col, type_set):
    return sum(1 for r, c in get_neighbors(row, col) if grid[r][c] in type_set)


def count_type_on_grid(type_set):
    return sum(1 for row in grid for cell in row if cell in type_set)


def port_count_later():
    return count_type_on_grid({PORT, MAINPORT})


def all_cells():
    return [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS)]


# ---------- Setup ----------
def generate_terrain():
    for row, col in all_cells():
        roll = random.random()
        if roll < 0.12:
            grid[row][col] = WATER
        elif roll < 0.34:
            grid[row][col] = FOREST
        elif roll < 0.50:
            grid[row][col] = STONE
        else:
            grid[row][col] = FIELD

    cr, cc = circle_pos
    grid[cr][cc] = CIRCLE_DORMANT

    corners = [(0, 0), (0, GRID_COLS - 1), (GRID_ROWS - 1, 0), (GRID_ROWS - 1, GRID_COLS - 1)]
    for r, c in corners:
        if (r, c) != circle_pos:
            grid[r][c] = DARKNESS


def reset_game():
    global resources, last_tick_rates, frame_counter, darkness_frame_counter, wisp_frame_counter
    global wisp, selected_type, message, message_timer, win_reason
    resources = dict(START_RESOURCES)
    last_tick_rates = {res: 0 for res in RESOURCE_ORDER}
    frame_counter = 0
    darkness_frame_counter = 0
    wisp_frame_counter = 0
    wisp = None
    selected_type = 0
    message, message_timer = "", 0
    win_reason = ""
    generate_terrain()


# ---------- Economy ----------
def can_afford(cost):
    return all(resources[res] >= amount for res, amount in cost.items())


def spend(cost):
    for res, amount in cost.items():
        resources[res] -= amount


def produce_resources():
    gained = {res: 0 for res in RESOURCE_ORDER}
    for row, col in all_cells():
        tile = grid[row][col]
        if tile in PRODUCTION:
            for res, amount in PRODUCTION[tile].items():
                gained[res] += amount
        if tile in BOOST_RESOURCE:
            boost = count_adjacent_later(row, col, {TOWN}) + 2 * count_adjacent_later(row, col, {CITY})
            gained[BOOST_RESOURCE[tile]] += BASE_YIELD[tile] + boost

    for res, amount in gained.items():
        resources[res] += amount
    last_tick_rates.update(gained)


def set_message(text, frames=90):
    global message, message_timer
    message, message_timer = text, frames


def attempt_build(row, col):
    option = FIELD_BUILD_OPTIONS[selected_type]
    if not option["requires"](row, col):
        set_message(f"Can't build {option['name']} here yet")
    elif not can_afford(option["cost"]):
        set_message(f"Not enough resources for {option['name']}")
    else:
        spend(option["cost"])
        grid[row][col] = option["result"]
        set_message(f"Built {option['name']}!", 60)


def attempt_upgrade(row, col):
    rule = UPGRADES.get(grid[row][col])
    if rule is None:
        set_message("Nothing to upgrade here", 60)
        return
    if not rule["requires"](row, col):
        set_message("Requirements not met yet")
    elif not can_afford(rule["cost"]):
        set_message("Not enough resources")
    else:
        spend(rule["cost"])
        grid[row][col] = rule["result"]
        set_message(f"{rule['label']} done!", 60)


# ---------- Darkness ----------
def update_darkness():
    cr, cc = circle_pos
    circle_state = grid[cr][cc]

    if circle_state == CIRCLE_AWAKE:
        return  # spread is paused, nothing to do

    if circle_state == CIRCLE_EMPOWERED:
        darkness_tiles = [(r, c) for r, c in all_cells() if grid[r][c] == DARKNESS]
        for r, c in random.sample(darkness_tiles, min(RETREAT_PER_INTERVAL, len(darkness_tiles))):
            grid[r][c] = FIELD
        return

    darkness_tiles = [(r, c) for r, c in all_cells() if grid[r][c] == DARKNESS]
    for r, c in darkness_tiles:
        if random.random() < SPREAD_CHANCE:
            candidates = [n for n in get_neighbors(r, c)
                          if grid[n[0]][n[1]] not in (DARKNESS, WATER) and n != circle_pos]
            if candidates:
                nr, nc = random.choice(candidates)
                grid[nr][nc] = DARKNESS


# ---------- Darkness Wisp ----------
def try_spawn_wisp():
    global wisp
    darkness_cells = [(r, c) for r, c in all_cells() if grid[r][c] == DARKNESS]
    targets = [(r, c) for r, c in all_cells() if grid[r][c] in VALUABLE_TARGETS]
    if not darkness_cells or not targets:
        return
    sr, sc = random.choice(darkness_cells)
    target = min(targets, key=lambda rc: abs(rc[0] - sr) + abs(rc[1] - sc))
    wisp = {
        "x": sc * TILE_SIZE + TILE_SIZE / 2,
        "y": sr * TILE_SIZE + TILE_SIZE / 2,
        "target": target,
    }


def update_wisp():
    global wisp
    if wisp is None:
        return
    tr, tc = wisp["target"]
    target_x = tc * TILE_SIZE + TILE_SIZE / 2
    target_y = tr * TILE_SIZE + TILE_SIZE / 2
    dx, dy = target_x - wisp["x"], target_y - wisp["y"]
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance <= WISP_SPEED:
        if grid[tr][tc] in VALUABLE_TARGETS:
            grid[tr][tc] = DARKNESS
        wisp = None
        return

    wisp["x"] += WISP_SPEED * dx / distance
    wisp["y"] += WISP_SPEED * dy / distance


def try_kill_wisp(pos):
    global wisp
    if wisp is None:
        return False
    dx, dy = pos[0] - wisp["x"], pos[1] - wisp["y"]
    if dx ** 2 + dy ** 2 <= WISP_CLICK_RADIUS ** 2:
        wisp = None
        resources["wood"] += WISP_KILL_REWARD["wood"]
        set_message("Wisp destroyed! +5 Wood", 60)
        return True
    return False


# ---------- Icons (simple shapes, one draw call per part) ----------
def draw_tree_icon(x, y, size, color=(60, 150, 70)):
    trunk_w, trunk_h = size // 4, size // 2
    pygame.draw.rect(screen, (90, 60, 40), (x - trunk_w // 2, y - trunk_h, trunk_w, trunk_h))
    pygame.draw.circle(screen, color, (x, y - trunk_h), size // 2)


def draw_stone_icon(x, y, size, color=(140, 140, 145)):
    points = [
        (x - size // 2, y), (x - size // 3, y - size // 3),
        (x, y - size // 2), (x + size // 3, y - size // 3), (x + size // 2, y),
    ]
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, (95, 95, 100), points, width=2)


def draw_house_icon(x, y, size, roof_color=(170, 70, 60)):
    wall_h = size // 2
    pygame.draw.rect(screen, (200, 170, 120), (x - size // 2, y - wall_h, size, wall_h))
    roof_points = [(x - size // 2 - 4, y - wall_h), (x, y - size), (x + size // 2 + 4, y - wall_h)]
    pygame.draw.polygon(screen, roof_color, roof_points)


def draw_port_icon(x, y, size, flags=1):
    pygame.draw.rect(screen, (120, 90, 60), (x - size // 2, y - size // 6, size, size // 6))
    for i in range(flags):
        pole_x = x - size // 4 + i * size // 2
        pygame.draw.line(screen, (90, 60, 40), (pole_x, y - size // 6), (pole_x, y - size), 3)
        pygame.draw.polygon(screen, (200, 60, 60), [
            (pole_x, y - size), (pole_x + size // 4, y - size + size // 6), (pole_x, y - size + size // 4),
        ])


def draw_magic_icon(x, y, size):
    pygame.draw.circle(screen, (130, 80, 200), (x, y - size // 3), size // 3)
    pygame.draw.circle(screen, (200, 160, 255), (x, y - size // 3), size // 3, width=2)


def draw_circle_icon(x, y, size, color):
    pygame.draw.circle(screen, color, (x, y - size // 3), size // 2, width=4)
    pygame.draw.circle(screen, color, (x, y - size // 3), size // 5)


def draw_wood_resource_icon(x, y, size):
    pygame.draw.circle(screen, (139, 94, 52), (x, y), size // 2)
    pygame.draw.circle(screen, (178, 130, 80), (x, y), size // 3)
    pygame.draw.circle(screen, (139, 94, 52), (x, y), size // 6)


def draw_stone_resource_icon(x, y, size):
    draw_stone_icon(x, y + size // 3, size, (150, 150, 155))


def draw_magic_resource_icon(x, y, size):
    pygame.draw.circle(screen, (150, 100, 210), (x, y), size // 2)
    pygame.draw.circle(screen, (210, 180, 255), (x, y), size // 2, width=2)


def draw_research_icon(x, y, size):
    top_w, bottom_w, height = size // 4, size // 2, size // 2
    neck = (x - top_w // 2, y - height, top_w, height // 3)
    pygame.draw.rect(screen, (190, 190, 195), neck)
    body_points = [
        (x - top_w // 2, y - height + height // 3), (x + top_w // 2, y - height + height // 3),
        (x + bottom_w // 2, y + size // 4), (x - bottom_w // 2, y + size // 4),
    ]
    pygame.draw.polygon(screen, (120, 200, 130), body_points)
    pygame.draw.polygon(screen, (90, 90, 95), body_points, width=2)


RESOURCE_ICON_DRAWERS = {
    "wood": draw_wood_resource_icon,
    "stone": draw_stone_resource_icon,
    "magic": draw_magic_resource_icon,
    "research": draw_research_icon,
}


ICON_DRAWERS = {
    FOREST: lambda x, y, size: draw_tree_icon(x, y, size, (35, 95, 45)),
    LUMBER_CAMP: lambda x, y, size: draw_tree_icon(x, y, size, (70, 190, 85)),
    STONE: lambda x, y, size: draw_stone_icon(x, y, size, (90, 90, 95)),
    QUARRY: lambda x, y, size: draw_stone_icon(x, y, size, (170, 170, 175)),
    VILLAGE: lambda x, y, size: draw_house_icon(x, y, size),
    TOWN: lambda x, y, size: draw_house_icon(x, y, int(size * 1.2), (200, 110, 60)),
    CITY: lambda x, y, size: draw_house_icon(x, y, int(size * 1.4), (220, 180, 60)),
    PORT: lambda x, y, size: draw_port_icon(x, y, size, 1),
    MAINPORT: lambda x, y, size: draw_port_icon(x, y, int(size * 1.3), 2),
    MAGIC_GROVE: lambda x, y, size: draw_magic_icon(x, y, size),
    CIRCLE_DORMANT: lambda x, y, size: draw_circle_icon(x, y, size, (120, 120, 130)),
    CIRCLE_AWAKE: lambda x, y, size: draw_circle_icon(x, y, size, (90, 160, 220)),
    CIRCLE_EMPOWERED: lambda x, y, size: draw_circle_icon(x, y, size, (250, 210, 90)),
}


# ---------- Drawing ----------
def draw_button(rect, label, color=(70, 70, 90)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, width=2)
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=rect.center))


def draw_grid():
    for row, col in all_cells():
        x, y = col * TILE_SIZE, row * TILE_SIZE
        cell = grid[row][col]

        if cell == WATER:
            pygame.draw.rect(screen, WATER_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            for dx, dy in TEXTURE_DOTS[:3]:
                pygame.draw.line(screen, WATER_LINE_COLOR, (x + dx, y + dy), (x + dx + 10, y + dy), 2)
        elif cell == DARKNESS:
            pygame.draw.rect(screen, DARKNESS_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, GRASS_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            for dx, dy in TEXTURE_DOTS:
                pygame.draw.circle(screen, GRASS_DOT_COLOR, (x + dx, y + dy), 2)

        pygame.draw.rect(screen, GRID_LINE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), width=1)

        drawer = ICON_DRAWERS.get(cell)
        if drawer:
            drawer(x + TILE_SIZE // 2, y + TILE_SIZE - 8, TILE_SIZE - 24)


def draw_hover():
    row, col = pixel_to_tile(pygame.mouse.get_pos())
    if not is_valid(row, col):
        return
    rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (250, 250, 250), rect, width=2)


def circle_state_lines():
    state = grid[circle_pos[0]][circle_pos[1]]
    if state == CIRCLE_DORMANT:
        return "Dormant", "Need 30 Stone, 20 Magic"
    if state == CIRCLE_AWAKE:
        return "Awakened - halted", "Need 40S 40M 20R"
    return "Empowered!", "Darkness retreating"


def draw_panel():
    pygame.draw.rect(screen, PANEL_COLOR, (PANEL_X, 0, PANEL_W, WINDOW_H))
    pygame.draw.line(screen, PANEL_BORDER, (PANEL_X, 0), (PANEL_X, WINDOW_H), 2)

    for i, res in enumerate(RESOURCE_ORDER):
        row_y = 14 + i * 42
        RESOURCE_ICON_DRAWERS[res](PANEL_X + 26, row_y + 18, 28)
        amount = big_small_font.render(str(resources[res]), True, TEXT_DARK)
        screen.blit(amount, (PANEL_X + 52, row_y + 4))
        rate = font.render(f"+{last_tick_rates[res]}", True, (90, 110, 70))
        screen.blit(rate, (PANEL_X + 52, row_y + 24))

    dark_count = count_type_on_grid({DARKNESS})
    line1 = font.render(f"Darkness: {dark_count}", True, TEXT_DARK)
    screen.blit(line1, (PANEL_X + 14, 200))
    line2 = font.render(f"Goal: {resources['research']}/{RESEARCH_WIN_TARGET}", True, TEXT_DARK)
    screen.blit(line2, (PANEL_X + 14, 222))

    pygame.draw.line(screen, PANEL_BORDER, (PANEL_X + 10, 246), (WINDOW_W - 10, 246), 1)
    header = font.render("Stone Circle", True, TEXT_DARK)
    screen.blit(header, (PANEL_X + 14, 252))
    state_line, hint_line = circle_state_lines()
    screen.blit(font.render(state_line, True, TEXT_DARK), (PANEL_X + 14, 274))
    screen.blit(font.render(hint_line, True, (100, 90, 70)), (PANEL_X + 14, 294))

    pygame.draw.line(screen, PANEL_BORDER, (PANEL_X + 10, 322), (WINDOW_W - 10, 322), 1)
    build_label = font.render("Build on Field:", True, TEXT_DARK)
    screen.blit(build_label, (PANEL_X + 14, 328))

    for i, option in enumerate(FIELD_BUILD_OPTIONS):
        rect = menu_buttons[i]
        cost_str = " ".join(f"{amt}{res[0].upper()}" for res, amt in option["cost"].items())
        pygame.draw.rect(screen, (190, 178, 145), rect)
        border = (60, 48, 30) if i == selected_type else (150, 138, 105)
        pygame.draw.rect(screen, border, rect, width=3 if i == selected_type else 1)
        label = font.render(f"{option['name']} ({cost_str})", True, TEXT_DARK)
        screen.blit(label, label.get_rect(center=rect.center))


def draw_message_box():
    rect = (0, GRID_H, GRID_W, MSG_BOX_H)
    pygame.draw.rect(screen, MSG_BOX_COLOR, rect)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=2)

    text = message if message_timer > 0 else "Click Forest/Stone to claim it. Click Field to build."
    label = font.render(text, True, TEXT_DARK)
    screen.blit(label, (14, GRID_H + 14))


def draw_wisp():
    if wisp is None:
        return
    x, y = int(wisp["x"]), int(wisp["y"])
    pygame.draw.circle(screen, (60, 15, 80), (x, y), 14)
    pygame.draw.circle(screen, (255, 255, 255), (x - 5, y - 3), 3)
    pygame.draw.circle(screen, (255, 255, 255), (x + 5, y - 3), 3)


# ---------- Win / lose checks ----------
def check_game_over():
    global game_state, win_reason
    dark_count = count_type_on_grid({DARKNESS})
    circle_state = grid[circle_pos[0]][circle_pos[1]]

    if resources["research"] >= RESEARCH_WIN_TARGET:
        game_state, win_reason = "WON", "research"
    elif circle_state == CIRCLE_EMPOWERED and dark_count == 0:
        game_state, win_reason = "WON", "darkness"
    elif dark_count >= LOSE_DARKNESS_RATIO * (GRID_ROWS * GRID_COLS):
        game_state = "LOST"


# ---------- Main loop ----------
reset_game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START" and start_button.collidepoint(event.pos):
                game_state = "PLAYING"

            elif game_state == "PLAYING":
                if try_kill_wisp(event.pos):
                    continue

                clicked_menu = False
                for i, rect in enumerate(menu_buttons):
                    if rect.collidepoint(event.pos):
                        selected_type = i
                        clicked_menu = True
                        break

                if not clicked_menu:
                    row, col = pixel_to_tile(event.pos)
                    if is_valid(row, col):
                        if grid[row][col] == FIELD:
                            attempt_build(row, col)
                        else:
                            attempt_upgrade(row, col)

            elif game_state in ("WON", "LOST") and restart_button.collidepoint(event.pos):
                reset_game()
                game_state = "PLAYING"

    if game_state == "PLAYING":
        if message_timer > 0:
            message_timer -= 1

        frame_counter += 1
        if frame_counter >= TICK_FRAMES:
            frame_counter = 0
            produce_resources()

        darkness_frame_counter += 1
        if darkness_frame_counter >= DARKNESS_INTERVAL_FRAMES:
            darkness_frame_counter = 0
            update_darkness()

        if wisp is None:
            wisp_frame_counter += 1
            if wisp_frame_counter >= WISP_INTERVAL_FRAMES:
                wisp_frame_counter = 0
                try_spawn_wisp()
        update_wisp()

        check_game_over()

    screen.fill(GRASS_COLOR)

    if game_state == "START":
        title = big_font.render("STOP THE DARKNESS", True, TEXT_DARK)
        screen.blit(title, title.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 60)))
        subtitle = font.render("Upgrade tiles, awaken the Stone Circle, push back the dark",
                                True, (70, 90, 55))
        screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 20)))
        draw_button(start_button, "Start")

    elif game_state == "PLAYING":
        draw_grid()
        draw_hover()
        draw_wisp()
        draw_panel()
        draw_message_box()

    elif game_state == "WON":
        text = "Research Victory!" if win_reason == "research" else "You pushed back the Darkness!"
        msg = big_font.render(text, True, (40, 110, 50))
        screen.blit(msg, msg.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 60)))
        draw_button(restart_button, "Play Again")

    elif game_state == "LOST":
        msg = big_font.render("The Darkness consumed your land...", True, (120, 30, 30))
        screen.blit(msg, msg.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 60)))
        draw_button(restart_button, "Try Again")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
