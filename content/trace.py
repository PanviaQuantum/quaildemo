##################################################################################################################
# trace.py
# Trace command buffer
###############################################
# Create a schema of types that can be used as store and search tags
schema={'key':str, 'sha2-800':list, 'vector':list, 'bvector':list, 'unsigned8bitvector':list, 'signed8bitvector':list, 'unsigned16bitvector':list, 'signed16bitvector':list, 'unicodevector':list, 'utf8vector':list, 'utf8x2vector':list }

# Create a list of Store command objects 
# make tag type one of schema
tag = 'key'  # eg. tag with 'key':'english number', content with dictionary X  
# tag = 'bvector'  # eg. tag with 'bvector':[boolean of ascii bytes of 'english number', content with dictionary X  
# tag = 'utf8vector'  # eg. tag with 'utf8vector':[ascii bytes of 'english number', content with dictionary X  

# Test data English numbers
mynums =['zero','one','two','three','four','five','six','seven','eight','nine','ten',\
'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen',\
'twenty','twenty-one','twenty-two','twenty-three','twenty-four','twenty-five','twenty-six',\
'twenty-seven','twenty-eight','twenty-nine','thirty','thirty-one','thirty-two','thirty-three',\
'thirty-four','thirty-five','thirty-six','thirty-seven','thirty-eight','thirty-nine','forty' ]

# test size
items = len(mynums)

# traceTag returns an object for Trace
# pass a type and an item of type
def traceTag(qtype,qdata):
 if qtype in schema:
  if type(qdata) == schema[qtype]:
   y={'tag':{qtype:qdata}}
   return y

# Trace takes a list traceTag objects and 
# returns a panvia object with 'command':'action':'Trace'
def Trace(item,total,*args):
 y={'panvia':{'command':{'action':'Trace','item':item,'total':total},'list':list(args)}}
 return y

#############################
# Trace english numbers state
# transformed from english
#############################
englishTrace = []
for i in range(items):
 qubitItem = traceTag(tag, mynums[i] )
 qubitState = Trace( i, items, qubitItem )
 englishTrace.append( qubitState )
