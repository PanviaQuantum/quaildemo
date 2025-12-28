# baseparams.py 
# contains dictionaries of shape coordinate tuple lists for render function
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# baseprims define the format of following items in list
# Default is line as sequences of x,y tuples with None for line breaks
baseprims = { 'line': ('x','y'), 'circle': ('radius','center'), 'fill': 'color' }

baseparams = { 'line' : [(-10,0),(10,0),None],
               'store' : [(-10,-10),(-8,-8),(8,-8),(10,0),(8,8),(-8,8),(-10,10),None],
               'state' : [(-20,-10),(-20,10),(-10,10),(-10,-10),(-20,-10),None],
               'gate1' : [(-6,-8),(6,-8),(6,8),(-6,8),(-6,-8),None,(-10,0),(-6,0),None,(6,0),(10,0),None],
               'control' : [(-10,0),(10,0),'circle',2,(0,0),'fill','black'],
               'target' : [(-10,0),(10,0),None,(0,5),(0,-5),'circle',5,(0,0)],
               'crot' : [(-10,0),(10,0),None,(-1.41,-1.41),(1.41,1.41),None,(-1.41,1.41),(-1.41,1.41),'circle',0.75,(0,0),'fill','red'],
               'connect' : [(-7,-10),(-7,10),None,(7,-10),(7,10),None,(-10,0),(-7,0),None,(7,0),(10,0),'white',(-7,10),(7,10),(7,-10),(-7,-10),'fill','grey'],
               'connect_top' : [(-7,10),(7,10),None],
               'connect_bottom' : [(-7,-10),(7,-10),None],
               'linethru' : [(0,10),(0,-10),None],
               'lineup' : [(0,0),(0,10),None],
               'linedown' : [(0,0),(0,-10),None],
               'pass' : [(-6,8),(-6,-8),None,(6,8),(6,-8),None],
               'measure' : [(-7,10),(-6,8),(-6,-8),(-7,-10),None,(-10,0),(-6,0),None,(6,0),(10,0),None,(7,10),(6,8),(6,-8),(7,-10),'red',6,(-3.53,3.63),(-2.5,4.43),'orange',(-2.5,4.43),(-1.29,4.93),'yellow',(-1.29,4.93),(0,5.1),'lightcyan',(0,5.1),(1.29,4.93),'greenyellow',(1.29,4.93),(2.5,4.43),'green',(2.5,4.43),(3.53,3.63),'silver',2,(0,-2.75),(0,4.75),None,(-0.5,4),(0,4.75),None,(0.5,4),(0,4.75),None],
               'top' : [(-6,8),(6,8),None],
               'bottom' : [(-6,-8),(6,-8),None],
               'teleport' : [(-7,-10),(-7,10),None,(7,-10),(7,10),None,(-10,0),(-7,0),None,(7,0),(10,0),'red',(-5,10),(-5.59,9),(-5.95,8),(-5.95,7),(-5.59,6),(-5,5),(-4.41,4),(-4.05,3),(-4.05,2),(-4.41,1),(-5,0),(-5.59,-1),(-5.95,-2),(-5.95,-3),(-5.59,-4),(-5,-5),(-4.41,-6),(-4.05,-7),(-4.05,-8),(-4.41,-9),(-5,-10),'orange',(-3,10),(-3.59,9),(-3.95,8),(-3.95,7),(-3.59,6),(-3,5),(-2.41,4),(-2.05,3),(-2.05,2),(-2.41,1),(-3,0),(-3.59,-1),(-3.95,-2),(-3.95,-3),(-3.59,-4),(-3,-5),(-2.41,-6),(-2.05,-7),(-2.05,-8),(-2.41,-9),(-3,-10),'yellow',(-1,10),(-1.59,9),(-1.95,8),(-1.95,7),(-1.59,6),(-1,5),(-0.41,4),(-0.05,3),(-0.05,2),(-0.41,1),(-1,0),(-1.59,-1),(-1.95,-2),(-1.95,-3),(-1.59,-4),(-1,-5),(-0.41,-6),(-0.05,-7),(-0.05,-8),(-0.41,-9),(-1,-10),'lightcyan',(1,10),(0.41,9),(0.05,8),(0.05,7),(0.41,6),(1,5),(1.59,4),(1.95,3),(1.95,2),(1.59,1),(1,0),(0.41,-1),(0.05,-2),(0.05,-3),(0.41,-4),(1,-5),(1.59,-6),(1.95,-7),(1.95,-8),(1.59,-9),(1,-10),'greenyellow',(3,10),(2.41,9),(2.05,8),(2.05,7),(2.41,6),(3,5),(3.59,4),(3.95,3),(3.95,2),(3.59,1),(3,0),(2.41,-1),(2.05,-2),(2.05,-3),(2.41,-4),(3,-5),(3.59,-6),(3.95,-7),(3.95,-8),(3.59,-9),(3,-10),'green',(5,10),(4.41,9),(4.05,8),(4.05,7),(4.41,6),(5,5),(5.59,4),(5.95,3),(5.95,2),(5.59,1),(5,0),(4.41,-1),(4.05,-2),(4.05,-3),(4.41,-4),(5,-5),(5.59,-6),(5.95,-7),(5.95,-8),(5.59,-9),(5,-10),None],
               'trace' : [(-10,0),(-5,0),None,(5,0),(10,0),'red',(-5,-6),(-4,-5.41),(-3,-5.05),(-2,-5.05),(-1,-5.41),(0,-6),(1,-6.59),(2,-6.95),(3,-6.95),(4,-6.59),(5,-6),'orange',(-5,-4),(-4,-3.41),(-3,-3.05),(-2,-3.05),(-1,-3.41),(0,-4),(1,-4.59),(2,-4.95),(3,-4.95),(4,-4.59),(5,-4),'yellow',(-5,-2),(-4,-1.41),(-3,-1.05),(-2,-1.05),(-1,-1.41),(0,-2),(1,-2.59),(2,-2.95),(3,-2.95),(4,-2.59),(5,-2),'lightcyan',(-5,0),(-4,0.59),(-3,0.95),(-2,0.95),(-1,0.59),(0,0),(1,-0.59),(2,-0.95),(3,-0.95),(4,-0.59),(5,0),'greenyellow',(-5,2),(-4,2.59),(-3,2.95),(-2,2.95),(-1,2.59),(0,2),(1,1.41),(2,1.05),(3,1.05),(4,1.41),(5,2),'green',(-5,4),(-4,4.59),(-3,4.95),(-2,4.95),(-1,4.59),(0,4),(1,3.41),(2,3.05),(3,3.05),(4,3.41),(5,4),'black','circle',10,(0,0)]
              }

