import pygame as pg

from core.game import Game
from core.event_holder import EventHolder
from core import common_resources as cr

pg.init()

cr.screen = pg.display.set_mode([720,720])
cr.event_holder = EventHolder()

game = Game()
clock = pg.time.Clock()
fps = 60
while not cr.event_holder.should_quit:
    cr.event_holder.get_events()
    game.check_events()
    game.render()
    pg.display.update()
    clock.tick(fps)