import pygame as pg
from pygame.locals import *
import chess
from pygame.rect import FRect
from pygame import Surface

import core.common_resources as cr

class Game:

    def __init__(self):
        self.board = chess.Board()
        self.board_map = {} # A map that contains every coord and their co-responding rectangle
        self.pieces_map = {}

        self.board_surface:Surface
        self.pieces_surface:Surface

        self.board_rect = FRect(cr.boards_json_dict['classic_board']['board_rect'])
        self.board_sprite = cr.boards_sprite_dict['classic_board']
        self.resize_board()
        self.create_board_tiles()

    def resize_board( self ):
        self.board_sprite.transform(cr.screen.get_width(), cr.screen.get_height())

        m = self.board_sprite.get_diff()[0]
        self.board_rect.x *= m
        self.board_rect.y *= m
        self.board_rect.w *= m
        self.board_rect.h *= m
        self.board_rect.w += 1
        self.board_rect.h += 1

    def create_board_tiles( self ):
        w = self.board_rect.w / 8
        h = self.board_rect.h / 8

        letters = 'abcdefgh'
        digits = '12345678'

        for x,letter in zip(range(8),letters):
            for y,digit in zip(range(8),digits[::-1]):
                rect = FRect(x*w,y*h,w,h)
                rect.x += self.board_rect.x
                rect.y += self.board_rect.y
                uci = letter+digit
                self.board_map[uci] = rect





    def check_events( self ):
        if cr.event_holder.mouse_pressed_keys[0]:
            for uci in self.board_map:
                rect = self.board_map[uci]
                if cr.event_holder.mouse_rect.colliderect(rect):
                    print(uci)


    def render( self ):
        cr.screen.blit(self.board_sprite.transformed_surface,[0,0])
        # pg.draw.rect(cr.screen,[0,0,0],self.board_rect,width=20)