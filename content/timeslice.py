# timeslice.py
# timeslice class contains the operations, gates and wires for all qubits
# tag dict for
# - populate data in any order 
# - render tiles in any order since position is encoded in lineIndex
from operation import operation
from render import draw
from textkey import textkey

# wire and node enable lookup of lineIndex by tag name
class wire:
   def __init__(self, name, lineIndex):
      self.name = name
      self.lineIndex = lineIndex

class node(wire):
   def __init__(self, activity, name, lineIndex ):
      self.activity = activity
      self.name = name
      self.lineIndex = lineIndex

class multiverse:
   def __init__(self, operation, group, index, startLine = None, lastLine = None ):
      self.operation = operation   # 'Connect', 'Teleport' 
      self.group = []   # build a list of qubit names
      for x in group:
         self.group.append( x['tag']['key'] )    # list of tags
      self.index = index    # index of multiverse
      self.size = len(self.group)  # size of multiverse
      self.lineIndexStart = startLine
      self.lineIndexEnd   = lastLine

class collapse:
   def __init__(self, operation, group, observe, index, startLine = None, lastLine = None ):
      self.operation = operation   # 'Collapse' 
      self.observe = observe
      self.group = []   # build a list of qubit names
      for x in group:
         self.group.append( x['tag']['key'] )    # list of tags
      self.index = index    # index of multiverse
      self.size = len(self.group)  # size of multiverse
      self.lineIndexStart = startLine
      self.lineIndexEnd   = lastLine

