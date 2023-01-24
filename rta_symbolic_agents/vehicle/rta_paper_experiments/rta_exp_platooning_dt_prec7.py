import maude
import sys
sys.path.append('../../lib_py')
sys.path.append('../logicalScenarios/platooning')
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from datetime import date
from platooning_z3 import *

today = date.today().strftime("%Y-%m-%d")
printResults = "rta_exp_platooning_dt_prec7-" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** Check Dur using Dt Bad Adequacy ***",file=f)
  maudeLoad = "../logicalScenarios/platooning/scenarios/following/load-platooning-manh.maude"
  maudeModule = 'SCENARIO-PLATOONING'
  asys = "asys(36,basicCond and testBounds0(6/2,4/2,2/1,1/10),2)"
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  start = timer()
  results = checkDtPrec1(maudeLoad,maudeModule,asys,f)
  end = timer()
  delta = end - start 
  print("====> Total Time for Dt Prec1 Adequacy =" + str(delta),file=f)
  print(timedelta(seconds=delta), file=f)
  for res in results:
    print(str(res),file=f)