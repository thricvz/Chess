import pygame as pg
import string

#Board Class
class Board():
    
    def __init__(self,dimensions = (512,512)):
        self.SCREEN = pg.display.set_mode(dimensions)   #creates a 400 by 400 window
        self.TILE_SIZE = dimensions[0] // 8
        self.BOARD_IMAGE = pg.transform.scale(pg.image.load("Assets\\Chess_Board.png"), dimensions)
        self.FONT = pg.font.SysFont(None,20)

        self.dots_group = pg.sprite.Group()
        self.pieces_group = pg.sprite.Group()

        self.board_state = {'a8': None, 'b8': None, 'c8': None, 'd8': None, 'e8': None, 'f8': None, 'g8': None, 'h8': None,
                            'a7': None, 'b7': None, 'c7': None, 'd7': None, 'e7': None, 'f7': None, 'g7': None, 'h7': None,
                            'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
                            'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
                            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
                            'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
                            'a2': None, 'b2': None, 'c2': None, 'd2': None, 'e2': None, 'f2': None, 'g2': None, 'h2': None,
                            'a1': None, 'b1': None, 'c1': None, 'd1': None, 'e1': None, 'f1': None, 'g1': None, 'h1': None}
        
        self.board_positions = list(self.board_state)     #list containing every position available in the board
        self.board_positions = [self.board_positions[x:x+8] for x in range(0, len(self.board_positions), 8)]

        self.piece_selected = False               
        self.predicted_cases = list()

    def coordinates(self,case):
        case_x = int(ord(case[0])-97)
        case_y = abs(int(case[1]) - 8)
        return case_x,case_y

    def generate_pieces(self):
        board_starting_positions = {
            "pawn" : ["a7","b7","c7","d7","e7","f7","g7","h7","a2","b2","c2","d2","e2","f2","g2","h2",] ,
            "rook" : ["a8","h8","a1","h1"],
            "knight"  : ["b8","g8","b1","g1"],
            "bishop" : ["c8","f8","c1","f1"],
            "queen" : ["d8","d1"],
            "king"  : ["e8","e1"],
        }

        for piece in board_starting_positions.items():
            piece_color = "black"
            for case in piece[1]:
                if piece[1].index(case) == len(piece[1]) / 2 : piece_color = "white"

                self.board_state[case] = Piece(piece[0],piece_color)
     

    def build(self):

        self.SCREEN.blit(self.BOARD_IMAGE, (0, 0))

        for case_y,row in enumerate(self.board_positions):
            for case_x,case in enumerate(row):
                    case_content = self.board_state[case]  # gets what is in the case


                    text = self.FONT.render(case, True, (0, 0, 255))  # case text
                    self.SCREEN.blit(text, (case_x * self.TILE_SIZE + 3, case_y * self.TILE_SIZE + 3))

                    if case_content != None:
                        case_content.rect = (case_x * self.TILE_SIZE,case_y * self.TILE_SIZE)
                        self.pieces_group.add(case_content)

                    if case in self.predicted_cases:
                        dot_sprite_instance = Dot(case_x * self.TILE_SIZE,case_y * self.TILE_SIZE)
                        self.dots_group.add(dot_sprite_instance)

        self.dots_group.draw(self.SCREEN)
        self.pieces_group.draw(self.SCREEN)

        self.dots_group.empty()
        self.pieces_group.empty()
    def manage_click(self):
        if pg.mouse.get_pressed()[0]:   #if mouse is pressed then:
                mouse_x,mouse_y = pg.mouse.get_pos()    #gets the mouse coordinates
                case_column = (mouse_x // self.TILE_SIZE)   #transforms it into the corresponding row and column (count starts at 1)
                case_row = (mouse_y // self.TILE_SIZE)

                pg.time.delay(200) #delay that prevents the dot from blinking fast

                current_clicked_case = self.board_positions[case_row][case_column]

                if not self.piece_selected:
                    if self.board_state[current_clicked_case] != None:
                        self.selected_board_case  = current_clicked_case
                        self.piece_selected = True
                        self.predicted_cases = self.predict(self.selected_board_case)


                else:
                    if current_clicked_case in self.predicted_cases:
                        self.move(current_clicked_case)

                    self.piece_selected = False
                    self.predicted_cases = []

        return self
    def move(self,new_case):
        self.board_state[new_case] = None
        self.board_state[new_case] = self.board_state[self.selected_board_case]
        self.board_state[self.selected_board_case] = None


    def predict(self,piece_case):  #too much if else statements need to find a more algoritmic way to solve this problem
        predicted_positions = list()
        piece = self.board_state[piece_case]
        piece_position = self.coordinates(piece_case)

        #piece.mouvement_axis[0] = (0,1) if piece.type == "bishop" and piece.color == "black" else (0,-1)
        for step in piece.mouvement_axis:
            for n in range(1, 8): #since the maximum of cases in any direction is 8

                if piece.mouvement_type == "discontinous": n = 1

                if piece_position[0] + n * step[0] in range(8) and piece_position[1] + n * step[1] in range(8):             #checks if the future position  is on the board
                    gen_x = piece_position[0] + n * step[0]
                    gen_y = piece_position[1] + n * step[1]

                    generated_position = self.board_positions[gen_y][gen_x]

                    if self.board_state[generated_position] == None:
                        predicted_positions.append(generated_position)

                    elif self.board_state[generated_position].color != piece.color:
                        predicted_positions.append(generated_position)
                        break

                    elif self.board_state[generated_position].color == piece.color:
                        break
                else:
                    break

        return predicted_positions


class Piece(pg.sprite.Sprite):
    mouvement_axis_map = {
                    "pawn": [(0,-1)] ,
                    "rook" : [(1,0),(0,-1),(-1,0),(0,1)],
                    "knight" : [(-2,1),(-1,2),(-2,-1),(-1,-2),(2,1),(1,2),(2,-1),(1,-2)],
                    "bishop" : [(-1,1),(-1,-1),(1,1),(1,-1)] ,
                    "queen" : [(1,0),(0,-1),(-1,0),(0,1),(-1,1),(-1,-1),(1,1),(1,-1)],
                    "king" : [(1,0),(0,-1),(-1,0),(0,1),(-1,1),(-1,-1),(1,1),(1,-1)]
                          }
    ###this format consists of the "steps" that have to be done on the board (x,y) : ex-> (-1,1) would be one "step" to the left and one "step" to the bottom
    def __init__(self,type,color):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.color = color
        self.image = pg.transform.scale(pg.image.load(f"Assets\\{self.color[0]}_{self.type}_png_128px.png"), (64, 64))
        self.rect = self.image.get_rect()
        self.mouvement_axis = Piece.mouvement_axis_map[self.type]
        self.mouvement_type = "discontinous" if self.type  in ["king","knight","pawn"] else "continous"
        self.times_moved = 0
        self.clicked = False

class Dot(pg.sprite.Sprite):
    def __init__(self,specified_x,specified_y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load("Assets\\dot.png"), (45, 45))
        self.DOT_SIZE = self.image.get_width()
        self.rect = (specified_x+10.5,specified_y+10.5,self.DOT_SIZE,self.DOT_SIZE)
