# Copyright (C) Benjamin James Read, 2022 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Benjamin Read <benjamin-read@hotmail.co.uk>, January 2022

# imports for GTK 3+

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

# import for spellchecker class

from spellcheck import spellchecker

# import button handler function

import butHandlers

# handler for keypress events

def keypress_handler(widget, event):

    # get key pressed

    key = event.keyval

    # handle case that escape key was pressed

    if key == Gdk.KEY_Escape:
        Gtk.main_quit()

# handler for activation of application

def activate(args):

    # create new gtk builder and pull in glade file widgets

    builder = Gtk.Builder()
    builder.add_from_file("res/editorMain.glade")

    # get window widget from builder and post main_quit as handler for window end

    window = builder.get_object("editorMain1")
    window.connect("destroy", Gtk.main_quit)

    # get css for window styles and display it

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_path("res/buk.css")
    context = Gtk.StyleContext()
    screen = Gdk.Screen.get_default()
    context.add_provider_for_screen(screen, cssprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # get the default text buffer and connect up some text tags for it

    buff = builder.get_object("buff0")
    buff.create_tag("bold", weight=700)
    buff.create_tag("ital", style=Pango.Style.ITALIC)
    buff.create_tag("uline", underline=Pango.Underline.SINGLE)
    buff.create_tag("sthru", strikethrough=True)
    buff.create_tag("ljust", justification=Gtk.Justification.LEFT)
    buff.create_tag("rjust", justification=Gtk.Justification.RIGHT)
    buff.create_tag("cjust", justification=Gtk.Justification.CENTER)
    buff.create_tag("fjust", justification=Gtk.Justification.FILL)

    # get toolbuttons

    butBold = builder.get_object("butBold")
    butItal = builder.get_object("butItal")
    butUline = builder.get_object("butUline")
    butSthru = builder.get_object("butSthru")
    butIndent = builder.get_object("butIndent")
    butUnindent = builder.get_object("butUnindent")
    butCjust = builder.get_object("butCjust")
    butLjust = builder.get_object("butLjust")
    butRjust = builder.get_object("butRjust")
    butFjust = builder.get_object("butFjust")
    butSaveas = builder.get_object("butSaveas")
    butOpen = builder.get_object("butOpen")
    butPaste = builder.get_object("butPaste")

    # connect up event handler for each toolbutton

    butBold.connect("clicked", butHandlers.togleable_clicked_handler, builder, "bold")
    butItal.connect("clicked", butHandlers.togleable_clicked_handler, builder, "ital")
    butSthru.connect("clicked", butHandlers.togleable_clicked_handler, builder, "sthru")
    butUline.connect("clicked", butHandlers.togleable_clicked_handler, builder, "uline")
    butIndent.connect("clicked", butHandlers.indent, builder)
    butUnindent.connect("clicked", butHandlers.unindent, builder)
    butLjust.connect("clicked", butHandlers.justify_clicked_handler, builder, "ljust")
    butRjust.connect("clicked", butHandlers.justify_clicked_handler, builder, "rjust")
    butCjust.connect("clicked", butHandlers.justify_clicked_handler, builder, "cjust")
    butFjust.connect("clicked", butHandlers.justify_clicked_handler, builder, "fjust")
    butSaveas.connect("activate", butHandlers.saveas_activate_handler, builder)
    butOpen.connect("activate", butHandlers.open_activate_handler, builder)
    butPaste.connect("clicked", butHandlers.paste_clicked_handler, builder)

    # create spellcheck instance using hunspell, and connect handler for text changes

    spellcheck = spellchecker()
    buff.connect("changed", spellcheck.spellcheck_buff, builder)
    
    # connect signal handler for keypress events

    window.connect("key_press_event", keypress_handler)

    # show the window and its contents 

    window.show_all()

def launchGraphics():

    # create new application, connect activation handler and trigger it

    app = Gtk.Application.new("in.Buk", 0)
    app.connect("activate", activate)
    app.run()

    # run GTK main to begin run loop

    ret = Gtk.main()
    return ret