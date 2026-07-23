import asyncio
import pygame
import random

# Pygame ကို စတင်ခြင်း
pygame.init()

# Screen အကျယ်/အမြင့် သတ်မှတ်ခြင်း (Mobile Dynamic Friendly)
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Catcher Game")

# အရောင်များ
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GOLD = (255, 215, 0)
DARK = (30, 30, 30)

# ကစားသမား (Basket) သတ်မှတ်ချက်များ
player_width, player_height = 80, 20
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - 50
player_speed = 7

# ဒင်္ဂါး (Coin) သတ်မှတ်ချက်များ
coin_radius = 15
coin_x = random.randint(coin_radius, WIDTH - coin_radius)
coin_y = 0
coin_speed = 5

# အမှတ် (Score)
score = 0
font = pygame.font.SysFont(None, 36)

# Main Game Loop (Web ပေါ်မှာ အလုပ်လုပ်ဖို့ asyncio သုံးရပါတယ်)
async def main():
    global player_x, coin_x, coin_y, coin_speed, score

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(DARK)

        # Event များကို စစ်ဆေးခြင်း
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ထိန်းချုပ်မှုများ (ကီးဘုတ် / Touch ခလုတ်များ)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Touch screen အတွက် (ဖုန်းမှာ မျက်နှာပြင် လက်ဝဲ/လက်ယာ နှိပ်ရင် ရွှေ့ရန်)
        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            if mouse_x < WIDTH // 2 and player_x > 0:
                player_x -= player_speed
            elif mouse_x >= WIDTH // 2 and player_x < WIDTH - player_width:
                player_x += player_speed

        # Coin အောက်ကို ပြုတ်ကျခြင်း
        coin_y += coin_speed

        # Coin နဲ့ Basket ထိမထိ (Collision Check)
        if player_y < coin_y + coin_radius < player_y + player_height:
            if player_x < coin_x < player_x + player_width:
                score += 1
                coin_y = 0
                coin_x = random.randint(coin_radius, WIDTH - coin_radius)
                coin_speed += 0.2 # အမှတ်ရလေ ပိုမြန်လာလေ

        # အောက်ခြေ ရောက်သွားရင် ပြန်စမည်
        if coin_y > HEIGHT:
            coin_y = 0
            coin_x = random.randint(coin_radius, WIDTH - coin_radius)
            score = 0 # အမှတ် ပြန်စမည်
            coin_speed = 5

        # ပစ္စည်းများကို မျက်နှာပြင်ပေါ် ဆွဲခြင်း
        # Player (Basket)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height), border_radius=5)
        # Coin
        pygame.draw.circle(screen, GOLD, (coin_x, coin_y), coin_radius)

        # Score ပြသခြင်း
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0) # Web browser အတွက် လိုအပ်သည်

    pygame.quit()

# Run the game
asyncio.run(main())

