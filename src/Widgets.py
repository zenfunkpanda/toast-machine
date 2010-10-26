#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors: Quinn Storm (quinn@beryl-project.org)
#          Patrick Niklaus (marex@opencompositing.org)
#          Guillaume Seguin (guillaume@segu.in)
#          Christopher Williams (christopherw@verizon.net)
# Copyright (C) 2007 Quinn Storm


import pygtk
import gtk
import gtk.gdk
import gobject
import cairo, pangocairo
from math import pi, sqrt
import time
import re
import mimetypes
mimetypes.init()

import locale
import gettext
_ = gettext.gettext



# Edge selection widget
#
class EdgeSelector (gtk.DrawingArea):

    __gsignals__    = {"clicked" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_PYOBJECT,))}

    _base_surface   = None
    _surface        = None
    _radius         = 13
    _cradius        = 20
    _coords         = []

    def __init__ (self):
        '''Prepare widget'''
        super (EdgeSelector, self).__init__ ()
        background = "../data/icons/display.png"
        self._base_surface = cairo.ImageSurface.create_from_png (background)
        self.add_events (gtk.gdk.BUTTON_PRESS_MASK)
        self.connect ("expose_event", self.expose)
        self.connect ("button_press_event", self.button_press)
        self.set_size_request (196, 196)

        # Useful vars
        x0 = 16
        y0 = 24
        x1 = 181
        y1 = 133
        x2 = x0 + 39
        y2 = y0 + 26
        x3 = x1 - 39
        y3 = y1 - 26
        self._coords = (x0, y0, x1, y1, x2, y2, x3, y3)

    def draw (self, cr, width, height):
        '''The actual drawing function'''
        # Useful vars
        x0, y0, x1, y1, x2, y2, x3, y3 = self._coords
        cradius = self._cradius
        radius  = self._radius

        cr.set_line_width(1.0)

        # Top left edge
        cr.new_path ()
        cr.move_to (x0, y0 + cradius)
        cr.line_to (x0, y0)
        cr.line_to (x0 + cradius, y0)
        cr.arc (x0, y0, cradius, 0, pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "TopLeft")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "TopLeft")
        cr.stroke ()
        # Top right edge
        cr.new_path ()
        cr.move_to (x1, y0 + cradius)
        cr.line_to (x1, y0)
        cr.line_to (x1 - cradius, y0)
        cr.arc_negative (x1, y0, cradius, pi, pi/2)
        cr.close_path ()
        self.set_fill_color (cr, "TopRight")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "TopRight")
        cr.stroke ()
        # Bottom left edge
        cr.new_path ()
        cr.move_to (x0, y1 - cradius)
        cr.line_to (x0, y1)
        cr.line_to (x0 + cradius, y1)
        cr.arc_negative (x0, y1, cradius, 2 * pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "BottomLeft")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "BottomLeft")
        cr.stroke ()
        # Bottom right edge
        cr.new_path ()
        cr.move_to (x1, y1 - cradius)
        cr.line_to (x1, y1)
        cr.line_to (x1 - cradius, y1)
        cr.arc (x1, y1, cradius, pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "BottomRight")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "BottomRight")
        cr.stroke ()
        # Top edge
        cr.new_path ()
        cr.move_to (x2 + radius, y0)
        cr.line_to (x3 - radius, y0)
        cr.arc (x3 - radius, y0, radius, 0, pi / 2)
        cr.line_to (x2 + radius, y0 + radius)
        cr.arc (x2 + radius, y0, radius, pi / 2, pi)
        cr.close_path ()
        self.set_fill_color (cr, "Top")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Top")
        cr.stroke ()
        # Bottom edge
        cr.new_path ()
        cr.move_to (x2 + radius, y1)
        cr.line_to (x3 - radius, y1)
        cr.arc_negative (x3 - radius, y1, radius, 0, - pi / 2)
        cr.line_to (x2 + radius, y1 - radius)
        cr.arc_negative (x2 + radius, y1, radius, - pi / 2, pi)
        cr.close_path ()
        self.set_fill_color (cr, "Bottom")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Bottom")
        cr.stroke ()
        # Left edge
        cr.new_path ()
        cr.move_to (x0, y2 + radius)
        cr.line_to (x0, y3 - radius)
        cr.arc_negative (x0, y3 - radius, radius, pi / 2, 0)
        cr.line_to (x0 + radius, y2 + radius)
        cr.arc_negative (x0, y2 + radius, radius, 0, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "Left")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Left")
        cr.stroke ()
        # Right edge
        cr.new_path ()
        cr.move_to (x1, y2 + radius)
        cr.line_to (x1, y3 - radius)
        cr.arc (x1, y3 - radius, radius, pi / 2, pi)
        cr.line_to (x1 - radius, y2 + radius)
        cr.arc (x1, y2 + radius, radius, pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "Right")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Right")
        cr.stroke ()

    def set_fill_color (self, cr, edge):
        '''Set painting color for edge'''
        cr.set_source_rgb (0.9, 0.9, 0.9)

    def set_stroke_color (self, cr, edge):
        '''Set stroke color for edge'''
        cr.set_source_rgb (0.45, 0.45, 0.45)

    def redraw (self, queue = False):
        '''Redraw internal surface'''
        alloc = self.get_allocation ()
        # Prepare drawing surface
        width, height = alloc.width, alloc.height
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context (self._surface)
        # Draw background
        cr.set_source_surface (self._base_surface)
        cr.paint ()
        # Draw
        self.draw (cr, alloc.width, alloc.height)
        # Queue expose event if required
        if queue:
            self.queue_draw ()

    def expose (self, widget, event):
        '''Expose event handler'''
        cr = self.window.cairo_create ()
        if not self._surface:
            self.redraw ()
        cr.set_source_surface (self._surface)
        cr.rectangle (event.area.x, event.area.y,
                      event.area.width, event.area.height)
        cr.clip ()
        cr.paint ()
        return False

    def in_circle_quarter (self, x, y, x0, y0, x1, y1, x2, y2, radius):
        '''Args:
            x, y = point coordinates
            x0, y0 = center coordinates
            x1, y1 = circle square top left coordinates
            x2, y2 = circle square bottom right coordinates
            radius = circle radius'''
        if not self.in_rect (x, y, x1, y1, x2, y2):
            return False
        return self.dist (x, y, x0, y0) <= radius

    def dist (self, x1, y1, x2, y2):
        return sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def in_rect (self, x, y, x0, y0, x1, y1):
        return x >= x0 and y >= y0 and x <= x1 and y <= y1

    def button_press (self, widget, event):
        x, y = event.x, event.y
        edge = ""

        # Useful vars
        x0, y0, x1, y1, x2, y2, x3, y3 = self._coords
        cradius = self._cradius
        radius  = self._radius

        if self.in_circle_quarter (x, y, x0, y0, x0, y0,
                                   x0 + cradius, y0 + cradius,
                                   cradius):
            edge = "TopLeft"
        elif self.in_circle_quarter (x, y, x1, y0, x1 - cradius, y0,
                                     x1, y0 + cradius, cradius):
            edge = "TopRight"
        elif self.in_circle_quarter (x, y, x0, y1, x0, y1 - cradius,
                                     x0 + cradius, y1, cradius):
            edge = "BottomLeft"
        elif self.in_circle_quarter (x, y, x1, y1, x1 - cradius, y1 - cradius,
                                     x1, y1, cradius):
            edge = "BottomRight"
        elif self.in_rect (x, y, x2 + radius, y0, x3 - radius, y0 + radius) \
             or self.in_circle_quarter (x, y, x2 + radius, y0, x2, y0,
                                        x2 + radius, y0 + radius, radius) \
             or self.in_circle_quarter (x, y, x3 - radius, y0, x3 - radius, y0,
                                        x3, y0 + radius, radius):
            edge = "Top"
        elif self.in_rect (x, y, x2 + radius, y1 - radius, x3 - radius, y1) \
             or self.in_circle_quarter (x, y, x2 + radius, y1, x2, y1 - radius,
                                        x2 + radius, y1, radius) \
             or self.in_circle_quarter (x, y, x3 - radius, y1,
                                        x3 - radius, y1 - radius,
                                        x3, y1, radius):
            edge = "Bottom"
        elif self.in_rect (x, y, x0, y2 + radius, x0 + radius, y3 - radius) \
             or self.in_circle_quarter (x, y, x0, y2 + radius, x0, y2,
                                        x0 + radius, y2 + radius, radius) \
             or self.in_circle_quarter (x, y, x0, y3 - radius,
                                        x0, y3 - radius,
                                        x0 + radius, y3, radius):
            edge = "Left"
        elif self.in_rect (x, y, x1 - radius, y2 + radius, x1, y3 - radius) \
             or self.in_circle_quarter (x, y, x1, y2 + radius, x1 - radius, y2,
                                        x1, y2 + radius, radius) \
             or self.in_circle_quarter (x, y, x1, y3 - radius,
                                        x1 - radius, y3 - radius,
                                        x1, y3, radius):
            edge = "Right"

        if edge:
            self.emit ("clicked", edge, event)

