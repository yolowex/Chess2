import pygame as pg
from pygame.locals import *
import chess
from pygame.rect import FRect
from pygame import Surface

from common_resources import *

class Game:

    def __init__(self):
        self.board = chess.Board()
        self.board_map = {}
        self.pieces_map = {}
        self.board_rect = FRect(screen.get_rect())

        self.board_surface:Surface
        self.pieces_surface:Surface

    def check_events( self ):
        ...

    def render( self ):
        ...