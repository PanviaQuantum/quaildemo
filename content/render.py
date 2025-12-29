# render.py
# contains dictionaries and subroutines to draw circuit elements
# timeslices composed of multiverse, gate, multi-gate and wire elements
# 
from operation import operation
from baseparams import localparams
from colorkey import colorkey
from textkey import textkey
import numpy as np
import math

mvgap = 15

class draw:
   def renderNode( qnode, ax, mvLookup, x, y, x_scale, y_scale, color, fill, text=None, font=None ):
      # print( qnode.node.operation + ' ' + qnode.node.dependent )
      # adjust vertical position using mvLookup by qubit name
      mv,v,(xpane,ypane) = mvLookup[ qnode.node.dependent ]
      mvy = v * mvgap        # delta = 50% of line
      py = y - ypane - mvy   # - is down
      px = x + xpane

      if qnode.node.operation == 'Store':
         text = qnode.node.dependent
         g = localparams('store', px, py, x_scale, y_scale, color, fill, text=text, font=font )    # draw params
         g.render(ax)                # execute draw from params

         # convert qubit phase to p(|0>) = probability of |0> state
         phase = qnode.node.phase
         radians = phase * 2 * np.pi
         mag = math.cos(radians)
         probability = mag* mag
         g = localparams('state', px, py, x_scale, y_scale, color, None, probability=probability )    # draw params
      elif qnode.node.operation == 'Trace':
         text = qnode.node.dependent
         g = localparams('trace', px, py, x_scale, y_scale, color, fill, text=text, font=font )    # draw params
      else:
         text = qnode.node.operation
         g = localparams('gate1', px, py, x_scale, y_scale, color, fill, text=text, font=font )    # draw params

      g.render(ax)                # execute draw from params
      return

   def renderNodes( qnodes, ax, mvLookup, x, y0, y1, x_scale, y_scale, color, fill ):
      # print( qnodes.node.operation + ' ' + qnodes.node.dependent+ ' ' + qnodes.node.independent )
      # adjust vertical position using mvLookup by qubit name
      mv0,v,(xpane,ypane) = mvLookup[ qnodes.node.dependent ]
      mv1,v,(xpane,ypane) = mvLookup[ qnodes.node.independent ]
      assert mv0 == mv1     # gates must be in the same multiverse
      mvy = v * mvgap        # delta = 50% of line
      py0 = y0 - ypane - mvy    # - is down
      py1 = y1 - ypane - mvy    # - is down
      px = x + xpane

      g0 = localparams('target', px, py0, x_scale, y_scale, color, fill )    # draw params
      g1 = localparams('control', px, py1, x_scale, y_scale, color, fill )  
      if y0 > y1:
         g2 = localparams('linedown', px, py0, x_scale, y_scale, color, None )    # draw params
         g3 = localparams('lineup', px, py1, x_scale, y_scale, color, None )   
      else:
         g2 = localparams('lineup', px, py0, x_scale, y_scale, color, None )    # draw params
         g3 = localparams('linedown', px, py1, x_scale, y_scale, color, None ) 

      g0.render(ax)                # execute draw from params
      g1.render(ax)                
      g2.render(ax)                
      g3.render(ax)                
      return

   def renderMulti( multiverseOp, ax, mvLookup, x, y, dy, x_scale, y_scale, color, text=None, font=None  ):
      if multiverseOp.operation == 'Connect':
         # print( 'multiverseOp ' + str(multiverseOp.index) )
         q = multiverseOp.group[0]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy    # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
         palette = colorkey()
         fill = palette.color(mv)
         # print(fill)
         g = localparams('connect', px, py, x_scale, y_scale, color=color, fill=fill )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_top', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params

         text = multiverseOp.operation    # label middle connect
         by = dy
         for q in multiverseOp.group[1:-1]:
            mv,v,(xpane,ypane) = mvLookup[ q ]
            mvy = v * mvgap        # delta = 50% of line
            py = y - ypane - mvy + by    # - is down
            px = x + xpane
            # print( q + ' mv ' + str(mv))
            g = localparams('connect', px, py, x_scale, y_scale, color=color, fill=fill, text=text, font=font )    # draw params
            g.render(ax)                # execute draw from params
            by += dy

         q = multiverseOp.group[-1]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy + by   # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
        
         g = localparams('connect', px, py, x_scale, y_scale, color=color, fill=fill )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_bottom', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params
         #####################################################################################
      elif multiverseOp.operation == 'Teleport':
         # print( 'multiverseOp ' + str(multiverseOp.index) )
         q = multiverseOp.group[0]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy    # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
         palette = colorkey()
         fill = palette.color(mv)
         # print(fill)
         g = localparams('teleport', px, py, x_scale, y_scale, color=color, fill=fill )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_top', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params

         text = multiverseOp.operation    # label middle connect
         by = dy
         for q in multiverseOp.group[1:-1]:
            mv,v,(xpane,ypane) = mvLookup[ q ]
            mvy = v * mvgap        # delta = 50% of line
            py = y - ypane - mvy + by    # - is down
            px = x + xpane
            # print( q + ' mv ' + str(mv))
            g = localparams('teleport', px, py, x_scale, y_scale, color=color, fill=fill, text=text, font=font )    # draw params
            g.render(ax)                # execute draw from params
            by += dy

         q = multiverseOp.group[-1]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy + by   # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
        
         g = localparams('teleport', px, py, x_scale, y_scale, color=color, fill=fill )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_bottom', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params
         #####################################################################################
      elif multiverseOp.operation == 'Collapse':
         # print( 'multiverseOp ' + str(multiverseOp.index) )
         q = multiverseOp.group[0]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy    # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
         if multiverseOp.observe[0] == True:
            g = localparams('measure', px, py, x_scale, y_scale, color, None )    # draw params
         else:
            g = localparams('teleport', px, py, x_scale, y_scale, color, None )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_top', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params

         i = 1
         by = dy
         for q in multiverseOp.group[1:-1]:
            mv,v,(xpane,ypane) = mvLookup[ q ]
            mvy = v * mvgap        # delta = 50% of line
            py = y - ypane - mvy + by    # - is down
            px = x + xpane
            # print( q + ' mv ' + str(mv))
            if multiverseOp.observe[i] == True:
               g = localparams('measure', px, py, x_scale, y_scale, color, None )    # draw params
            else:
               g = localparams('teleport', px, py, x_scale, y_scale, color, None )    # draw params
            g.render(ax)                # execute draw from params
            by += dy
            i += 1

         q = multiverseOp.group[-1]
         mv,v,(xpane,ypane) = mvLookup[ q ]
         mvy = v * mvgap        # delta = 50% of line
         py = y - ypane - mvy + by   # - is down
         px = x + xpane
         # print( q + ' mv ' + str(mv))
         if multiverseOp.observe[i] == True:
            g = localparams('measure', px, py, x_scale, y_scale, color, None )    # draw params
         else:
            g = localparams('teleport', px, py, x_scale, y_scale, color, None )    # draw params
         g.render(ax)                # execute draw from params
         h = localparams('connect_bottom', px, py, x_scale, y_scale, color, None )    # draw params
         h.render(ax)                # execute draw from params
      return

   def renderWire( qubit, ax, mvLookup, x, y, x_scale, y_scale, color ):
      # print( qubit )
      # adjust vertical position using mvLookup by qubit name
      mv,v,(xpane,ypane) = mvLookup[ qubit ]
      mvy = v * mvgap        # delta = 50% of line
      py = y - ypane - mvy    # - is down
      px = x + xpane

      g = localparams('line', px, py, x_scale, y_scale, color, None )    # draw params
      g.render(ax)                # execute draw from params
      return


