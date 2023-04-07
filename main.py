import pygame as pg
from pygame.locals import *

from core.game import Game
from core.event_holder import EventHolder
from core import common_resources as cr

pg.init()

cr.screen = pg.display.set_mode([720,720])
cr.event_holder = EventHolder()

game = Game()

while not cr.event_holder.should_quit:
    cr.event_holder.get_events()
    game.check_events()
    game.render()
    pg.display.update()