import hunspell
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class spellchecker:

    def __init__(self):
        self.hunspell_instance = hunspell.HunSpell("res/hunspell-en_US/en_US.dic", "res/hunspell-en_US/en_US.aff")

    def is_valid_word(self, word):
        return self.hunspell_instance.spell(word)

    def spellcheck_buff(self, event, builder):

        # get tag for misspelt words and data structures

        buff = builder.get_object("buff0")
        table = builder.get_object("tab0")
        tag = table.lookup("misspelt")

        start = buff.get_start_iter()
        end = buff.get_end_iter()

        wstart = Gtk.TextIter.copy(end)
        wstart.backward_word_start()
        wend = Gtk.TextIter.copy(wstart)
        wend.forward_word_end()
        text = buff.get_text(wstart, wend, False)

        if self.is_valid_word(text):
            buff.remove_tag(tag, wstart, wend)
        else:
            buff.apply_tag(tag, wstart, wend)

        while not wstart.is_start:
            wstart.backward_word_start
            wend = Gtk.TextIter.copy(wstart)
            wend.forward_word_end()
            text = buff.get_text(wstart, wend, False)
            if self.is_valid_word(text):
                buff.remove_tag(tag, wstart, wend)
            else:
                buff.apply_tag(tag, wstart, wend)