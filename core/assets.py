import this
import json
from core.sprite import Sprite


def contains_text(src:str,text:str):
    return src.find(text) != -1

root = "./assets"
pieces_root = root+"/chess_pieces/"
boards_root = root+"/chess_boards/"
ui_root = root+"/ui/"

pieces_sprite_dict = {
    'K':Sprite(pieces_root+"white_king.png"),
    'Q':Sprite(pieces_root+"white_queen.png"),
    'R':Sprite(pieces_root+"white_rook.png"),
    'B':Sprite(pieces_root+"white_bishop.png"),
    'N':Sprite(pieces_root+"white_knight.png"),
    'P':Sprite(pieces_root+"white_pawn.png"),

    'k':Sprite(pieces_root+"black_king.png"),
    'q':Sprite(pieces_root+"black_queen.png"),
    'r':Sprite(pieces_root+"black_rook.png"),
    'b':Sprite(pieces_root+"black_bishop.png"),
    'n':Sprite(pieces_root+"black_knight.png"),
    'p':Sprite(pieces_root+"black_pawn.png"),
}

boards_sprite_dict = {
    'classic_board':Sprite(boards_root+"board_empty.png")
}

boards_json_dict = {
    'classic_board':json.loads(open(boards_root+"board_empty.json").read())
}

ui_dict = {
    'ai':Sprite(ui_root+"ai.png"),
    'exit':Sprite(ui_root+"exit.png"),
    'reset':Sprite(ui_root+"reset.png"),
    'undo':Sprite(ui_root+"undo.png"),
}

StockfishPath = '/home/yolo/stockfish/stockfish_15.1_linux_x64_avx2/' \
                        'stockfish-ubuntu-20.04-x86-64-avx2'



