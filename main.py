import pygame
import random
import math

# Pygame kutubxonasini ishga tushirish
pygame.init()

# Telefon ekrani o'lchamlarini olish
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyberpunk Ping Pong")

# Ranglar palitrasi
BG_COLOR = (8, 8, 20)
CYAN = (0, 255, 247)
MAGENTA = (255, 0, 128)
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
DARK_PANEL = (15, 15, 35)

# O'yin va boshqaruv maydoni nisbati
PLAY_HEIGHT = HEIGHT - int(WIDTH * 0.32)

# Raketka (Paddle) parametrlar
PADDLE_WIDTH = int(WIDTH * 0.045)
PADDLE_HEIGHT = int(PLAY_HEIGHT * 0.17)
player_x = int(WIDTH * 0.05)
player_y = PLAY_HEIGHT // 2 - PADDLE_HEIGHT // 2
player_speed = 0

# To'p parametrlar
BALL_SIZE = int(WIDTH * 0.05)
ball_x = WIDTH // 2
ball_y = PLAY_HEIGHT // 2
ball_dx = 9 * random.choice((1, -1))
ball_dy = 9 * random.choice((1, -1))

# Vizual effektlar
particles = []
ball_trail = []
shockwaves = []
shake_amount = 0
grid_offset = 0

# Arka fon yulduzlari
stars = [[random.randint(0, WIDTH), random.randint(0, PLAY_HEIGHT), random.uniform(1, 3)] for _ in range(40)]

# Hisob va shriftlar
score = 0
combo = 1
font_score = pygame.font.SysFont("sans-serif", int(WIDTH * 0.1), bold=True)
font_combo = pygame.font.SysFont("sans-serif", int(WIDTH * 0.045), bold=True)

# Boshqaruv tugmalari (Pastki panel)
btn_size = int(WIDTH * 0.22)
btn_y = PLAY_HEIGHT + (HEIGHT - PLAY_HEIGHT - btn_size) // 2
btn_up = pygame.Rect(int(WIDTH * 0.08), btn_y, btn_size, btn_size)
btn_down = pygame.Rect(WIDTH - int(WIDTH * 0.08) - btn_size, btn_y, btn_size, btn_size)

# Zarrachalar effekti
def add_particles(x, y, color, count=18):
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(3, 10)
        particles.append({
            'x': x, 'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'color': color,
            'life': random.randint(15, 25),
            'max_life': 25
        })

# To'lqin effekti
def add_shockwave(x, y, color):
    shockwaves.append({'x': x, 'y': y, 'radius': 5, 'max_radius': 60, 'color': color, 'alpha': 255})

clock = pygame.time.Clock()
running = True

