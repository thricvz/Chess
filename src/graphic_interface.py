import pygame


class Piece_sprite(pygame.sprite.Sprite):
    def __init__(self,type,color,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f"Assets\\{color[0]}_{type}_png_128px.png"), (64, 64))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        
class Dot(pygame.sprite.Sprite):
    def __init__(self,specified_x,specified_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Assets\\dot.png"), (64,64))
        self.DOT_SIZE = self.image.get_width()
        self.adjustement = (64 - self.DOT_SIZE) // 2
        self.rect = (specified_x + self.adjustement,specified_y + self.adjustement,self.DOT_SIZE,self.DOT_SIZE)

class GUI(Piece_sprite,Dot):
    
    def __init__(self,dimensions):
        self.PIECES_SPRITES = pygame.sprite.Group()
        self.DOTS = pygame.sprite.Group()
        self.screen_dimensions = dimensions
        self.SCREEN = pygame.display.set_mode(self.screen_dimensions)
        self.FONT = pygame.font.SysFont('dejavusansmono',40)
        self.screen_height,self.screen_width = self.screen_dimensions
        self.previous_player = None


    def _get_square(self,x,y):
        return f"{chr(97+x)}{abs(y-8)}"
    
    def _get_coordinates(self,square):
        square_x = int(ord(square[0])-97)
        square_y = abs(int(square[1]) - 8)
        return square_x,square_y

    def create_screen(self):
        pygame.display.set_caption("Chess Game")
        background = pygame.transform.scale(pygame.image.load("Assets\\Chess_Board.png"),(self.screen_dimensions))
        self.SCREEN.blit(background,(0,0))

    def display_menu(self):
        self.SCREEN.fill("white")
        
    def update_pieces(self,pieces_in_play):
        for piece in pieces_in_play:
            piece_x,piece_y = self._get_coordinates(piece.position)
            self.PIECES_SPRITES.add(Piece_sprite(piece.type,piece.color,piece_x*64,piece_y*64))

    def reset_predicted_squares(self):
        self.DOTS.empty()
    
    def reset_pieces(self):
        self.PIECES_SPRITES.empty()
    
    def update_predicted_squares(self,predicted_squares):
        for square in predicted_squares:
            square_x,square_y = self._get_coordinates(square)
            self.DOTS.add(Dot(square_x*64,square_y*64))

    def display_pieces(self):
        self.create_screen()
        self.DOTS.update()
        self.DOTS.draw(self.SCREEN)
        self.PIECES_SPRITES.update()
        self.PIECES_SPRITES.draw(self.SCREEN)
        
    def get_clicked_square(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            return self._get_square((mouse_x // 64 ),(mouse_y // 64))
        return "undefined"
        
    def display_message(self,message,current_player,ignore=False):
        message_already_shown = current_player == self.previous_player

        if not message_already_shown or ignore:
            message_box = self.FONT.render(message,False,'white','black')
            message_box_width,message_box_height = message_box.get_size()
            center_screen = ((self.screen_width-message_box_width)*0.5,((self.screen_height-message_box_height*0.5)*0.5))
            self.SCREEN.blit(message_box,center_screen)
            pygame.display.update()
            pygame.time.delay(750)
            self.previous_player = current_player
