# Mission: Pygame UI for a School Game Project

## Why
The user needs to build a game for a school project in Python, using Pygame, due in **3 weeks**
(target: around 2026-10-24). They are a total beginner with Pygame specifically (though they know
Python). They were inspired by a browser tile-based building/resource-management game (place
buildings on a grid, unlock new buildings based on adjacent tiles, manage a resource economy, win
conditions) and want to build their **own original game** with a similar core mechanic — same
genre of gameplay, their own theme/art/names, simplified in scope. HUD/UI was the original itch
(health bars, score, timers) and stays the throughline: this genre of game lives or dies on clear
resource counters, a build-menu UI, and tile/selection feedback, so UI skills apply directly
rather than being a side quest.

## Success looks like
- Can open a Pygame window and run a correct game loop without copying boilerplate blindly, and render text/shapes as UI every frame (**done** — Lessons 1–2).
- Can render a 2D grid of clickable tiles and detect which tile the mouse clicked.
- Can track simple game state (one resource, a few building types, what's built where) and reflect it live in a HUD (resource counter, build-menu buttons, tile highlight on hover).
- Can implement one simple unlock rule (e.g. building X only placeable next to an already-built Y) — just one rule, not a full adjacency web.
- Can add a minimal win condition and a start/win screen with a clickable button.
- Can explain *why* each piece works, not just recite it — this still matters even under the deadline.

## Constraints
- Total beginner in Pygame (knows Python itself).
- **Hard deadline: 3 weeks** (~2026-10-24). Pacing must fit this — favor "working and simple" over "complete and faithful to the inspiration game."
- Sessions happen incrementally; keep each lesson small enough to finish in one sitting.
- **2026-10-17 scope change**: user asked to clone the actual reference game (flori9's "Stop the Darkness" on itch.io) instead of building a loosely-inspired original, plus add one new mechanic not in the source. This **supersedes** the 2026-10-03 simplified-scope and "original, not a clone" decisions below. Accepted risk: closer scope with ~1 week left. `main.py` now implements: 4 resources (wood/stone/magic/research), adjacency-gated tile upgrades, a Stone Circle that halts then reverses spreading darkness, 2 win conditions (research threshold, darkness cleared), a lose condition (darkness overruns the map), and a new Darkness Wisp enemy (roams toward a building, destroys it on arrival, player can click to kill it) as the "little different" addition. Simplifications vs. the original: no flood-fill water bodies (Mainport just needs 3 Ports anywhere), no Extended Mode, ~3 building tiers instead of the original's ~15.
- ~~User explicitly chose the simplified scope over a close clone when asked (2026-10-03): one resource type, a handful of buildings, one unlock rule, one win condition.~~ Superseded above.
- ~~Build an original game ... not a clone of the reference game's content or branding.~~ Superseded above.

## Out of scope
- The original's full building tree (~15 tiers), true flood-fill water bodies for Mainport, and Extended Mode (3 more win conditions) — explicitly cut for the 1-week deadline even under the closer-clone scope.
- Advanced rendering (OpenGL, shaders, pygame-ce specific extensions) — not needed for a school project.
- Networking/multiplayer.
- Sprite-sheet/tilemap asset pipelines — plain shapes/colors are enough for tiles and buildings unless the user later asks for art assets.
