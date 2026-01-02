from ipykernel.com import Comm
from IPython.display import Javascript, display

my_comm = Comm(target_name='my_comm_target', data={'foo': 1 })

@my_comm.on_msg
def _recv(msg):
  data = msg['content']['data']
  print(f"Kernel received: {data}")
  my_comm.send({'echo': f"Kernel echoes: {data['message']}"})
