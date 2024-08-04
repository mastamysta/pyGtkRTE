# pyGtkRTE
RichTextEditor in Python GTK+3

![Screencast from 04-08-24 16_35_06](https://github.com/user-attachments/assets/f4af64f6-dc99-497b-a3ac-120e2d5ff91d)

This project is a rich text editor, with support for all expected rich-text editing functionality aswell as spell checking. Image processing is in development.

To run, this project requires GTK+3 to be installed aswell as Hunspell:
  
  sudo apt install python-gi python-gi-cairo python3-gi python3-gi-cairo gir1.2-gtk-3.0
  
  pip install hunspell

The project is organised into a few files:

- pyBuk.py contains the main() function. Therefore, to kick-off the program use python3 pyBuk.py

- maingraphics.py is called by main(), and sets up event handlers and the spell checker module.

- The spell checker module has been included in this repo, this allows the editor to dynamically highlight misspelt words.

- The bulk of the work is done in butHandlers.py. This contains subrouties to allow font changes, highlighting underlining e.t.c
