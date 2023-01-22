import pygame


pygame.init()

SIZE = pygame.Rect((0, 0), (900, 500))
ROUND_OVER = pygame.event.custom_type()
FONT = pygame.font.SysFont('Consolas', 24, bold=True)

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

class Actor:
    def __init__(self, name):
        self.name = name
        self.turn_over = True

    def turn_started(self):
        self.turn_over = False

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

    def end_player_turn(self):
        self.current_player.turn_ended()
        self._next_player()

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

    next_player_button = Button((200, 100), (SIZE.width // 2, 400), 'Next Player', 'purple')
    new_round_button = Button((200, 100), (SIZE.width - 200, 400), 'New Round', 'darkgreen')

    while running:
        clock.tick(60)
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_player_button.clicked(event):
                    turn_handler.end_player_turn()
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

        new_round_button.render(screen)
        next_player_button.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
