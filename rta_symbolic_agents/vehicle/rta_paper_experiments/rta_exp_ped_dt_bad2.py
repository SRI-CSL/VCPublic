import maude
import sys
sys.path.append('../../lib_py')
sys.path.append('../logicalScenarios/pedestrian-crossing')
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from datetime import date
from pedestrian_crossing_z3 import *

today = date.today().strftime("%Y-%m-%d")
printResults = "rta_exp_ped_dt_bad2-" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** Check Dur using Dt Bad Adequacy ***",file=f)
  maudeLoad = "../logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian-resilience.maude"
  maudeModule = 'SCENARIO-CROSSING'
  asys = "asysPedXLine(3,5/1,2/1,1/1,1/10)"
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  start = timer()
  results = checkDtBad(maudeLoad,maudeModule,asys)
  end = timer()
  delta = end - start 
  print("====> Total Time for Dt Bad Adequacy =" + str(delta),file=f)
  print(timedelta(seconds=delta), file=f)
  for res in results:
    print(str(res),file=f)
