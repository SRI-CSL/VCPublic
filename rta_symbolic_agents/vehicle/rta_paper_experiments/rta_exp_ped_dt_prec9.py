import maude
import sys
sys.path.append('../../lib_py')
sys.path.append('../logicalScenarios/pedestrian-crossing')
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from datetime import date
from pedestrian_crossing_z3 import *

# did not terminate

today = date.today().strftime("%Y-%m-%d")
printResults = "rta_exp_ped_dt_prec9-" + today + ".txt" 

with open(printResults,'w') as f:
  print("\n\n**** Check Dur using Prec1 Adequacy ***",file=f)
  maudeLoad = "../logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian.maude"
  maudeModule = 'SCENARIO-CROSSING'
  asys = "asysPedXLine(3,4/1,2/1,1/1,1/10)"
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  start = timer()
  # checkDtPrec1OneLog(maudeLoad,maudeModule,"saferSP","safeSP",6,4,2,asys,f)
  checkDtPrec1OneLog(maudeLoad,maudeModule,"safeSP","saferSP",6,4,2,asys,f)

  end = timer()
  delta = end - start 
  print("====> Total Time for Prec1 Adequacy =" + str(delta),file=f)
  print(timedelta(seconds=delta), file=f)
