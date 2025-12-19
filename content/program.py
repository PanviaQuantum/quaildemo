# program.py
# contains command buffers and methods to load, step and vizualize
# vizualize generates html and svg files for circuit and state
#
from timeslice import timeslice

class program:
   # Constructor accepts a list of commands or list of lists of commands plus screen pixels
   def __init__(self,commands=[],width=800,height=500):
      self.future = commands
      self.history = []
      self.pc = 0
      self.globals = { 'width':width, 'height':height, 'timeslices': 0, 'multiverses': [], 'qubits': 0, 'connection': 0, 'multiverseIndex': {}, 'width': 20, 'height': 20, 'border': 30, 'numPanes': 1, 'paneDim': 10, 'multiverseDim': 1 }
      self.circuits = None   # list of timeslices 
      self.qubits = None     # dict of tag : position
   # load accepts a list of commands or list of lists of commands and updates globals

   def load(self,commands):
      self.future.append( commands )
      self.update()

   def preparse(self,commands):
      action = commands[0]['panvia']['command']['action']
      total = commands[0]['panvia']['command']['total']
      return action, total

   # update processes lists of commands and updates globals
   def update(self):
      self.globals['timeslices'] = len(self.future) + len(self.history)
      tcon = self.findConnection()     # locate multiverses
      print(tcon)
      if tcon != None:
         # Initialized self.globals.qubits and multiverses
         qubnet = self.propagate(tcon)
      else:
         qubnet = self.propagate(0)
      self.circuits = qubnet
      # Program represented as ordered timeslice instances in self.circuits

   def propagate(self,start):
      lastslot = None
      before = []
      if start > 0:
         # propagate backwards from start
         nextslot = None
         for i in range(start,-1,-1):
            k = i - len(self.history) 
            if k >= 0:
               tslice = self.future[k]
            else:
               tslice = self.history[i]
            slot = timeslice(i)        # create new timeslice
            slot.organize( tslice, nextslot, -1 )    # input commands and last iter's slot
            before.insert(0,slot)  # prepend timeslice
            nextslot = slot
         lastslot = before[start]
         start += 1   # processed start slot so advance
      # propagate forwards from start
      after = []
      for i in range(start, self.globals['timeslices']):
         k = i - len(self.history) 
         if k >= 0:
            tslice = self.future[k]
         else:
            tslice = self.history[i]
         slot = timeslice(i)        # create new timeslice
         slot.organize( tslice, lastslot, 1 )    # input commands and last iter's slot
         after.append(slot)  # append timeslice
         lastslot = slot

      sequence = before + after

      return sequence

   # findConnection sets self.globals.connection to the timeslice index of Connect
   def findConnection(self):
      t = 0
      self.globals['connection'] = 0
      self.globals['multiverses'] = []
      for seq in self.future:
         action = seq[0]['panvia']['command']['action']
         total = seq[0]['panvia']['command']['total']
         qubits = 0
         if action == 'Connect' or action == 'Teleport':
            # record 'connection' seed slice
            self.globals['connection'] = t + len(self.history)

            # count qubits to partition layout to panes
            for g in seq:
               qubits += len( g['panvia']['list'] )

            self.globals['qubits'] = qubits

            multiverseDim = int(qubits / total)    # qubits per multiverse 
            self.globals['multiverseDim'] = multiverseDim

            paneDim = self.globals['paneDim']   # 10 multiverses per pane

            nPanes = int( total / paneDim )
            self.globals['numPanes'] = nPanes

            # Proportion screen layout
            # panewidth set from circuits width
            nslices = self.globals['timeslices']

            width = self.globals['width']
            height = self.globals['height']
            border_x = self.globals['border']
            border_y = self.globals['border']

            paneWidth = (border_x * 2) + (nslices * width)
            paneHeight = (border_y * 2) + (paneDim * multiverseDim * height)
            paneHeight = paneHeight + (paneDim * 15)

            for g in seq:
               cohort = []
               m = g['panvia']['command']['item']
               xpane = ((int( m / paneDim )) % 2) * paneWidth
               ypane = (int( m / (2 * paneDim ))) * paneHeight
               v = m % paneDim              # v is mv index in pane

               h = g['panvia']['list']
               for x in h:
                  q = x['tag']['key']
                  cohort.append( q )
                  self.globals['multiverseIndex'][ q ] = (m,v,(xpane,ypane))   # lookup mv + pane by tag
               self.globals['multiverses'].append(cohort)

            # Done globals initialization for pane layout 
            return t    # index of Connect timeslice

         t += 1
      return None   # no index for Connect timeslice

   ################################################################################
   # diagram plots the future and history to a svg file
   def diagram(self,ax):
      self.update()
      # Program represented as ordered timeslice instances in self.circuits
      # self.globals has geometry parameters height, width, timeslices, qubits
      # self.circuit has local parameters for each timeslice
      #
      # Layout Grid of Tiles each 10 high 10 wide
      width = self.globals['width']
      height = self.globals['height']
      border_x = self.globals['border']
      border_y = self.globals['border']
      x_scale = 1.0
      y_scale = 1.0
      color = 'black'
      fill = 'grey'

      x = border_x
      # Draw from top left corner, pass -height to descend
      y = border_y
      
      # Pass in multiverseIndex for mv lookup by qubit name
      mvLookup = self.globals['multiverseIndex']
      paneDim = self.globals['paneDim']
      multiverseDim = self.globals['multiverseDim']
      paneDim *= multiverseDim

      for slot in self.circuits:
         slot.render( ax, mvLookup, x, y, width, -height, paneDim, x_scale, y_scale, color, fill )
         x += width
      # draw key
           
      return

   def execute(self,commands):
      action, total = preparse(commands)

      # for x in commands:
            

   def step(self,steps=1):
      for t in range(steps):
         items = self.future.pop(0)
         self.globals['connection'] -= 1
         execute( items )
         self.history.append(items)

