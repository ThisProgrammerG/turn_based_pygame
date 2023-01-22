import pygame


SIZE = WIDTH, HEIGHT = 900, 500
ROUND_OVER = pygame.event.custom_type()

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

class Actor:
    def __init__(self, name, observer):
        self.name = name
        self.turn_over = True
        self.observer = observer

    def turn_started(self):
        self.turn_over = False

    def turn_ended(self):
        self.turn_over = True
        self.observer.turn_ended()

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

    def turn_ended(self):
        self._next_player()

def get_center(rect):
    x = WIDTH // 2 - rect.width // 2
    y = HEIGHT // 2 - rect.height // 2

    return x, y

def main():
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True

    turn_handler = TurnHandler()
    players = [Actor('Player1', turn_handler), Actor('Bot', turn_handler), Actor('Dealer', turn_handler)]
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
                if next_player_button.clicked(event):
                    turn_handler.current_player.turn_ended()
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
