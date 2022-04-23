import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib


# a helper function to see whether a tag is ever inactive in an iter range

def tag_complete(buff, tag, start, end):

    ret = False

    if start.has_tag(tag):
        next_toggle = Gtk.TextIter.copy(start)
        gret = next_toggle.forward_to_tag_toggle(tag)
        if gret:
            if not next_toggle.in_range(start, end):
                ret = True
    
    return ret


# helper function to apply toggleable text tags to text

def apply_tog_tag(builder, tag):
    
    # get necessary data structures for apply tag call

    buff = builder.get_object("buff0")
    table = builder.get_object("tab0")

    # find selection bounds

    start, end = buff.get_selection_bounds()

    # if tag is present (and complete) remove it, otherwise add the tag

    if tag_complete(buff, tag, start, end):
        buff.remove_tag(tag, start, end)
    else:
        buff.apply_tag(tag, start, end)

# handles the clicked events for the toggleable formatters (bold, ital, sthru, uline)

def togleable_clicked_handler(self, builder, tag_id):

    table = builder.get_object("tab0")
    tag = table.lookup(tag_id)
    apply_tog_tag(builder, tag)

# handles the clicked event for indent toolbutton

def indent(self, builder):

    # constant pixel increment for each indent

    indentIncrement = 25

    # get critical data structures

    buff = builder.get_object("buff0")
    table = builder.get_object("tab0")

    # get tags on start of selection

    if buff.get_has_selection():
        start, end = buff.get_selection_bounds()
    else:
        start = buff.get_iter_at_mark(buff.get_insert())
        end = Gtk.TextIter.copy(start)
        end.forward_char()

    tags = start.get_tags()

    # tag found boolean, so we know whether to create a new indent tag

    tagFound = False

    # go through list of text tags applied to the iter, looking for ones with indent-set

    for tag in tags:
        if tag.get_property("indent-set"):

            tagFound = True

            # remove old tag

            buff.remove_tag(tag, start, end)

            # find previous indent value, increment and register if necessary

            previousIndent = tag.get_property("indent")
            newIndent = previousIndent + indentIncrement
            newName = "indent" + str(newIndent)
            newTag = table.lookup(newName)

            if newTag == None:
                buff.create_tag(newName, indent=newIndent)
                newTag = table.lookup(newName)
                buff.apply_tag(newTag, start, end)
            else:
                buff.apply_tag(newTag, start, end)

            break
    
    # if we didnt find a tag with an indent property, create a base tag
    if not tagFound:
        newTag = table.lookup("indent25")
        if newTag == None:
            buff.create_tag("indent25", indent=indentIncrement)
            
        newTag = table.lookup("indent25")
        buff.apply_tag(newTag, start, end)
    
    return True

# handles the clicked event for unindent toolbutton
            
def unindent(self, builder):

    # constant pixel increment for each indent

    indentIncrement = 25

    # get critical data structures

    buff = builder.get_object("buff0")
    table = builder.get_object("tab0")

    # get tags on start of selection

    if buff.get_has_selection():
        start, end = buff.get_selection_bounds()
    else:
        start = buff.get_iter_at_mark(buff.get_insert())
        end = Gtk.TextIter.copy(start)
        end.forward_char()

    tags = start.get_tags()

    # tag found boolean, so we know whether to create a new indent tag

    tagFound = False

    # go through list of text tags applied to the iter, looking for ones with indent-set

    for tag in tags:
        if tag.get_property("indent-set"):

            tagFound = True

            # remove old tag

            buff.remove_tag(tag, start, end)

            # find previous indent value, increment and register if necessary

            previousIndent = tag.get_property("indent")
            print(str(previousIndent))
            newIndent = previousIndent - indentIncrement
            if newIndent < 0:
                break
            newName = "indent" + str(newIndent)
            newTag = table.lookup(newName)

            if newTag == None:
                buff.create_tag(newName, indent=newIndent)
                newTag = table.lookup(newName)
                buff.apply_tag(newTag, start, end)
            else:
                buff.apply_tag(newTag, start, end)

            break
    
    return True

# handles the clicked event for justification toolbuttons

def justify_clicked_handler(self, builder, tag_id):
    
    # get necessary data structures

    buff = builder.get_object("buff0")
    table = builder.get_object("tab0")

    # get selection bounds

    if buff.get_has_selection():

        start, end = buff.get_selection_bounds()
        tags = start.get_tags()

        # tag found boolean, so we know whether to create a new justify tag

        tagFound = False

        for tag in tags:
            if tag.get_property("justification-set"):

                tagFound = True

                buff.remove_tag(tag, start, end)
                newTag = table.lookup(tag_id)
                buff.apply_tag(newTag, start, end)
                break

        if not tagFound:
            newTag = table.lookup(tag_id)
            buff.apply_tag(newTag, start, end)

# handles the activate event for saveas toolbutton

def saveas_activate_handler(self, builder):

    # get iters for start and end of buffer

    buff = builder.get_object("buff0")
    start = buff.get_start_iter()
    end = buff.get_end_iter()

    # register serialize format and serialize

    format = buff.register_serialize_tagset(None)
    txt = buff.serialize(buff, format, start, end)

    # open a dialog to select the save location

    dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        file_path = dialog.get_filename()
        GLib.file_set_contents(file_path, txt)
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")

    dialog.destroy()

# handles the activate event for open file toolbutton

def open_activate_handler(self, builder):

    # get end iter of text buffer to insert deserialized text
    
    buff = builder.get_object("buff0")
    end = buff.get_end_iter()

    dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        file_path = dialog.get_filename()
        result, des_content = GLib.file_get_contents(file_path)
        assert result
        # register dereialize tagset and deserialize data to text buffer

        format = buff.register_deserialize_tagset(None)
        text = buff.deserialize(buff, format, end, des_content)
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")

    dialog.destroy()

# signal handler for when overlay wants to allocate an image

def get_child_position(overlay, widget, allocation, width, height):
    allocation.x = 100
    allocation.y = 0
    allocation.width = width
    allocation.height = height
    return True

# callback for when clipboard returns data

def paste_callback(clipboard, pixbuf, builder):
    
    # using this as a macro becuse i don't know python

    eventImages = 2

    if eventImages == 0:

        overlay = builder.get_object("olay0")
        overlay.connect("get-child-position", get_child_position, pixbuf.get_width(), pixbuf.get_height())
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        eventbox = Gtk.EventBox.new()
        eventbox.add(image)
        overlay.add_overlay(eventbox)
        eventbox.show_all()

    elif eventImages == 1:

        # add child in window method of adding

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        view = builder.get_object("view0")
        view.add_child_in_window(image, Gtk.TextWindowType.TEXT, 0, 300)
        image.show()

    elif eventImages == 2:

        # add overlay method of adding

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        view = builder.get_object("view0")
        view.add_overlay(image, 0, 0)
        image.show()

    else:

        if pixbuf == None:
            print("Error, paste callback received no image")
        else:
            buff = builder.get_object("buff0")
            view = builder.get_object("view0")
            cursor = buff.get_iter_at_mark(buff.get_insert())
            buff.insert_pixbuf(cursor, pixbuf)

# handles the clicked event for paste button

def paste_clicked_handler(self, builder):

    display = Gdk.Display.get_default()
    clipboard = Gtk.Clipboard.get_default(display)
    clipboard.request_image(paste_callback, builder)
    return True