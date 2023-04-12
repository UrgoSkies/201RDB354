import pygame
import sys
import random

pygame.init()

# ekrāna izmērs un displejs
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# krasas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)

# texta fonti
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# loga nosaukums
pygame.display.set_caption('SKAITLISKAIS LĪDZSVARS')

# sakotnejas speles mainigo vertibas
sequence = "323232322"
player_A_score = 0
player_B_score = 0
player_A_numbers = []
player_B_numbers = []
number_buttons = []
game_started = False
player_turn = random.choice(["A", "B"])

# speles restartesanas mainigie
def reset_game():
    global player_A_score, player_B_score, player_A_numbers, player_B_numbers, player_turn, sequence
    player_A_score = 0
    player_B_score = 0
    player_A_numbers = []
    player_B_numbers = []
    player_turn = random.choice(["A", "B"])
    sequence = "323222322"

reset_game()  

# Start pogas zimesanas funkcija
def draw_button(screen, text, x, y, width, height, button_color, text_color):
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)

# Minimaksa algoritms
def minimax(sequence, depth, is_maximizing):
    if depth == 0 or len(sequence) == 1:
        return int(sequence[0]) if is_maximizing else -int(sequence[0]), 0

    best_eval = -float('inf') if is_maximizing else float('inf')
    best_index = 0

    for i in (0, len(sequence) - 1):
        new_sequence = sequence[:i] + sequence[i + 1:]
        eval, _ = minimax(new_sequence, depth - 1, not is_maximizing)

        if is_maximizing and eval > best_eval:
            best_eval = eval
            best_index = i
        elif not is_maximizing and eval < best_eval:
            best_eval = eval
            best_index = i

    return best_eval, best_index

# galvenais speles cikls
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # peles klikski uz pogas Start
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            x, y = event.pos
            if start_button.collidepoint(x, y):
                game_started = True

        # peles klikski prieks speletaja B (speletajs)
        if event.type == pygame.MOUSEBUTTONDOWN and game_started and player_turn == "B":
            x, y = event.pos
            for i, button_rect in enumerate(number_buttons):
                if button_rect.collidepoint(x, y) and (i == 0 or i == len(sequence) - 1):
                    chosen_number = int(sequence[i])
                    sequence = sequence[:i] + sequence[i+1:]
                    player_B_score += chosen_number  
                    player_B_numbers.append(chosen_number)
                    player_turn = "A"

   
    screen.fill(WHITE)

    # kamer spele nesakas , zimejam start pogu
    if not game_started:
        start_button = pygame.draw.rect(screen, GREEN, (screen_width // 2 - 50, screen_height // 2 - 25, 100, 50))
        draw_button(screen, "START", screen_width // 2 - 50, screen_height // 2 - 25, 100, 50, GREEN, BLACK)

    # ja spele sacas tad zimejam speles laukumu
    else:
        # A un B speletaja konta zimesana
        score_A_text = font.render(f"AI: {player_A_score}", True, TEXT_COLOR)
        screen.blit(score_A_text, (10, 10))
        score_B_text = font.render(f"SPĒLĒTĀJS: {player_B_score}", True, TEXT_COLOR)
        screen.blit(score_B_text, (screen_width - score_B_text.get_width() - 10, 10))

        # gajena progresa imformacijas izvadisana
        turn_text = font.render(f"GĀJIENS: {'AI' if player_turn == 'A' else 'SPĒLĒTĀJS'}", True, TEXT_COLOR)
        screen.blit(turn_text, (screen_width // 2 - turn_text.get_width() // 2, 10))

        # secibas skaitlu zimesana
        number_buttons = []
        button_x = 50
        button_y = screen_height // 2
        button_width = 50
        button_height = 50

        total_width = len(sequence) * (button_width + 10) - 10
        first_button_x = (screen_width - total_width) // 2

        for i, num in enumerate(sequence):
            color = GREEN if i == 0 or i == len(sequence) - 1 else RED
            button_rect = pygame.draw.rect(screen, color, (first_button_x, button_y, button_width, button_height))
            number_buttons.append(button_rect)
            draw_button(screen, num, first_button_x, button_y, button_width, button_height, color, BLACK)
            first_button_x += button_width + 10

        # skaitlu kurus speletaji izvelejas zimesana (zem speletaja vardiem)
        numbers_y = 100
        for number in player_A_numbers:
            number_text = small_font.render(str(number), True, TEXT_COLOR)
            screen.blit(number_text, (10, numbers_y))
            numbers_y += number_text.get_height() + 10

        numbers_y = 100
        for number in player_B_numbers:
            number_text = small_font.render(str(number), True, TEXT_COLOR)
            screen.blit(number_text, (screen_width - number_text.get_width() - 10, numbers_y))
            numbers_y += number_text.get_height() + 10

        # ja seciba palika 1 skaitlis tad beidzam speli un izvelejamies uzvaretaju
        if len(sequence) == 1:
            if player_A_score > player_B_score:
                winner = "AI UZVARĒJA!"
            elif player_A_score < player_B_score:
                winner = "SPĒLĒTĀJS UZVARĒJA!"
            else:
                winner = "SPĒLĒ NEIZŠĶIRTS!"

            # rezultata zimesana uz ekrana
            result_text = font.render(winner, True, BLACK)
            text_rect = result_text.get_rect()
            text_rect.center = (screen_width // 2, screen_height // 2 - 50)
            screen.blit(result_text, text_rect)

            # pogas "velreiz" zimesana
            reset_button = pygame.draw.rect(screen, GREEN, (screen_width // 2 - 125, screen_height // 2 + 125, 150, 50))
            draw_button(screen, "VĒLREIZ", screen_width // 2 - 125, screen_height // 2 + 125, 150, 50, GREEN, BLACK)

            # pogas "iziet" zimesana
            exit_button = pygame.draw.rect(screen, RED, (screen_width // 2 + 25, screen_height // 2 + 125, 100, 50))
            draw_button(screen, "IZIET", screen_width // 2 + 25, screen_height // 2 + 125, 100, 50, RED, BLACK)

            pygame.display.flip()

            # gaidam kamer speletajs izvelas vai nu restartet vai nu iziet
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if reset_button.collidepoint(x, y):
                        reset_game()
                        break
                    if exit_button.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

        # ja spele sacas un AI veic gajenu
        if game_started and player_turn == "A":
            _, chosen_index = minimax(sequence, 15, True)
            chosen_number = int(sequence[chosen_index])
            sequence = sequence[:chosen_index] + sequence[chosen_index+1:]
            player_A_score += chosen_number  # score
            player_A_numbers.append(chosen_number)
            player_turn = "B"

    # ekrana atjauninajums
    pygame.display.flip()
    pygame.time.wait(100)
