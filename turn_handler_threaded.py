import threading
import random
import time

import pygame


SIZE = WIDTH, HEIGHT = 900, 500
ROUND_OVER = pygame.event.custom_type()
TURN_ENDED = pygame.event.custom_type()

pygame.init()

class Button:
    def __init__(self, size, position, color):
        self.position = position
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(**{'center': position})

    def clicked(self, event):
        return self.rect.collidepoint(event.pos)

    def render(self, surface):
        surface.blit(self.image, self.rect)

def thinking():
    seconds = random.randint(3, 6)
    print(f'Thinking for {seconds} seconds.')
    while True:
        time.sleep(seconds)
        break

    print(f'Done thinking.')

class Actor:
    def __init__(self, name):
        self.name = name
        self.turn_over = True
        self.thinking_thread = threading.Thread(target=thinking, daemon=True)

    def turn_started(self):
        self.turn_over = False
        if not self.name.lower().find('player') > -1:
            self.thinking_thread.start()

    def turn_ended(self):
        self.turn_over = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Player: {self.name}'

class TurnHandler:
    def __init__(self):
        self._players = None
        self.players = None
        self.current_player = None
        self.round_over = False
        self.player_index = 0

    def reset(self):
        self.round_over = False
        self.player_index = 0
        self.players = self._players.copy()
        self._next_player()

    def _next_player(self):
        try:
            self.current_player = self.players[self.player_index]
            self.current_player.turn_started()
            self.player_index += 1
        except IndexError:
            pygame.event.post(pygame.event.Event(ROUND_OVER))

    def set_players(self, players):
        self._players = players.copy()
        self.players = players.copy()
        self._next_player()

    def end_current_player(self):
        self.current_player.turn_ended()
        self._next_player()

    def player_thinking(self):
        return self.current_player.thinking_thread.is_alive()

def get_center(rect):
    x = WIDTH // 2 - rect.width // 2
    y = HEIGHT // 2 - rect.height // 2

    return x, y

def main():
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True

    turn_handler = TurnHandler()
    players = [Actor('Player1'), Actor('Bot'), Actor('Dealer')]
    turn_handler.set_players(players)

    font = pygame.font.SysFont('Consolas', 24, bold=True)
    next_player_button = Button((100, 100), (WIDTH // 2, 400), 'orange')
    new_round_button = Button((100, 100), (WIDTH - 100, 400), 'green')

    while running:
        clock.tick(60)
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f'Is player thinking: {turn_handler.player_thinking()}')
                if not turn_handler.player_thinking():
                    if next_player_button.clicked(event):
                        turn_handler.end_current_player()
                    elif new_round_button.clicked(event):
                        turn_handler.reset()
            elif event.type == ROUND_OVER:
                turn_handler.round_over = True

        if turn_handler.round_over:
            text = font.render(f'Round Over.', True, 'red')
            screen.blit(text, get_center(text.get_rect()))
        else:
            text = font.render(f'In play: {turn_handler.current_player.name}', True, 'purple')
            screen.blit(text, get_center(text.get_rect()))

        new_round_button.render(screen)
        next_player_button.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
