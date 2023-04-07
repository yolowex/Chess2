import pygame as pg
from pygame.locals import *

import chess
from typing import Optional
from pygame.rect import FRect
from pygame import Surface

from core.common_functions import *
import core.common_resources as cr


class Game :

    def __init__( self ) :
        self.board = chess.Board()
        self.board_map = {}  # A map that contains every coord and their co-responding rectangle
        self.pieces_map = {}

        self.board_rect = FRect(cr.boards_json_dict['classic_board']['board_rect'])
        self.board_sprite = cr.boards_sprite_dict['classic_board']
        self.resize_board()
        self.create_board_tiles()

        self.resize_pieces()
        self.selected_piece = None
        self.update_pieces_map()

    def update( self ):
        self.update_pieces_map()

    def resize_board( self ) :
        self.board_sprite.transform(cr.screen.get_width(), cr.screen.get_height())

        m = self.board_sprite.get_diff()[0]
        self.board_rect.x *= m
        self.board_rect.y *= m
        self.board_rect.w *= m
        self.board_rect.h *= m
        self.board_rect.w += 1
        self.board_rect.h += 1


    def create_board_tiles( self ) :
        w = self.board_rect.w / 8
        h = self.board_rect.h / 8

        letters = 'abcdefgh'
        digits = '12345678'

        for x, letter in zip(range(8), letters) :
            for y, digit in zip(range(8), digits[: :-1]) :
                rect = FRect(x * w, y * h, w, h)
                rect.x += self.board_rect.x
                rect.y += self.board_rect.y
                uci = letter + digit
                self.board_map[uci] = rect


    def update_pieces_map( self ) :
        fen = self.board.board_fen()

        new_fen = [expand_fen_row(i) for i in fen.split('/')]

        pieces = {}

        for row, digit in zip(new_fen, "87654321") :
            for column, letter in zip(row, "abcdefgh") :
                if column != '0' :
                    pieces[letter + digit] = column

        self.pieces_map = pieces


    def resize_pieces( self ) :
        tallest_piece = cr.pieces_sprite_dict["r"]

        h = self.board_rect.h / 8

        for name in cr.pieces_sprite_dict :
            sprite = cr.pieces_sprite_dict[name]
            if sprite.raw_surface.get_height() > tallest_piece.raw_surface.get_height() :
                tallest_piece = sprite

        tallest_piece.transform_by_height(h)
        rel = tallest_piece.get_diff()

        for name in cr.pieces_sprite_dict :
            sprite = cr.pieces_sprite_dict[name]
            sprite.transform_by_rel(rel[0], rel[1])


    def render_pieces( self ) :
        for uci in self.pieces_map :
            piece_name = self.pieces_map[uci]
            rect = self.board_map[uci]
            piece_rect = cr.pieces_sprite_dict[piece_name].transformed_surface.get_rect()
            piece_rect.center = rect.center

            cr.screen.blit(cr.pieces_sprite_dict[piece_name].transformed_surface, piece_rect)


    def check_pieces_moving( self ) :
        if not cr.event_holder.mouse_pressed_keys[0] :
            return

        for uci in self.board_map :
            rect = self.board_map[uci]
            if not cr.event_holder.mouse_rect.colliderect(rect) :
                continue

            if self.selected_piece is None :
                if uci in self.pieces_map:
                    piece = self.pieces_map[uci]
                    if (piece.islower() and self.turn == 'black') or \
                            (piece.isupper() and self.turn == 'white'):

                        self.selected_piece = uci
            else :
                if uci != self.selected_piece:
                    if self.move(self.selected_piece+uci):
                        self.selected_piece = None
                        self.update()



    def check_events( self ) :
        self.check_pieces_moving()


    def render( self ) :
        cr.screen.blit(self.board_sprite.transformed_surface, [0, 0])
        self.render_pieces()  # pg.draw.rect(cr.screen,[0,0,0],self.board_rect,width=20)


    @property
    def turn( self ) :
        result = 'black'
        if self.board.turn :
            result = 'white'

        return result

    def move( self,uci ):
        if chess.Move.from_uci(uci) in self.board.legal_moves:
            self.board.push_uci(uci)
            return True

        return False
