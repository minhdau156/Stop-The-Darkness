# Team Workload Split (4 members, 10 days)

Context: everyone is a Pygame/Python beginner, this is the first game project for the
whole team. Two members are mostly covering the documentation and the slide deck, so
their coding workload is kept lighter — but still real, isolated pieces they can own
end-to-end.

Scope = exactly the 8 lesson topics: game loop/window, text & fonts, grid & mouse
picking, resources & HUD, build-menu buttons, unlock rule (adjacency), win condition &
screens, icon drawing with primitives.

## Roles

### You / Member A — Core & Rules (integration lead)
- Lesson 1: game loop & window setup → build the shared skeleton everyone else plugs into
- Lesson 6: unlock rule / adjacency logic
- Lesson 7: win/lose condition & screen switching
- Also responsible for merging everyone's code together at the end

### Member B — Gameplay systems
- Lesson 2: text/fonts helper
- Lesson 3: grid & mouse picking
- Lesson 4: resources & HUD display

### Member C — Build menu (+ writes the document)
- Lesson 5: build-menu buttons (fairly self-contained: draw buttons, detect clicks,
  trigger a callback)

### Member D — Icons/art (+ makes the slides)
- Lesson 8: drawing icons with primitives (shapes/colors for each building type)

## Why this split

A and B own the two halves of the game that must talk to each other constantly
(engine/rules vs. grid/resources), so it makes sense for one of them to be the
integrator. C and D get the two most visually/logically isolated pieces — a button
component and some icon-drawing functions — so they can build and test them almost
standalone before plugging in. That keeps their coding time low without making their
contribution trivial (a teacher can clearly see what they wrote).

## 10-day plan (to avoid merge conflicts with 4 beginners)

1. **Day 1–2** — Member A writes a minimal shared skeleton: one `main.py` with the game
   loop, a `GameState` object (dict/class holding grid, resources, screen state), and
   empty stub functions for grid, HUD, build menu, icons. Push it so everyone branches
   off the same starting point.
2. **Day 3–6** — Everyone builds their piece in a separate branch/file against that
   shared `GameState`, so no one blocks anyone else.
3. **Day 7–8** — Member A (integrator) merges all branches into `main.py`, fixes the
   seams.
4. **Day 9** — Everyone playtests together, fixes bugs found in their own module.
5. **Day 10** — Buffer + docs/slides finalized, submit.
