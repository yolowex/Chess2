import pygame as pg
from pygame.locals import *

from core.event_holder import EventHolder
from core import common_resources as cr

pg.init()

cr.screen = pg.display.set_mode([800,640])
cr.event_holder = EventHolder()



while not cr.event_holder.should_quit:
    cr.event_holder.get_events()
