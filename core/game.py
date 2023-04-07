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
        self.selected_piece_valid_moves = []
        self.checkers_list = []

        self.promotion_choice = None
        self.update_pieces_map()

        self.promotion_panel_open = False
        self.promotion_panel_pieces = 'QRBN'
        self.onhold_promotion = None
        self.hovered_promotion_sections = None
        self.promotion_panel = FRect(0, 0, self.board_rect.w / 2, self.board_rect.h / 8)
        self.promotion_panel.center = cr.screen.get_rect().center
        self.promotion_panel_sections = [FRect(self.promotion_panel), FRect(self.promotion_panel),
            FRect(self.promotion_panel), FRect(self.promotion_panel), ]

        self.adjust_promotion_panel()
        self.ai_is_active = False

        self.bottom_panel = FRect(0, 0, cr.screen.get_width(), cr.screen.get_height())
        self.bottom_panel_speed = 3
        self.adjust_bottom_panel()
        self.resize_ui_elements()

        self.highlight_color = [150, 200, 150]
        self.move_color = [150, 150, 200]
        self.take_color = [200, 150, 150]
        self.check_color = [250, 20, 20]


    def adjust_bottom_panel( self ) :
        self.bottom_panel.h = cr.screen.get_height() * 0.05
        self.bottom_panel.y = cr.screen.get_width()


    def adjust_promotion_panel( self ) :
        w = self.board_rect.w / 8
        self.promotion_panel_sections[0].w = w
        self.promotion_panel_sections[1].x += w
        self.promotion_panel_sections[1].w = w
        self.promotion_panel_sections[2].x += w * 2
        self.promotion_panel_sections[2].w = w
        self.promotion_panel_sections[3].x += w * 3
        self.promotion_panel_sections[3].w = w


    def resize_ui_elements( self ) :
        for name in cr.ui_dict :
            sprite = cr.ui_dict[name]
            sprite.transform_by_height(self.bottom_panel.h * 0.8)


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
        self.fill_checkers_list()


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


    def check_pieces_moving( self ) :
        if cr.event_holder.mouse_pressed_keys[2] :
            self.selected_piece = None
            self.update_pieces_map()

        if not cr.event_holder.mouse_pressed_keys[0] :
            return

        for uci in self.board_map :
            rect = self.board_map[uci]
            if not cr.event_holder.mouse_rect.colliderect(rect) :
                continue

            if uci in self.pieces_map :
                piece = self.pieces_map[uci]
                if (piece.islower() and self.turn == 'black') or (
                        piece.isupper() and self.turn == 'white') :
                    self.selected_piece = None

            if self.selected_piece is None :
                if uci in self.pieces_map :
                    piece = self.pieces_map[uci]
                    if (piece.islower() and self.turn == 'black') or (
                            piece.isupper() and self.turn == 'white') :
                        self.selected_piece = uci
                        self.fill_selected_piece_valid_moves()
            else :
                if uci != self.selected_piece :
                    move = self.selected_piece + uci
                    if self.is_promotion(move) :
                        if self.promotion_choice is None :
                            self.promotion_panel_open = True
                            self.onhold_promotion = move
                            return

                    if self.move(move) :
                        self.selected_piece = None
                        self.update_pieces_map()


    def check_promotion_panel( self ) :
        if cr.event_holder.mouse_pressed_keys[2] :
            self.promotion_panel_open = False

        click = cr.event_holder.mouse_pressed_keys[0]
        for rect, c in zip(self.promotion_panel_sections,
                range(len(self.promotion_panel_sections))) :
            if cr.event_holder.mouse_rect.colliderect(rect) :
                self.hovered_promotion_sections = c
                if click :
                    self.promotion_choice = self.promotion_panel_pieces[c].lower()
                    if self.move(self.onhold_promotion + self.promotion_choice) :
                        self.selected_piece = None
                        self.selected_piece_valid_moves.clear()
                        self.update_pieces_map()

                    self.promotion_choice = None
                    self.promotion_panel_open = False
                    self.hovered_promotion_sections = False
                    break


    def check_bottom_panel( self ) -> bool :

        click = cr.event_holder.mouse_pressed_keys[0]

        for name, rect in zip(['undo', 'reset', 'ai', 'exit'],
                [self.ui_undo_rect, self.ui_reset_rect, self.ui_ai_rect, self.ui_exit_rect]):
            surface = cr.ui_dict[name].transformed_surface
            surface_rect = surface.get_rect()
            surface_rect.center = rect.center

            if cr.event_holder.mouse_rect.colliderect(surface_rect):
                if click:
                    if name == 'exit':
                        cr.event_holder.should_quit = True
                        return True
                    if name == 'undo':
                        self.undo()
                    if name == 'reset':
                        self.reset()
                    if name == 'ai':
                        self.trigger_ai()


        if cr.event_holder.mouse_pos.y > self.board_rect.y + self.board_rect.h or cr.event_holder.mouse_rect.colliderect(
            self.bottom_panel) :
            if self.bottom_panel.y > cr.screen.get_height() - self.bottom_panel.h :
                self.bottom_panel.y -= self.bottom_panel_speed

            return True

        if self.bottom_panel.y < cr.screen.get_height() :
            self.bottom_panel.y += self.bottom_panel_speed

        return False


    def check_events( self ) :
        if self.promotion_panel_open :
            self.check_promotion_panel()
        else :
            if not self.check_bottom_panel() :
                self.check_pieces_moving()


    def render_pieces( self ) :
        for uci in self.pieces_map :
            piece_name = self.pieces_map[uci]
            rect = self.board_map[uci]
            piece_rect = cr.pieces_sprite_dict[piece_name].transformed_surface.get_rect()
            piece_rect.center = rect.center

            cr.screen.blit(cr.pieces_sprite_dict[piece_name].transformed_surface, piece_rect)


    def render_valid_moves( self ) :
        if self.selected_piece is None :
            return

        for uci in self.selected_piece_valid_moves :
            target = uci[2 :]
            rect = self.board_map[target].copy()
            rect.x -= 1
            rect.y -= 1
            rect.w += 2
            rect.h += 2

            if target in self.pieces_map or self.board.is_en_passant(chess.Move.from_uci(uci)) :
                pg.draw.rect(cr.screen, self.take_color, rect)
            else :
                pg.draw.rect(cr.screen, self.move_color, rect, width=int(rect.w // 8))

        rect = self.board_map[self.selected_piece].copy()
        rect.x -= 1
        rect.y -= 1
        rect.w += 2
        rect.h += 2
        pg.draw.rect(cr.screen, self.highlight_color, rect, width=int(rect.w // 8))


    def render_checkers( self ) :
        for uci in self.checkers_list :
            rect = self.board_map[uci].copy()
            rect.x -= 1
            rect.y -= 1
            rect.w += 2
            rect.h += 2

            pg.draw.rect(cr.screen, self.check_color, rect)


    def render_promotion_panel( self ) :
        pg.draw.rect(cr.screen, self.highlight_color, self.promotion_panel)

        if self.hovered_promotion_sections is not None :
            pg.draw.rect(cr.screen, self.take_color,
                self.promotion_panel_sections[self.hovered_promotion_sections])

        for index, name in zip(range(4), self.promotion_panel_pieces) :
            if self.turn == 'black' :
                name = name.lower()

            surface = cr.pieces_sprite_dict[name].transformed_surface
            surface_rect = surface.get_rect()
            rect = self.promotion_panel_sections[index]
            surface_rect.center = rect.center
            cr.screen.blit(surface, surface_rect)


    def render_bottom_panel( self ) :
        pg.draw.rect(cr.screen, [130, 140, 160], self.bottom_panel)

        for name, rect in zip(['undo', 'reset', 'ai', 'exit'],
                [self.ui_undo_rect, self.ui_reset_rect, self.ui_ai_rect, self.ui_exit_rect]):
            surface = cr.ui_dict[name].transformed_surface
            surface_rect = surface.get_rect()
            surface_rect.center = rect.center
            cr.screen.blit(surface,surface_rect)

    def render( self ) :
        cr.screen.blit(self.board_sprite.transformed_surface, [0, 0])
        self.render_checkers()
        self.render_valid_moves()
        self.render_pieces()

        if self.promotion_panel_open :
            self.render_promotion_panel()

        self.render_bottom_panel()


    def undo( self ):
        try:
            self.board.pop()
            self.update_pieces_map()
        except IndexError:
            ...

    def reset( self ):
        self.board.reset()
        self.update_pieces_map()

    def trigger_ai( self ):
        self.ai_is_active = not self.ai_is_active
        text = 'activated ai'
        if not self.ai_is_active:
            text = 'de' + text

        print(text)


    @property
    def turn( self ) :
        result = 'black'
        if self.board.turn :
            result = 'white'

        return result


    @property
    def ui_undo_rect( self ) :
        rect = FRect(0, 0, self.bottom_panel.w * 0.2, self.bottom_panel.h)
        rect.x, rect.y = self.bottom_panel.x, self.bottom_panel.y
        rect.x += self.bottom_panel.w * 0
        return rect


    @property
    def ui_reset_rect( self ) :
        rect = FRect(0, 0, self.bottom_panel.w * 0.2, self.bottom_panel.h)
        rect.y = self.bottom_panel.y
        rect.x = self.ui_undo_rect.x + self.ui_undo_rect.w
        return rect


    @property
    def ui_ai_rect( self ) :
        rect = FRect(0, 0, self.bottom_panel.w * 0.2, self.bottom_panel.h)
        rect.y = self.bottom_panel.y
        rect.x = self.ui_reset_rect.x + self.ui_reset_rect.w
        return rect


    @property
    def ui_exit_rect( self ) :
        rect = FRect(0, 0, self.bottom_panel.w * 0.2, self.bottom_panel.h)
        rect.y = self.bottom_panel.y
        rect.x = self.bottom_panel.w - rect.w
        return rect


    def move( self, uci ) :
        if self.is_legal(uci) :
            self.board.push_uci(uci)
            return True

        return False


    def is_legal( self, uci ) :
        if self.is_promotion(uci) :
            uci += 'q'

        return chess.Move.from_uci(uci) in self.board.legal_moves


    def fill_selected_piece_valid_moves( self ) :
        self.selected_piece_valid_moves.clear()
        for uci in self.board_map :
            if self.selected_piece == uci :
                continue
            move = self.selected_piece + uci
            if self.is_legal(move) :
                self.selected_piece_valid_moves.append(move)


    def fill_checkers_list( self ) :
        self.checkers_list = self.get_checkers_coordination()


    def find_piece( self, name ) :
        for uci in self.pieces_map :
            piece = self.pieces_map[uci]
            if piece == name :
                return uci


    def get_checkers_coordination( self ) :
        if not self.board.is_check() :
            return []

        checkers = str(self.board.checkers()).split('\n')
        checkers = [[c for c in i if c != ' '] for i in checkers]
        result = []
        for row, digit in zip(checkers, '87654321') :
            for cell, letter in zip(row, 'abcdefgh') :
                if cell == '1' :
                    result.append(letter + digit)

        king = 'K'
        if self.turn == 'black' :
            king = 'k'

        result.append(self.find_piece(king))

        return result


    def is_promotion( self, uci ) :
        # Check if move is a pawn promotion
        if self.pieces_map[uci[:2]] in ['p', 'P'] :
            if uci[3 :] in ['1', '8'] :
                return True

        return False
