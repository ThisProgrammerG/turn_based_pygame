import itertools
import random
import threading
import time

import pygame


pygame.init()

SIZE = pygame.Rect((0, 0), (900, 500))
ROUND_OVER = pygame.event.custom_type()
TURN_ENDED = pygame.event.custom_type()
FONT = pygame.font.SysFont('Consolas', 24, bold=True)
THINKING = itertools.cycle([FONT.render(f'{"." * i}', True, 'pink') for i in range(1, 6)])

class Button:
    def __init__(self, size, position, text, color):
        self.position = position
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(**{'center': position})
        self.text = FONT.render(text, True, 'white')
        self.image.blit(self.text, get_center(self.rect, self.text.get_rect()))

    def clicked(self, event):
        return self.rect.collidepoint(event.pos)

    def render(self, surface):
        surface.blit(self.image, self.rect)

def thinking():
    seconds = random.randint(3, 6)
    print(f'Thinking for: {seconds} seconds.')
    while True:
        time.sleep(seconds)
        break

class Actor:
    def __init__(self, name):
        self.name = name
        self.turn_over = True
        self.thinking_thread = threading.Thread(target=thinking, daemon=True)
        self.ran_thread = False  # Can only run threads once

    def turn_started(self):
        self.turn_over = False
        if not self.name.lower().find('player') > -1:
            if not self.ran_thread:
                self.thinking_thread.start()
                self.ran_thread = True
            else:
                self.thinking_thread = threading.Thread(target=thinking, daemon=True)
                self.thinking_thread.start()

    def turn_ended(self):
        self.turn_over = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Player: {self.name}'

class TurnHandler:
    def __init__(self):
        self.players = None
        self.current_player = None
        self.round_over = False
        self.player_index = 0

    def reset(self):
        self.round_over = False
        self.player_index = 0
        self._next_player()

    def _next_player(self):
        """ Try to get the next player if there are any. Otherwise, round is over. """
        try:
            self.current_player = self.players[self.player_index]
            self.current_player.turn_started()
            self.player_index += 1
        except IndexError:
            pygame.event.post(pygame.event.Event(ROUND_OVER))

    def set_players(self, players):
        self.players = players.copy()
        self._next_player()

    def end_player_turn(self):
        self.current_player.turn_ended()
        self._next_player()

    def player_thinking(self):
        return self.current_player.thinking_thread.is_alive()

def get_center(rect, other_rect):
    x = rect.width // 2 - other_rect.width // 2
    y = rect.height // 2 - other_rect.height // 2

    return x, y

def main():
    screen = pygame.display.set_mode(SIZE.size)
    clock = pygame.time.Clock()
    running = True

    turn_handler = TurnHandler()
    players = [Actor('Player1'), Actor('Bot'), Actor('Dealer')]
    turn_handler.set_players(players)
    thinking_dots = next(THINKING)
    thinking_index = 0

    next_player_button = Button((200, 100), (SIZE.width // 2, 400), 'Next Player', 'purple')
    new_round_button = Button((200, 100), (SIZE.width - 200, 400), 'New Round', 'darkgreen')

    while running:
        clock.tick(60)
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not turn_handler.player_thinking():  # Block click events until the other player is done thinking
                    if next_player_button.clicked(event):
                        turn_handler.end_player_turn()
                        thinking_index = 0
                    elif new_round_button.clicked(event):
                        turn_handler.reset()
            elif event.type == ROUND_OVER:
                turn_handler.round_over = True

        if turn_handler.round_over:
            text = FONT.render(f'Round Over.', True, 'red')
            screen.blit(text, get_center(SIZE, text.get_rect()))
        else:
            text = FONT.render(f'In play: {turn_handler.current_player.name}', True, 'purple')
            screen.blit(text, get_center(SIZE, text.get_rect()))

        if turn_handler.player_thinking():
            if thinking_index % 10 == 0:
                thinking_dots = next(THINKING)
            thinking_index += 1
            screen.blit(thinking_dots, (0, 0))

        new_round_button.render(screen)
        next_player_button.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
