# textkey.py
# class contains font properties and supplies font properties for plt.figtext
# plt.figtext( x, y, text, font, align )

import logging
logging.getLogger('matplotlib.font_manager').disabled = True
from matplotlib.font_manager import FontProperties

class textkey:
   def __init__(self,style,size):
      # Create a default font with passed style and size
      font0 = FontProperties()
      self.font = font0.copy()
      self.font.set_style(style)
      self.font.set_size(size)
      # print( self.font )
   def textfont(self):
      return self.font



