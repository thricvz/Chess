import pygame as pg

#Board Class
class Board():
    
    def __init__(self,dimensions = (512,512)):
        self.SCREEN = pg.display.set_mode(dimensions)
        self.FRONT_LAYER = list()
        self.BACK_LAYER = list()
        self.SCREEN_HEIGHT = self.SCREEN.get_height()
        self.SCREEN_WIDTH = self.SCREEN.get_width()
        self.TILE_SIZE = dimensions[0] // 8
        self.BOARD_IMAGE = pg.transform.scale(pg.image.load("Assets\\Chess_Board.png"), dimensions)
        self.PRIMARY_FONT = pg.font.Font(None,40)
        self.SECONDARY_FONT = pg.font.Font(None,12)


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

        self.turn = "white"

    def get_coordinates(self,case):
        case_x = int(ord(case[0])-97)
        case_y = abs(int(case[1]) - 8)
        return case_x,case_y
    def display_layer(self,layer):
        for sprite_group in layer:
            sprite_group.draw(self.SCREEN)

    def clear_layer(self,layer):
        for sprite_group in layer:
            sprite_group.empty()
        layer.clear()
        return

    def generate_initial_position(self):
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

    def generate_elements_to_display(self):
        dots_group = pieces_group = text_group = pg.sprite.Group()

        border_adjustement = 0
        self.SCREEN.blit(self.BOARD_IMAGE, (0, 0))

        for case_y,row in enumerate(self.board_positions):
            for case_x,case in enumerate(row):
                    case_content = self.board_state[case]  # gets what is in the case

                    text_instance = Text(case, 10, "red", case_x * self.TILE_SIZE, case_y * self.TILE_SIZE, 30, 20)
                    text_group.add(text_instance)

                    if case_content is not None:
                        case_content.rect = (case_x * self.TILE_SIZE, case_y * self.TILE_SIZE)
                        pieces_group.add(case_content)

                    if case in self.predicted_cases:
                        dot_sprite_instance = Dot(case_x * self.TILE_SIZE + border_adjustement, case_y * self.TILE_SIZE)
                        dots_group.add(dot_sprite_instance)

        self.BACK_LAYER.append(dots_group)
        self.BACK_LAYER.append(pieces_group)
        self.FRONT_LAYER.append(text_group)

        return self

    def generate_turn_message(self):
        message_content = f"{self.turn}'s turn"

    def build(self):
        self.generate_elements_to_display()
        #self.display_layer(self.BACK_LAYER)
        self.display_layer(self.FRONT_LAYER)
        self.clear_layer(self.BACK_LAYER)
        self.clear_layer(self.FRONT_LAYER)


    def manage_click(self):
        if pg.mouse.get_pressed()[0]:   #if mouse is pressed then:
                mouse_x,mouse_y = pg.mouse.get_pos()    #gets the mouse get_coordinates
                case_column = (mouse_x // self.TILE_SIZE)   #transforms it into the corresponding row and column (count starts at 1)
                case_row = (mouse_y // self.TILE_SIZE)

                pg.time.delay(200) #delay that prevents the dot from blinking fast

                current_clicked_case = self.board_positions[case_row][case_column]

                if not self.piece_selected:
                    if self.board_state[current_clicked_case] is not None:
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
        self.board_state[self.selected_board_case].times_moved += 1
        self.board_state[new_case] = None
        self.board_state[new_case] = self.board_state[self.selected_board_case]
        self.board_state[self.selected_board_case] = None


    def predict(self,piece_case):  #too much if else statements need to find a more algoritmic way to solve this problem
        predicted_positions = list()
        piece = self.board_state[piece_case]
        piece_position = self.get_coordinates(piece_case)

        if piece.mouvement_type == "continous":
            action_range = [n for n in range(1,8)]
        elif piece.type == "pawn" and piece.times_moved == 0:           #two steps rule at beginning of the game
            action_range = [n for n in range(1,3)]
        else :
            action_range = [1]

        for step in piece.mouvement_axis:
            if piece.type == "pawn" and piece.color == "black" : step = [axis * -1 for axis in step]

            for n in action_range:

                if piece_position[0] + n * step[0] in range(8) and piece_position[1] + n * step[1] in range(8):
                    gen_x = piece_position[0] + n * step[0]
                    gen_y = piece_position[1] + n * step[1]

                    generated_position = self.board_positions[gen_y][gen_x]

                    if self.board_state[generated_position] is None:
                        predicted_positions.append(generated_position)

                    elif self.board_state[generated_position].color != piece.color and piece.type != "pawn":
                        predicted_positions.append(generated_position)
                        break

                    elif self.board_state[generated_position].color == piece.color:
                        break
                else:
                    break

        ###just a test
        if piece.type == "pawn":
                capture_steps = [[-1, 1], [1, 1]]

                for cap_step in capture_steps:
                    if piece.color == "black": cap_step = [axis * -1 for axis in cap_step]
                    if piece_position[0] + cap_step[0] in range(8) and piece_position[1] + cap_step[1] in range(8):
                        new_capt_x = piece_position[0] + cap_step[0]
                        new_capt_y = piece_position[1] + cap_step[1]
                        generated_position = self.board_positions[new_capt_y][new_capt_y]

                        if self.board_state[generated_position] is not None and self.board_state[generated_position].color != piece.color:
                            predicted_positions.append(generated_position)

        return predicted_positions

class Piece(pg.sprite.Sprite):
    mouvement_axis_map = {
                    "pawn": [[0,-1]],
                    "rook" : [[1,0],[0,-1],[-1,0],[0,1]],
                    "knight" : [[-2,1],[-1,2],[-2,-1],[-1,-2],[2,1],[1,2],[2,-1],[1,-2]],
                    "bishop" : [[-1,1],[-1,-1],[1,1],[1,-1]] ,
                    "queen" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]],
                    "king" : [[1,0],[0,-1],[-1,0],[0,1],[-1,1],[-1,-1],[1,1],[1,-1]]
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
        self.image = pg.transform.scale(pg.image.load("Assets\\dot.png"), (64,64))
        self.DOT_SIZE = self.image.get_width()
        self.adjustement = (64 - self.DOT_SIZE) // 2
        self.rect = (specified_x + self.adjustement,specified_y + self.adjustement,self.DOT_SIZE,self.DOT_SIZE)


class Text(pg.sprite.Sprite):
    def __init__(self, text, size,color,specified_x,specified_y,width, height):
        pg.sprite.Sprite.__init__(self)

        self.font = pg.font.SysFont("Arial", size)
        self.textSurface = self.font.render(text,True,color)
        self.image = pg.Surface((width, height))

        self.rect = (specified_x,specified_y,width,height)
        W = self.textSurface.get_width()
        H = self.textSurface.get_height()

        ###need to turn text into a image
