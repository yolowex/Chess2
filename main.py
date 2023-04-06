import pygame as pg
from pygame.locals import *

from core.event_holder import EventHolder

pg.init()

screen = pg.display.set_mode([800,640])
event_holder = EventHolder()

while not event_holder.should_quit:
    event_holder.get_events()
