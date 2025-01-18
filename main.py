import pygame
import time
import random
import json
pygame.font.init()



#makes window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")


#BG
BG = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\bg.png"), (WIDTH, HEIGHT))
BG_LVL2 = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\\space.jpg"), (WIDTH, HEIGHT))

#PLAYER
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\bird1.png"), (50, 50))
PLAYER_IMAGE_FLIPPED = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\bird2.png"), (50, 50))
PLAYER_IMAGE2 = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\player2.gif"), (90, 90))
PLAYER_VEL = 5

#FONT
FONT = pygame.font.SysFont("Time New Roman", 40)
LARGE_FONT = pygame.font.SysFont("Times New Roman", 60)

#STAR
STAR_IMAGE = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\sky.gif"), (70, 70))
STAR_IMAGE2 = pygame.transform.scale(pygame.image.load(r"C:\Users\ldaco\Desktop\coding\dodger\images\fire.gif"), (80, 80))
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

player_wins = {}

SCORE_FILE = "score.txt"

def load_scores():
    try:
        with open(SCORE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return{}
    except json.JSONDecodeError:
        return{}

def save_score(scores):
    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file)

def ask_username():
    username = ""
    while True:
        WIN.blit(BG, (0,0))
        prompt_text = FONT.render("Enter your Username: " + username, 1, "white")
        WIN.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE and username:
                    username = username[:-1]
                elif event.unicode.isalnum():
                    username += event.unicode


def draw(player, elapsed_time, stars, bg_image, star_image, player_image):
    #drawing the BG and putting it on the entire screen (0,0)
    WIN.blit(bg_image, (0,0))

    time_text = FONT.render(f"Time:  {round(elapsed_time)}s,", 1, "white")
    WIN.blit(time_text, (10,10))

    WIN.blit(player_image, (player.x, player.y))

    for star in stars:
        WIN.blit(star_image, (star.x, star.y))

    #applies the updates
    pygame.display.update()

def level_switch(level_text, bg_image):
    WIN.blit(bg_image, (0,0))
    text = LARGE_FONT.render(level_text, 1, "white")
    WIN.blit(text, (WIDTH//2 - text.get_width()// 2, HEIGHT //2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)

def start_screen(username):
    WIN.blit(BG, (0,0))
    title_text = LARGE_FONT.render(f"Welcome to Dodger, {username}!", 1, "white")
    wins_text = LARGE_FONT.render(f"Games Won: {player_wins.get(username, 0)}",1, "yellow")
    start_text = LARGE_FONT.render("Press Space to Start", 1, "white")
    WIN.blit(wins_text, (WIDTH // 2 - wins_text.get_width() // 2, HEIGHT // 1.5))
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 50))
    WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main():
    global player_wins
    player_wins = load_scores()


    username = ask_username()
    if username not in player_wins:
        player_wins[username] = 0
    
    start_screen(username)
    level_switch("Level 1", BG)

    run = True
    level = 1
    player  = pygame.Rect(200, (HEIGHT - PLAYER_HEIGHT) - 145, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    game_won = False

    current_player = PLAYER_IMAGE


#loop to keep window open

    while run:
        star_count += clock.tick(60)#returns number of ms since last tick
        elapsed_time = time.time() - start_time

        if elapsed_time >= 10 and not game_won:
            game_won = True
            stars.clear()

            player_wins[username] += 1
            save_score(player_wins)
            
            win_text = LARGE_FONT.render(f"CONGRATS " + username + " YOU WIN!", 1, "white")
            WIN.blit(win_text,(WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3 + 50))
            restart_text = FONT.render("Press SPACE to Restart or Esc to Quit", 1, "white")
            WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            pygame.display.update()

        if level == 1 and elapsed_time > 5:
            level = 2
            level_switch("Level 2", BG_LVL2)
            star_add_increment = 1500
            stars.clear()
            elapsed_time = 0

        bg_image = BG if level == 1 else BG_LVL2
        star_image = STAR_IMAGE if level == 1 else STAR_IMAGE2
        player_image = current_player if level == 1 else PLAYER_IMAGE2

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)#slowly enter by using - height
                stars.append(star)

            star_add_increment = max(300, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if game_won:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
                        return
                    elif event.type == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        if game_won:
            continue
            

        
        #buttons pressed to move left or right
        keys = pygame.key.get_pressed()

        if level == 1:
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
                current_player = PLAYER_IMAGE_FLIPPED
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
                current_player = PLAYER_IMAGE
            if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
                current_player = PLAYER_IMAGE_FLIPPED
            if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
                current_player = PLAYER_IMAGE

        else:
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
            if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL


        #for stars
        for star in stars[:]:#loop thru copy
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lose_text = LARGE_FONT.render("YOU LOST!", 1, "white")
            WIN.blit(lose_text, (WIDTH/2 - lose_text.get_width()/ 2, HEIGHT/2.3 - lose_text.get_height()/2))
            restart_text = FONT.render("Press SPACE to Restart or ESC to Exit",1,"white" )
            WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 - restart_text.get_height()/2))
            pygame.display.update()
            

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main()
                            return
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
        
        draw(player, elapsed_time, stars, bg_image, star_image, player_image)

    pygame.quit()

if __name__ == "__main__":
    main()