# ASOSIY O'YIN TSIKLI
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Ekran bosilganda tugmalarni tekshirish
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if btn_up.collidepoint(pos):
                player_speed = -14
            elif btn_down.collidepoint(pos):
                player_speed = 14
                
        # Ekrandan qo'l olinganda to'xtash
        if event.type == pygame.MOUSEBUTTONUP:
            player_speed = 0

    # Raketka harakati
    player_y += player_speed
    if player_y < 0:
        player_y = 0
    if player_y > PLAY_HEIGHT - PADDLE_HEIGHT:
        player_y = PLAY_HEIGHT - PADDLE_HEIGHT

    # To'p harakati
    ball_x += ball_dx
    ball_y += ball_dy

    # To'p izini saqlash
    ball_trail.append((ball_x + BALL_SIZE // 2, ball_y + BALL_SIZE // 2))
    if len(ball_trail) > 10:
        ball_trail.pop(0)

    # Yuqori va pastki devorlarga urilish
    if ball_y <= 0 or ball_y >= PLAY_HEIGHT - BALL_SIZE:
        ball_dy *= -1
        shake_amount = 6
        add_particles(ball_x + BALL_SIZE // 2, ball_y + BALL_SIZE // 2, CYAN)
        add_shockwave(ball_x + BALL_SIZE // 2, ball_y + BALL_SIZE // 2, CYAN)

    # O'ng devorga urilish
    if ball_x >= WIDTH - BALL_SIZE:
        ball_x = WIDTH - BALL_SIZE
        ball_dx *= -1
        shake_amount = 8
        add_particles(ball_x, ball_y + BALL_SIZE // 2, MAGENTA)
        add_shockwave(ball_x, ball_y + BALL_SIZE // 2, MAGENTA)

    # Raketkaga urilish
    player_rect = pygame.Rect(player_x, player_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

    if ball_rect.colliderect(player_rect):
        ball_x = player_x + PADDLE_WIDTH
        ball_dx *= -1.05
        ball_dy *= 1.05
        score += 10 * combo
        combo += 1
        shake_amount = 12
        add_particles(ball_x, ball_y + BALL_SIZE // 2, YELLOW, count=25)
        add_shockwave(ball_x, ball_y + BALL_SIZE // 2, YELLOW)

    # O'yinda yutqazish (To'p chap tomondan chiqib ketsa)
    if ball_x < 0:
        shake_amount = 18
        add_particles(ball_x + 30, ball_y + BALL_SIZE // 2, MAGENTA, count=35)
        ball_x = WIDTH // 2
        ball_y = PLAY_HEIGHT // 2
        ball_dx = 9 * random.choice((1, -1))
        ball_dy = 9 * random.choice((1, -1))
        score = 0
        combo = 1

    # Ekran tebranishi
    render_offset_x = random.randint(-shake_amount, shake_amount) if shake_amount > 0 else 0
    render_offset_y = random.randint(-shake_amount, shake_amount) if shake_amount > 0 else 0
    if shake_amount > 0:
        shake_amount -= 1

    # --- Rasm chizish (Canvas) ---
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_COLOR)

    # 1. Cyberpunk Fon Panjarasi (Cyber Grid)
    grid_offset = (grid_offset + 2) % 40
    for y in range(0, PLAY_HEIGHT, 40):
        pygame.draw.line(canvas, (20, 20, 55), (0, y + grid_offset), (WIDTH, y + grid_offset), 1)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(canvas, (20, 20, 55), (x, 0), (x, PLAY_HEIGHT), 1)

    # 2. Fon yulduzlari
    for star in stars:
        star[1] += star[2] * 0.4
        if star[1] > PLAY_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(canvas, (80, 80, 150), (int(star[0]), int(star[1])), int(star[2]))

    # 3. Portlash to'lqinlari (Shockwaves)
    for sw in shockwaves[:]:
        sw['radius'] += 4
        sw['alpha'] -= 12
        if sw['alpha'] <= 0 or sw['radius'] >= sw['max_radius']:
            shockwaves.remove(sw)
        else:
            surf = pygame.Surface((sw['radius']*2, sw['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*sw['color'], max(0, sw['alpha'])), (sw['radius'], sw['radius']), sw['radius'], 3)
            canvas.blit(surf, (sw['x'] - sw['radius'], sw['y'] - sw['radius']))

    # 4. To'p izi (Trail)
    for i, pos in enumerate(ball_trail):
        alpha = int(255 * (i / len(ball_trail)))
        radius = int((BALL_SIZE // 2) * (i / len(ball_trail)))
        if radius > 0:
            trail_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 0, 128, alpha // 2), (radius, radius), radius)
            canvas.blit(trail_surface, (pos[0] - radius, pos[1] - radius))

    # 5. Zarrachalar (Particles)
    for p in particles[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 1
        if p['life'] <= 0:
            particles.remove(p)
        else:
            size = int((p['life'] / p['max_life']) * 6)
            pygame.draw.circle(canvas, p['color'], (int(p['x']), int(p['y'])), max(1, size))

    # 6. Raketka va To'p
    pygame.draw.rect(canvas, CYAN, (player_x, player_y, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=10)
    pygame.draw.ellipse(canvas, MAGENTA, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # 7. Maydon ajratuvchi chiziq
    pygame.draw.line(canvas, MAGENTA, (0, PLAY_HEIGHT), (WIDTH, PLAY_HEIGHT), 4)

    # 8. Boshqaruv tugmalari paneli
    pygame.draw.rect(canvas, DARK_PANEL, (0, PLAY_HEIGHT, WIDTH, HEIGHT - PLAY_HEIGHT))
    pygame.draw.rect(canvas, CYAN, btn_up, border_radius=22)
    pygame.draw.rect(canvas, CYAN, btn_down, border_radius=22)

    # Yuqoriga va pastga ko'rsatuvchi strelkalar
    pygame.draw.polygon(canvas, BG_COLOR, [
        (btn_up.centerx, btn_up.top + 22),
        (btn_up.left + 22, btn_up.bottom - 22),
        (btn_up.right - 22, btn_up.bottom - 22)
    ])
    pygame.draw.polygon(canvas, BG_COLOR, [
        (btn_down.left + 22, btn_down.top + 22),
        (btn_down.right - 22, btn_down.top + 22),
        (btn_down.centerx, btn_down.bottom - 22)
    ])

    # 9. Hisob va Combo ko'rsatkichi
    score_txt = font_score.render(f"{score}", True, WHITE)
    combo_txt = font_combo.render(f"COMBO x{combo}", True, YELLOW)
    canvas.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 20))
    canvas.blit(combo_txt, (WIDTH // 2 - combo_txt.get_width() // 2, 20 + score_txt.get_height()))

    # Ekranga chiqarish va titrash effekti
    screen.fill(BG_COLOR)
    screen.blit(canvas, (render_offset_x, render_offset_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

