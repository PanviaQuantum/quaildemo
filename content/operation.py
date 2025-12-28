##################################################################################################################
# operations.py 
# Quantum Auto Inference Language
# Python class for Graphical User Interface to QUAIL contains:
#  1) qubit dict filled by tags in Store Commands - this starts the circuit representation
#         shared reference by timeslices
#          each timeslice contains an operation with nodes referenced by tags
#  2) Program = List of Command Lists, PC = index to current frame displayed in Map screen
#  3) Circuit class representation filled from Program Command List parsing
#  4) Map Renderer processes Circuit to Action named blocks left to right, highlighting the PC current timeslice
#  5) Circuit Renderer processes Circuit to iframe of HTML timeslices left to right,
#       upscaling x width of PC current timeslice 
#  6) State Renderer processes Trace JSON to HTML iframe
#  7) Screen Manager contains render parameters and coordinates with methods to determine from components
#     Proportioning of rendering parameters from component data
##################################################################################################################

# store a dependent passed qubit and phase
class qStore:
   def __init__(self,operation,dependent,phase):
      self.operation=operation
      self.dependent=dependent
      self.phase=phase

# gate a dependent passed qubit
class qNode:
   def __init__(self,operation,dependent):
      self.operation=operation
      self.dependent=dependent

# operation a dependent passed qubit and one or more independents
class qNodes:
   def __init__(self,operation,dependent,independent):
      self.operation=operation
      self.dependent=dependent
      self.independent=independent

# connect a list of passed qubits
class qConnect:
   def __init__(self,operation,qubits,index):
      self.operation=operation
      self.dependent=qubits
      self.index=index

# connect a list of passed qubits
class qCollapse:
   def __init__(self,operation,qubits,observe,index):
      self.operation=operation
      self.dependent=qubits
      self.observe=observe
      self.index=index


# Single C^2 qubit gate operation and multi qubit as dependent,and independent
# quantumAction lookup node type by command action, validating with return class for custom cases
quantumAction = { 'Store': qStore, 'Trace': qNode, 'Search': qNode, 'Delete': qNode, 'L-Gate': qNode, 'R-Gate': qNode, 'S-Gate': qNode, 'T-Gate': qNode, 'H-Gate': qNode, 'CNOT': qNodes, 'CROT': qNodes, 'Collapse': qCollapse, 'Connect': qConnect, 'Teleport': qConnect }

qNodesAction = { 'CNOT': 2, 'CROT': 2 } 

qConnectAction = { 'Connect': 3, 'Teleport': 4, 'Collapse': 5 }

# class operation uses dictionaries to parse commands to 3 types
# (1) qNode  (2) qNodes  (3) qConnect  and returns int code 1,2,3
class operation:
   def __init__(self):
      self.node = None

   def parse(self,commands):
      # print(commands)
      action = commands['panvia']['command']['action']
      total = commands['panvia']['command']['total']
      if action in quantumAction:
         g = commands['panvia']['list']
         if action in qNodesAction:
            self.node = quantumAction[action](action, g[0]['dependent']['tag']['key'], g[0]['independent']['tag']['key'])
            return 2  # two qubit node2
         elif action in qConnectAction:
            if action == 'Connect' or action == 'Teleport':
               self.node = quantumAction[action](action, commands['panvia']['list'], commands['panvia']['command']['item'] )
            elif action == 'Collapse':
               # extract observe True/False on each qubit for Collapse function
               observe = [ q['qubit']['observe'] for q in g ]
               print(observe)
               self.node = quantumAction[action](action, commands['panvia']['list'], observe, commands['panvia']['command']['item'] )
            else:
               assert False
            return 3   # multi qubit 
         elif action == 'Store':
            if 'qubit' in g[0]:
               phase = g[0]['qubit']['phase']
            else:
               phase = 0.0
            self.node = quantumAction[action](action, g[0]['tag']['key'], phase)
            return 1   # single qubit node1
         else:
            print(action)
            if action[1:6] == '-Gate':
               abbrev = action[0] + '-g'
               self.node = quantumAction[action](abbrev, g[0]['tag']['key'])
            else:   
               self.node = quantumAction[action](action, g[0]['tag']['key'])
            return 1   # single qubit node1

# end of operation.py