# Codify elements into localparam objects for rendering
# probability p(|0>) = 1 - p(|1>) is an optional variable passed for state
class localparams:
   def __init__(self,element,x,y,xscale,yscale,color,fill,text=None,font=None,probability=None,linewidth=1):
      self.element = element
      self.x = x
      self.y = y
      self.xscale = xscale
      self.yscale = yscale
      self.color = color
      self.fill = fill
      self.text = text
      self.font = font
      self.probability = probability
      self.linewidth = linewidth
   def render(self,ax):
      if self.element in baseparams == False:
         print("Error in render: element not in baseparams")
         return
      # create x and y arrays for passing to matplotlib
      x = []
      y = []
      pcolor = self.color    # pcolor can change
      plinewidth = self.linewidth  # plinewidth also can change
      pradius = 1.0
      pcenter = tuple((0,0))
      pfill = 'black'
      plist = baseparams[self.element]   # list of draw params for this element
      pargs = 0
      pop = None
      for op in plist:
         if pargs > 0:      # process arguments of a primitive
            if pargs == 2 and pop == 'circle':
               pradius = op
               #print(str(pradius))
            elif pargs == 1 and pop == 'circle':
               #print(op)
               pcenter = tuple(op)
               #print(str(pcenter))
            elif pargs == 1 and pop == 'fill':
               pfill = op
            else:
               print("Error in render parse args " + str(op))
               return
            pargs -= 1
            if pargs == 0 and pop == 'circle':
               if len(x) > 1:
                  ax.plot(x,y,linestyle='-',c=pcolor,linewidth=plinewidth)   # add line to plot
               xt = self.x + pcenter[0]
               yt = self.y + pcenter[1]
               # print(str(xt)+','+str(yt))
               verts = int(10 * pradius) + 8      # radius * 10 = vertices + 8
               theta = np.linspace( 0, 2 * np.pi, verts)
               pxradius = pradius * 0.5
               x = xt + (pxradius * np.cos(theta))
               y = yt + (pradius * np.sin(theta))
               #print(x1)
               #print(y1)
               ax.plot(x,y,linestyle='-',c=self.color)   # add line to plot
               pop = None
               #-------------------------------------------------------------
            elif pargs == 0 and pop == 'fill':
               if self.element == 'connect':
                  rcolor = self.fill
               else:
                  rcolor = pfill    # use color in param list
               ax.fill(x,y,facecolor=rcolor)
               pop = None
               #-------------------------------------------------------------
         elif op == None or op in mcolors.CSS4_COLORS:      # separation
            if len(x) > 1:
               ax.plot(x,y,linestyle='-',c=pcolor,linewidth=plinewidth)   # add line to plot
               if op != None:
                  pcolor = mcolors.CSS4_COLORS[op]
               # Test if this is a variable element for probability
               if self.element == 'state' and self.probability != None:
                  midy = ( self.probability * 20 )    # red bottom delta = green bar height
                  topdelta = midy - 20                # top delta = height 
                  # print( 'prob ' + str(self.probability) + ', midy ' + str(midy))
                  greenbar_y = y.copy() 
                  greenbar_y[1] += topdelta   # split adjusts top
                  greenbar_y[2] += topdelta
                  redbar_y = y.copy()
                  redbar_y[0] += midy     # split adjusts bottom
                  redbar_y[3] += midy
                  redbar_y[4] += midy
                  ax.fill( x, redbar_y, facecolor = 'red' )
                  ax.fill( x, greenbar_y, facecolor = 'green' )
               x.clear()
               y.clear()
               #-------------------------------------------------------------
         elif type(op) == int or type(op) == float:     
            plinewidth = op         # set width of next line section
         elif type(op) == tuple:
            xt = self.x + op[0]
            yt = self.y + op[1]
            x.append(xt)    # combine local and base coordinates
            y.append(yt)
         elif type(op) == str:
            # print(op)
            if op in baseprims == False:
               print("Error in render: element not in baseprims")
               return
            args = baseprims[op]
            if op == 'circle':
               pop = op
               pargs = 2         # radius and centre
            elif op == 'fill':
               pop = op
               pargs = 1         # fill color name

            # print(str(args) + ' = ' + str(pargs))
         else:
            print("Error in render: unrecognized op " + str(op) )
            return
      ###############   end of list processing loop ############
      if self.text != None and self.font != None:
         if self.text == 'Connect':
            bbox = {'fc': '0.8', 'pad': 4}
            props = {'ha':'center', 'va': 'center', 'bbox': bbox }
            ax.text( self.x, self.y, self.text, props, rotation=45 )
            print(self.text)
         else:
            # print(self.text)
            d = self.font.get_size() * 0.45
            w = len(self.text) * d * 0.25  # 0.155
            # print(w)
            position = ( self.x - w, self.y - d )
            ax.annotate( self.text, xy = position, xycoords='data')


