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
printResults = "rta_exp_ped_dt_noskip_spd-notres" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** No skip property ***",file=f)
  maudeLoad = "../logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian.maude"
  maudeModule = 'SCENARIO-CROSSING'
  asys = "asysPedXLineSpd(3,2/1,3/1,2/1,1/1,1/10)"
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