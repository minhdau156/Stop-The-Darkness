# Pygame Resources

## Knowledge

- [A Newbie Guide to pygame (official pygame.org docs)](https://www.pygame.org/docs/tut/newbieguide.html)
  The official starting point. Use for: setup, core concepts, the mental model behind surfaces/display/events.
- [Pygame: A Primer on Game Programming in Python (Real Python)](https://realpython.com/pygame-a-primer/)
  High-quality, well-tested walkthrough of the game loop, sprites, and collision. Use for: the canonical game loop structure and why each step exists.
- [Work with text — Pygame tutorial (pygame.readthedocs.io)](https://pygame.readthedocs.io/en/latest/4_text/text.html)
  Focused reference on `pygame.font`: creating fonts, rendering text to a Surface, blitting it. Use for: any HUD text (score, timers, labels).
- [pygame.draw official API docs](https://www.pygame.org/docs/ref/draw.html)
  Canonical reference for `draw.rect`, `draw.circle`, `draw.line`, etc. Use for: health bars, buttons, HUD backgrounds — anything drawn as a shape rather than an image.
- [pygame.Surface official API docs](https://www.pygame.org/docs/ref/surface.html)
  Reference for Surface methods (`blit`, `fill`, `convert_alpha`). Use for: understanding what a Surface actually is, since the whole UI model is "draw onto surfaces, blit surfaces onto the screen."
- [pygame.event official API docs](https://www.pygame.org/docs/ref/event.html)
  Use for: `MOUSEBUTTONDOWN`/`MOUSEBUTTONUP` and other event types beyond `QUIT`.
- [pygame.mouse official API docs](https://www.pygame.org/docs/ref/mouse.html)
  Use for: `get_pos()` — polling current mouse position outside the event queue (needed for hover highlights).
- [pygame.Rect official API docs](https://www.pygame.org/docs/ref/rect.html)
  Use for: `collidepoint()`, `.center`, and other Rect helpers — the basis of the button/click-region pattern used for the build menu and start/restart buttons.
- [pygame.time official API docs](https://www.pygame.org/docs/ref/time.html)
  Use for: `Clock.tick()` semantics, and as the jumping-off point for delta-time once the frame-counting shortcut (used for simplicity under the deadline) needs upgrading.
- [pygame.draw official docs](https://www.pygame.org/docs/ref/draw.html) + [Drawing graphics primitives (Pygame tutorial)](https://pygame.readthedocs.io/en/latest/2_draw/draw.html)
  Use for: `polygon()` signature/behavior — basis of composing simple original icons (tree, stone) from primitives instead of loading external art.

## Wisdom (Communities)

- [r/pygame](https://reddit.com/r/pygame)
  Active, beginner-friendly subreddit specifically for Pygame. Use for: code review, "why doesn't this work," project feedback.
- [Pygame community Discord (linked from pygame.org)](https://www.pygame.org/wiki/info)
  Real-time help channel. Use for: fast troubleshooting when stuck mid-project.

## Gaps

- No single authoritative source for "HUD design" specifically — HUD lessons will need to be synthesized from font + draw + Surface docs above rather than cited from one canonical tutorial. Flag this in HUD lessons: more citations, less single-source authority.
