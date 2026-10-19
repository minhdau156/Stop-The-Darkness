# main.py — Code Explanation

This file explains how `main.py` works, section by section, with line references.

## Overview (lines 1-12)

The game is "Stop the Darkness," built with Pygame. It is a tile-upgrade game.
The player claims and upgrades tiles on a grid. The player must stop a spreading
darkness. A roaming enemy, the Darkness Wisp, adds extra pressure.

## Config constants (lines 14-52)

These constants set the grid size, tile pixel size, colors, and timing rules.

- `GRID_COLS`, `GRID_ROWS`, `TILE_SIZE`: grid dimensions in tiles and pixels.
- `PANEL_W`, `MSG_BOX_H`: sizes of the side panel and the bottom message box.
- `TICK_FRAMES = 60`: resources are produced once per second (60 frames at 60 FPS).
- `DARKNESS_INTERVAL_FRAMES = 300`: darkness spreads or retreats every 5 seconds.
- `SPREAD_CHANCE = 0.35`: each darkness tile has a 35% chance to spread per interval.
- `RESEARCH_WIN_TARGET = 150`: Research needed to win by research.
- `LOSE_DARKNESS_RATIO = 0.6`: losing if 60% of tiles turn to darkness.
- `WISP_*` constants: control how often a Wisp spawns, its speed, and its reward.
- `START_RESOURCES`: resources the player starts with.

## Tile types (lines 54-74)

Each tile type is an integer constant (`FIELD`, `FOREST`, `WATER`, etc.).
`VALUABLE_TARGETS` lists the tile types a Darkness Wisp will chase.

## Upgrade rules (lines 76-121)

- `UPGRADES`: a dict. The key is the current tile type. The value holds the
  result tile, the resource cost, and a `requires` function that checks a
  condition (for example, "must be next to a Quarry").
- `FIELD_BUILD_OPTIONS`: a list of 3 buildings the player can place on a
  `FIELD` tile. The player picks one from the side panel before clicking.
- `PRODUCTION`: tiles that generate a fixed amount of a resource each tick
  (for example, a Village makes 1 Research per second).
- `BOOST_RESOURCE` and `BASE_YIELD`: tiles whose output also increases when a
  Town or City sits next to them (Lumber Camp, Quarry, Magic Grove).

## Game state (lines 126-156)

Global variables hold the live game state: the `grid` (2D list of tile
types), `resources` (dict of amounts), frame counters for ticking logic,
the current Wisp (or `None`), and `game_state` (`START`, `PLAYING`, `WON`,
or `LOST`). Pygame is initialized here, and the window, clock, and fonts
are created.

## Grid helper functions (lines 159-191)

Small utility functions used throughout the file:

- `is_valid`: checks a row/col is inside the grid.
- `pixel_to_tile`: converts a mouse pixel position to a grid cell.
- `get_neighbors`: returns the up/down/left/right neighbor cells.
- `has_adjacent_later` / `count_adjacent_later`: check neighbor tile types.
  Used by the `requires` rules in `UPGRADES` and `FIELD_BUILD_OPTIONS`.
- `count_type_on_grid`, `port_count_later`: count tiles of given types
  anywhere on the grid (used for the Mainport upgrade requirement).

## Setup (lines 194-228)

- `generate_terrain`: randomly fills the grid with Water, Forest, Stone, or
  Field, places the Stone Circle in the center, and scatters a few starting
  Darkness tiles on the border.
- `reset_game`: resets all state back to the starting values and calls
  `generate_terrain`. Used both at game start and after Win/Loss restart.

## Economy functions (lines 231-286)

- `can_afford` / `spend`: check and subtract resource costs.
- `produce_resources`: runs once per second. Adds up output from every
  `PRODUCTION` tile and every `BOOST_RESOURCE` tile, then updates `resources`
  and `last_tick_rates` (shown in the panel as "+N" per resource).
- `set_message`: shows a temporary message in the bottom message box.
- `attempt_build`: handles clicking a `FIELD` tile — checks the selected
  build option's requirement and cost, then places the building.
- `attempt_upgrade`: handles clicking any other upgradeable tile — looks up
  the rule in `UPGRADES`, checks requirement and cost, then upgrades it.

## Darkness logic (lines 289-310)

`update_darkness` runs every 5 seconds and depends on the Stone Circle state:

- **Dormant**: each Darkness tile has a 35% chance to spread into a random
  non-water, non-darkness neighbor (the Circle tile itself is protected).
- **Awakened**: spreading is paused — the function returns immediately.
- **Empowered**: darkness retreats — up to 2 random Darkness tiles revert
  to `FIELD` each interval.

## Darkness Wisp logic (lines 313-359)

- `try_spawn_wisp`: picks a random Darkness tile as a start point and the
  nearest valuable building as a target, then creates the `wisp` dict.
- `update_wisp`: moves the Wisp toward its target each frame. If it reaches
  the target, that tile turns into Darkness and the Wisp disappears.
- `try_kill_wisp`: called on mouse click. If the click lands within
  `WISP_CLICK_RADIUS` of the Wisp, it dies and the player gets a Wood reward.

## Drawing functions (lines 362-561)

This section has no game logic — it only draws shapes to the screen.

- `draw_*_icon` functions: draw simple geometric icons (tree, stone, house,
  port, magic orb, resource icons, Stone Circle) using basic Pygame shapes.
- `ICON_DRAWERS` / `RESOURCE_ICON_DRAWERS`: dicts that map a tile type or
  resource name to its drawing function, so the render loop can look up the
  right icon instead of using long if/else chains.
- `draw_grid`: draws every tile's background color, texture dots, grid
  lines, and icon.
- `draw_hover`: draws a white outline around the tile under the mouse.
- `draw_panel`: draws the right-side panel — resource counts and rates,
  darkness count, research goal, Stone Circle status, and the 3 build
  option buttons.
- `draw_message_box`: draws the bottom message bar.
- `draw_wisp`: draws the Wisp as a small dark circle with two white "eyes."

## Win/lose check (lines 564-574)

`check_game_over` runs every frame during play and sets `game_state` to
`WON` (by reaching the Research target, or by an empty, Empowered map) or
`LOST` (if Darkness covers 60%+ of the grid).

## Main loop (lines 577-666)

The classic Pygame loop structure:

1. **Event handling**: reads mouse clicks and the quit event. Behavior
   depends on `game_state`:
   - `START`: clicking the Start button begins play.
   - `PLAYING`: a click first tries to kill the Wisp, then checks the build
     menu buttons, then falls back to building or upgrading the clicked tile.
   - `WON` / `LOST`: clicking Restart calls `reset_game` and returns to
     `PLAYING`.
2. **Update step** (only while `PLAYING`): counts down the message timer,
   ticks `produce_resources` once per second, ticks `update_darkness` every
   5 seconds, spawns and moves the Wisp, and checks for game over.
3. **Draw step**: clears the screen, then draws the correct screen for the
   current `game_state` (title screen, play screen, win screen, or lose
   screen).
4. `pygame.display.flip()` shows the frame, and `clock.tick(60)` caps the
   loop at 60 FPS.

The loop ends when `running` becomes `False` (window closed), and
`pygame.quit()` cleans up.
