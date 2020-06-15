
from .models import PeptideSeq
import pandas as pd
import os

"""
def QurJson(a):

   Ps = PeptideSeq.objects.filter(Accession=a)
   df = pd.DataFrame(list(Ps.values()))
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   print (os.path.join(BASE_DIR,'DataBase','static','data','data1.json'))
   print(df)
"""

def QurJson(a=None,p=None):
   seq = []
   starts_sides = []
   end_sides = []
   lenght = []

   if p==None:

      Ps = PeptideSeq.objects.filter(Accession=a)

      for C in Ps:

         seq.append(C.Input_Sequence)
         starts_sides.append(C.P1_Position)
         end_sides.append(int(C.P1_Position)+(len(C.Input_Sequence)-1))
         lenght.append(len(C.Input_Sequence))

      clms = ['seq',           
        'starts_sides', 
        'end_sides', 
        'lenght',]

      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      Out_json_data = os.path.join(BASE_DIR,'DataBase','static','data','data.json')

      df = pd.DataFrame(list(zip(seq,starts_sides,end_sides,lenght)),columns=clms)
      df.to_json(Out_json_data, orient='split')

   elif a == None:

      Ps = PeptideSeq.objects.filter(Input_Sequence=p)

      for C in Ps:

         seq.append(C.Input_Sequence)
         starts_sides.append(C.P1_Position)
         end_sides.append(int(C.P1_Position)+(len(C.Input_Sequence)-1))
         lenght.append(len(C.Input_Sequence))

      clms = ['seq',           
        'starts_sides', 
        'end_sides', 
        'lenght',]

      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      Out_json_data = os.path.join(BASE_DIR,'DataBase','static','data','data.json')

      df = pd.DataFrame(list(zip(seq,starts_sides,end_sides,lenght)),columns=clms)
      df.to_json(Out_json_data, orient='split')

   else:
      Ps = PeptideSeq.objects.filter(Input_Sequence=p, Accession=a)

      for C in Ps:

         seq.append(C.Input_Sequence)
         starts_sides.append(C.P1_Position)
         end_sides.append(int(C.P1_Position)+(len(C.Input_Sequence)-1))
         lenght.append(len(C.Input_Sequence))

      clms = ['seq',           
        'starts_sides', 
        'end_sides', 
        'lenght',]

      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      Out_json_data = os.path.join(BASE_DIR,'DataBase','static','data','data.json')

      df = pd.DataFrame(list(zip(seq,starts_sides,end_sides,lenght)),columns=clms)
      df.to_json(Out_json_data, orient='split')





