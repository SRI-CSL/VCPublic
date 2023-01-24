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
printResults = "rta_exp_platooning_rss_noerrors_resilience-" + today + ".txt" 

with open(printResults,'w') as f:
  print("**** Resilience Check ***",file=f)
  maudeLoad = "../logicalScenarios/platooning/scenarios/following_RSS/load-platooning-manh.maude"
  maudeModule = 'SCENARIO-PLATOONING'
  asys = "asys(36,basicCond(5/1,40/1) and testBounds3(6/1,4/1,1/1,1/10),2)"
  t = 2
  safer = 3
  safe = 2 
  bad = 1
  maxdec1 = -8
  print("Maude Experiment:\n  " + maudeLoad + "\n  " + maudeModule + "\n  " + asys,file=f)
  print("  time = " + str(t),file=f)
  print("  maxdec1 = " + str(maxdec1),file=f)
  start = timer()
  result = isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad)
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