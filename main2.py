import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
running = True
score = 0


GRID_COLS = 16
GRID_ROWS = 12
TILE_SIZE = 40  # mỗi ô vuông 80x80 pixel



# grid[row][col] = 0 nghĩa là ô trống; sẽ dùng số khác cho "đã xây" ở bài sau
grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

def draw_grid(screen, grid):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            rect = (x, y, TILE_SIZE, TILE_SIZE)
            
            rect1 = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            border_color = (20, 20, 20)
            
            if grid[row][col] == 0:
                color = (50, 70, 50)      # ô trống — xanh rêu tối
            else:
                color = (160, 120, 60) # ô đã xây — nâu đất
            
            if rect1.collidepoint(pygame.mouse.get_pos()):
                border_color = (255, 255, 255)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, border_color, rect, width=2)  # viền ô, width=2 nghĩa là chỉ vẽ viền, không tô đặc

def pixel_to_tile(pos):
    x, y = pos
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    return row, col

def count_tile_in_grid(grid):
    tile_create = 0
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if (grid[row][col] == 1):
                tile_create += 1
    return tile_create

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            row, col = pixel_to_tile(event.pos)
            
            # chặn trường hợp bấm ngoài lưới (ví dụ cửa sổ rộng hơn lưới)
            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                grid[row][col] = 1 if grid[row][col] == 0 else 0  # bật/tắt ô
    screen.fill((30, 30, 40))
    draw_grid(screen, grid)
    
    
    count = count_tile_in_grid(grid)
    text_surface_2 = font.render(f"Tile Created: {count}", True, (255, 255, 255))
    text_rect_2 = text_surface_2.get_rect(topright=(780, 20))
    screen.blit(text_surface_2, text_rect_2)
    
    # hover_row, hover_col = pixel_to_tile(pygame.mouse.get_pos())
    # if 0 <= hover_row < GRID_ROWS and 0 <= hover_col < GRID_COLS:
    #     pygame.draw.rect(screen, (255, 255, 255), (hover_col * TILE_SIZE, hover_row * TILE_SIZE, TILE_SIZE, TILE_SIZE), width=2)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()