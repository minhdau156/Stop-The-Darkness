# Notes

- User is a total beginner in Pygame specifically (knows Python already). Don't over-explain Python syntax; do explain Pygame concepts from scratch.
- Motivation: a school game project. Keep lessons practical/applicable, not theoretical.
- Initial interest: drawing UI, specifically in-game HUD (health bars, score, etc). But ZPD requires window + game loop + basic drawing/text first — HUD is lesson 3+, not lesson 1.
- Quiz convention (per SKILL.md): every answer option same word/character count, no formatting clues.
- **Language**: lessons in Vietnamese (requested 2026-10-03). Keep standard technical terms in English as they appear in real Pygame docs/code (Surface, game loop, event, Sprite, blit, frame, FPS, pygame.draw, pygame.font, HUD, callback, etc.) — only narration/explanations/quiz prompts go in Vietnamese. Matches the user's general teaching-style preference (Vietnamese + English jargon) used in other workspaces (ML, SQL), so carry it forward here by default unless told otherwise.
- **Lesson length**: per general preference, go long/comprehensive per lesson rather than splitting into many thin ones — but each lesson still targets one tangible win.
- Practical exercise required in every lesson (hands-on, not just re-reading), per general preference.

## Roadmap status (2026-10-03)
Full lesson arc toward the 3-week school project is written (Lessons 1-7), plus one optional
polish lesson (8):
1. Window & game loop · 2. Text/fonts · 3. Grid & mouse picking · 4. Resource & HUD ·
5. Build-menu buttons · 6. Unlock rule (adjacency) · 7. Win condition & start/win screens ·
8. (optional) Drawing Tree/Stone icons from primitives, replacing flat-color tiles — user asked
for this specifically after finishing the core-mechanics lessons were generated.
This completes every "Success looks like" item in [[MISSION.md]]; Lesson 8 is pure visual polish,
not a new mechanic, so it doesn't reopen the simplified-scope decision in [[mission-shift-concrete-project]].
Next session: check in on how far the user actually got executing these (they haven't reported
progress/results yet — no learning records exist for demonstrated understanding of Lessons 1-8
content itself, only the mission-shift record). Don't assume completion; ask where they are before
assigning anything past Lesson 8 (further polish ideas: sound, movement/animation, second resource
— all explicitly out-of-scope for now unless asked).
