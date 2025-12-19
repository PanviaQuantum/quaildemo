##################################################################################################################
# execute.py
# Send command to Panvia Quantum Computer server
##################################################################################################################
import json
import http.client
from pprint import pprint

# panviaServer is the IP address of PanviaQuantumWebStore
panviaServer='70.234.218.42'
headers = {'content-type':'application/json'}

# Connect to PanviaQuantumWebStore with ip address
# Send python list or JSON text string to PanviaQuantumWebStore
# Read and Convert JSON response to python by first converting bytearray to str
# then str to python using json.loads(str)
def execute( commands, ip ):
 if type(ip) == str:
  webcon = http.client.HTTPConnection(ip)
  webcon.connect()
  if type(commands) == list:
   JSON = json.dumps(commands, indent=4 )
   webcon.request('POST','/PanviaWebAI', JSON, headers )
   myresp = webcon.getresponse()
   respdat = myresp.read()
   print(respdat)
   JSON = str(respdat,'latin-1')
   pprint(JSON)
   y = json.loads(JSON) 
   return y
  else:
   print('python list required')