class timeslice:
   def __init__(self, sliceIndex):
      self.sliceIndex = sliceIndex
      self.wires = []     # no activity
      self.node1 = []     # single qubit activity
      self.node2 = []     # >= two qubit activity
      self.worlds = []    # multiverse lists of activity
      self.left = None    # connector  
      self.right = None   # connector  
      # print('timeslice ' + str(sliceIndex))

   # organize partitions commands into wires, nodes and worlds of nodes
   # direction = -1 if adjacent timeslice is later
   # direction = 1 if adjacent timeslice is earlier
   def organize(self,commands,adjacent,direction):
      # parse the commands to a list of activity nodes
      activity = []
      worldsData = []    # 2nd pass to process multiverse Connect
      for x in commands:
         op = operation()
         category = op.parse(x)
         activity.append(op)
         # Partition to single node, dual node or multi-node activity
         if category == 1:
            self.node1.append(op)
         elif category == 2:
            self.node2.append(op)
         else:
            worldsData.append(op)

      if adjacent == None:
         ##########################################################
         if activity[0].node.operation == 'Connect' or activity[0].node.operation == 'Teleport':
            # seed for layout
            # 2nd pass to process multiverse Connect items
            # Assign lineIndex to multiverse items
            lineIndex = 0
            self.left = []
            self.right = []
            for mvdata in worldsData:
                lastlineIndex = lineIndex + len(mvdata.node.dependent) - 1
                mv = multiverse( activity[0].node.operation, mvdata.node.dependent, mvdata.node.index, lineIndex, lastlineIndex )
                self.worlds.append(mv)
                for x in mv.group:
                   self.left.append(x)
                   self.right.append(x)
                lineIndex = lastlineIndex + 1
            # print(self.left)
            # print('-------')
            # print(self.right)
            # Completed seed timeslice
            #######################################################
         elif activity[0].node.operation == 'Store':
            assert False, 'add code here..'

         else:
            assert False, 'add code here..'

         ##########################################################
      elif direction < 0:
         # propating backwards from seed
         # print(self.sliceIndex)
         # print('\nadjacent.left ')
         # print( adjacent.left )
         self.right = adjacent.left.copy()   # duplicate
         self.wires = self.right.copy()      # duplicate
         self.left = self.right.copy()       # duplicate
         if len(self.node1) > 0 and len(self.wires) > 0:
            for x in self.node1:
               if x.node.dependent in self.wires:
                  self.wires.remove(x.node.dependent)
                  if x.node.operation == 'Store':
                     nodei = self.left.index(x.node.dependent)
                     print(x.node.operation + x.node.dependent + ' ' + str(nodei) )
                     self.left[ nodei ] = None  # no left propagation
         if len(self.node2) > 0 and len(self.wires) > 0:
            for x in self.node2:
               if x.node.dependent in self.wires:
                  self.wires.remove(x.node.dependent)
               if x.node.independent in self.wires:
                  self.wires.remove(x.node.independent)
         # wires now contains all the no activity qubits in this timeslice
         # print('\nself.wires')
         # print( self.wires )
         ##########################################################

      elif activity[0].node.operation == 'Collapse':
         # propating forwards from seed reaches a collapse event
         self.left = adjacent.right.copy()   # duplicate
         # pass observe to process multiverse Collapse items for observe 
         # Assign lineIndex to multiverse items
         lineIndex = 0
         for mvdata in worldsData:
             lastlineIndex = lineIndex + len(mvdata.node.dependent) - 1
             xv = collapse( 'Collapse', mvdata.node.dependent, mvdata.node.observe, mvdata.node.index, lineIndex, lastlineIndex )
             self.worlds.append(xv)
             lineIndex = lastlineIndex + 1

         ##########################################################
      else:
         # propating forwards from seed
         # print(self.sliceIndex)
         # print('\nadjacent.right ')
         # print( adjacent.right )
         self.left = adjacent.right.copy()   # duplicate
         self.wires = self.left.copy()       # duplicate
         self.right = self.left.copy()       # duplicate
         if len(self.node1) > 0 and len(self.wires) > 0:
            for x in self.node1:
               if x.node.dependent in self.wires:
                  self.wires.remove(x.node.dependent)
         if len(self.node2) > 0 and len(self.wires) > 0:
            for x in self.node2:
               if x.node.dependent in self.wires:
                  self.wires.remove(x.node.dependent)
               if x.node.independent in self.wires:
                  self.wires.remove(x.node.independent)
         # wires now contains all the no activity qubits in this timeslice
         # print('\nself.wires')
         # print( self.wires )
     
      return

      #################################################################
      # ax is the axes render context added to matplotlib pyplot of fig
      # allows calling plot functions directly for rendering in the fig
   def render(self, ax, mvLookup, x, y, dx, dy, paneDim, x_scale, y_scale, color, fill ):

      # Create font generators
      fontgen = textkey('normal','small')
      font = fontgen.textfont()

      # draw single qubit gates
      for g in self.node1:
         iy = self.right.index(g.node.dependent) % paneDim    # obtain index from name
         gy = y + (iy * dy)
         draw.renderNode(g, ax, mvLookup, x, gy, x_scale, y_scale, color, fill, None, font )

      # use mvLookup to calculate vertical offset as multiple of multiverseIndex
      # draw multiverses
      ifontgen = textkey('italic','medium')
      ifont = ifontgen.textfont()

      for m in self.worlds:
         iy = m.lineIndexStart % paneDim    # obtain starting line index from multiverse
         gy = y + (iy * dy)
         draw.renderMulti(m, ax, mvLookup, x, gy, dy, x_scale, y_scale, color, None, ifont )

      # draw multi-qubit gates
      for g in self.node2:
         iy0 = self.right.index(g.node.dependent) % paneDim  # obtain index from name
         gy0 = y + (iy0 * dy)
         iy1 = self.right.index(g.node.independent) % paneDim   # obtain index from name
         gy1 = y + (iy1 * dy)

         draw.renderNodes(g, ax, mvLookup, x, gy0, gy1, x_scale, y_scale, color, fill )

      # draw no activity wires
      for w in self.wires:
         if w == None:
            continue
         iy = self.left.index(w) % paneDim    # obtain index from name
         wy = y + (iy * dy)
         draw.renderWire(w, ax, mvLookup, x, wy, x_scale, y_scale, color )

      return
      

