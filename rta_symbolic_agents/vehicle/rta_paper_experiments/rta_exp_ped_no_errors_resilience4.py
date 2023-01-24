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
printResults = "rta_exp_ped_no_errors_resilience4-" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** Resilience Check ***",file=f)
  maudeLoad = "../logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian-resilience.maude"
  maudeModule = 'SCENARIO-CROSSING'
  asys = "asysPedXLine(3,3/1,2/1,1/1,1/10)"
  t = 6
  safer = 3
  safe = 2 
  bad = 1
  maxdec1 = -8
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  print("  time = " + str(t),file=f)
  print("  maxdec1 = " + str(maxdec1),file=f)
  start = timer()
  result = isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)
  end = timer()
  delta = end - start 
  print("====> Total Time for Resilience =" + str(delta),file=f)
  print(timedelta(seconds=delta), file=f)
  if result == True:
    print("System is resilient",file=f)
  elif result[0] == "afterTicks":
    print("System reaches a bad state within " + str(t) + " ticks",file=f)
    print(result[1],file=f)
  elif result[0] == "checkImGrSPDT":
    print("System reaches does not safer within " + str(t) + " ticks",file=f)
    print(result[1],file=f)





    