# Edge selection widget
#
class SingleEdgeSelector (EdgeSelector):

    _current = []

    def __init__ (self, edge):
        '''Prepare widget'''
        EdgeSelector.__init__ (self)
        self._current = edge.split ("|")
        self.connect ('clicked', self.edge_clicked)

    def set_current (self, value):
        self._current = value.split ("|")
        self.redraw (queue = True)

    def get_current (self):
        return "|".join (filter (lambda s: len (s) > 0, self._current))
    current = property (get_current, set_current)

    def set_fill_color (self, cr, edge):
        '''Set painting color for edge'''
        if edge in self._current:
            cr.set_source_rgb (0.64, 1.0, 0.09)
        else:
            cr.set_source_rgb (0.80, 0.00, 0.00)

    def set_stroke_color (self, cr, edge):
        '''Set stroke color for edge'''
        if edge in self._current:
            cr.set_source_rgb (0.31, 0.60, 0.02)
        else:
            cr.set_source_rgb (0.64, 0.00, 0.00)

    def edge_clicked (self, widget, edge, event):
    	
        if not len (edge):
            return
			
        if self._current == [edge]:
		    self._current = [""]
        else:
            self._current = [edge]
        print self._current
        #if edge in self._current:
        #    self._current.remove (edge)
        #else:
        #    self._current.append (edge)

        self.redraw (queue = True)

