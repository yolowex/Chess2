import pygame as pg
from pygame.locals import *
import chess
from pygame.rect import FRect
from pygame import Surface

import core.common_resources as cr

class Game:

    def __init__(self):
        self.board = chess.Board()
        self.board_map = {}
        self.pieces_map = {}
        self.board_rect = FRect(cr.screen.get_rect())

        self.board_surface:Surface
        self.pieces_surface:Surface

        self.board_rect = FRect(cr.boards_json_dict['classic_board']['board_rect'])
        self.board_sprite = cr.boards_sprite_dict['classic_board']
        self.resize_board()


    def resize_board( self ):
        self.board_sprite.transform(cr.screen.get_width(), cr.screen.get_height())

        m = self.board_sprite.get_diff()[0]
        self.board_rect.x *= m
        self.board_rect.y *= m
        self.board_rect.w *= m
        self.board_rect.h *= m
        self.board_rect.w += 1
        self.board_rect.h += 1

    def check_events( self ):
        ...

    def render( self ):
        cr.screen.blit(self.board_sprite.transformed_surface,[0,0])
        pg.draw.rect(cr.screen,[0,0,0],self.board_rect,width=20)