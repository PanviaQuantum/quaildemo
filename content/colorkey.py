# colorkey.py
# class contains palette and random color selection function
import matplotlib.colors as mcolors
import random

class colorkey:
   def __init__(self):
      # Create palette exluding black and white
      colorlist = list(mcolors.CSS4_COLORS)
      self.palette = colorlist[8:-4]
      # print(self.palette)
      self.paletteSize = len(self.palette)
      # print(self.paletteSize)
      self.randpalette = random.shuffle( self.palette )

      # return color name for int i
   def color(self,i):
      j = i % self.paletteSize
      return self.palette[j]

      # return pseudo-random color name for int i
   def randcolor(self,i):
      j = i % self.paletteSize
      return self.randpalette[j]

      # return random color name for int i
   def randomcolor(self):
      j = random.randint( 0, self.paletteSize-1 )
      return self.palette[j]   

