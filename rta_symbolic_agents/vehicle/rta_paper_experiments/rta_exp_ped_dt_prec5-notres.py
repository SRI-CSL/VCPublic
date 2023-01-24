import maude
import sys
sys.path.append('../../lib_py')
sys.path.append('../logicalScenarios/pedestrian-crossing')
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from datetime import date
from pedestrian_crossing_z3 import *

# Did not terminate...

today = date.today().strftime("%Y-%m-%d")
printResults = "rta_exp_ped_dt_prec5-notres" + today + ".txt" 

with open(printResults,'w') as f:
  print("\n\n**** Check Dur using Prec1 Adequacy ***",file=f)
  maudeLoad = "../logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian.maude"
  maudeModule = 'SCENARIO-CROSSING'
  asys = "asysPedXLineDist(3,6/1,4/1,2/1,19/1,1/10)"
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  start = timer()
  results = checkDtPrec1(maudeLoad,maudeModule,asys,f)
  end = timer()
  delta = end - start 
  print("====> Total Time for Prec1 Adequacy =" + str(delta),file=f)
  print(timedelta(seconds=delta), file=f)
  for res in results:
    print(str(res),file=f)