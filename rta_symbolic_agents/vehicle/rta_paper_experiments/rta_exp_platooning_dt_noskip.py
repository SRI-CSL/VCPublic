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
printResults = "rta_exp_platooning_dt_noskip-" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** Check Dur using Dt Bad Adequacy ***",file=f)
  maudeLoad = "../logicalScenarios/platooning/scenarios/following/load-platooning-manh.maude"
  maudeModule = 'SCENARIO-PLATOONING'
  asys = "asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)"
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  start = timer()
  sp1 = "saferSP"
  sp2 = "unsafeSP"
  results = checkNoSkipProperty(maudeLoad,maudeModule,asys,sp1,sp2)
  print(results)
  end = timer()
  delta = end - start 
  print("====> Total Time for no skip =" + str(delta),file=f)
  print("Result " + str(results),file=f)
  print(timedelta(seconds=delta), file=f)
