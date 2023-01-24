import maude
import sys
sys.path.append('../../../lib_py')
from maude_z3 import SMT_CHECK
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from basic_lib import * 

def checkProperties(data,safer,safe,bad,maxdec1):
  posX = data[0]
  posY = data[1]
  spd = data[2]
  acc = data[3]
  saferL = []
  safeL = []
  badL = []
  distTar = []
  numTicks = len(posX["v(1)"])
  for t in range(numTicks):
    posV1 = posY["v(1)"][t]
    posV2 = posY["v(2)"][t]
    vel = spd["v(1)"][t]
    distTar.append(posV2 - posV1)
    dstop = - (vel * vel) / (2 * maxdec1)
    saferL.append(dstop + (safer * (vel / 2/1)))
    safeL.append(dstop + (safe * (vel / 2/1)))
    badL.append(dstop + (bad * (vel / 2/1)))
  print("distTar --> ", distTar)
  print("Safer --> ", saferL)
  print("Safe --> ", safeL)
  print("Bad --> ", badL)
  return [distTar,saferL,safeL,badL]

def checkDtBad(maudeLoad,maudeModule,asys):
  start = timer()
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asys = str(asys) 
  # print("=====> Start Time =", start)
  dt = m.parseTerm("getTickSize(" + asys + ")")
  dt.reduce()
  spset = m.parseTerm("spset")
  spset.reduce()
  sps = str(spset).split(" ")
  results = []
  for sp in sps:
    relSP = m.parseTerm(sp + " getRelSP(" + sp + ",none)")
    relSP.reduce()
    spsRel = str(relSP).split(" ")
    for sp1 in spsRel:
      print("Checking case:" + sp + " -> " + sp1)
      check = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(" + sp + "," + sp1 + "," + asys + "," + str(dt) + ")")
      check.reduce()
      results.append([sp,sp1,str(check)])
      print(check)
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time for CheckDur =", end - start)
  print(timedelta(seconds=end-start))
  return results

def checkDtPrec1(maudeLoad,maudeModule,asys,file):
  start = timer()
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys) 
  # print("=====> Start Time =", start)
  dt = m.parseTerm("getTickSize(" + asys + ")")
  dt.reduce()
  spset = m.parseTerm("spset")
  spset.reduce()
  sps = str(spset).split(" ")
  results = []
  for sp in sps:
    relSP = m.parseTerm(sp + " getRelSP(" + sp + ",none)")
    relSP.reduce()
    spsRel = str(relSP).split(" ")
    for sp1 in spsRel:
      print("Checking case:" + sp + " -> " + sp1)
      check = m.parseTerm("checkDTPrec1SPtoSP1(" + sp + "," + sp1 + "," + asys + "," + str(dt) + ")")
      check.reduce()
      # print(check)
      if str(check) == "(none).CheckDurResult":
        results.append([sp,sp1,"true"])
        print("OK")
      else: 
        results.append([sp,sp1,"false"])
        print("Not OK")
      # print(str([sp,sp1,str(check)]),file=file)
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time for CheckDur =", end - start)
  print(timedelta(seconds=end-start))
  return results

def checkNoSkipProperty(maudeLoad,maudeModule,asys,sp1,sp2):
  start = timer()
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys)
  sp1 = str(sp1)
  sp2 = str(sp2)
  dt = m.parseTerm("getTickSize(" + asys + ")")
  dt.reduce()
  check = m.parseTerm("checkNoSkipProperty(" + sp1 + "," + sp2 + "," + asys + "," + str(dt) + ")")
  check.reduce()
  return check

def checkDtPrec1Log(maudeLoad,maudeModule,safer,safe,bad,asys,file):
  start = timer()
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys) 
  # print("=====> Start Time =", start)
  dt = m.parseTerm("getTickSize(" + asys + ")")
  dt.reduce()
  spset = m.parseTerm("spset")
  spset.reduce()
  sps = str(spset).split(" ")
  results = []
  for sp in sps:
    relSP = m.parseTerm(sp + " getRelSP(" + sp + ",none)")
    relSP.reduce()
    spsRel = str(relSP).split(" ")
    for sp1 in spsRel:
      print("Checking case:" + sp + " -> " + sp1)
      check = m.parseTerm("checkDTPrec1SPtoSP1(" + sp + "," + sp1 + "," + asys + "," + str(dt) + ")")
      check.reduce()
      print(check)
      if str(check) == "(none).CheckDurResult":
        results.append([sp,sp1,"true"])
        print("OK")
      else: 
        spNotMaude = m.parseTerm("getSPNot(" + str(check) + ")")
        spNot = spNotMaude.reduce()
        asysNotMaude = m.parseTerm("getAsysNot(" + str(check) + ")")
        asysNot = asysNotMaude.reduce()
        print(asysNot)
        data = printLog(m,maude_z3.smt_model,str(asysNot),["v(1)","v(2)"])
        data2 = checkProperties(data,safer,safe,bad,maxdec1)
        print(data2)
        print(str([sp,sp1,spNot,str(data2)]),file=file)
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time for CheckDur =", end - start)
  print(timedelta(seconds=end-start))
  return results

def checkDtPrec1OneLog(maudeLoad,maudeModule,sp,sp1,safer,safe,bad,asys,file):
  start = timer()
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys) 
  # print("=====> Start Time =", start)
  dt = m.parseTerm("getTickSize(" + asys + ")")
  dt.reduce()
  print("Checking case:" + sp + " -> " + sp1)
  check = m.parseTerm("checkDTPrec1SPtoSP1(" + sp + "," + sp1 + "," + asys + "," + str(dt) + ")")
  check.reduce()
  results = []
  # print(check)
  if str(check) == "(none).CheckDurResult":
    results.append([sp,sp1,"true"])
    print("OK")
  else: 
    print("DT Prec Adequacy not satisfied")
    spNot = m.parseTerm("getSPNot(" + str(check) + ")")
    spNot.reduce()
    asysNot = m.parseTerm("getAsysNot(" + str(check) + ")")
    asysNot.reduce()
    # dataInit = printLog(m,maude_z3.smt_model,str(asys),["v(1)","v(2)"])
    # dataInit2 = checkProperties(dataInit,safer,safe,bad,-8)
    dataNot = printLog(m,maude_z3.smt_model,str(asysNot),["v(1)","v(2)"])
    dataNot2 = checkProperties(dataNot,safer,safe,bad,-8)
    # print(dataInit2,dataNot2)
    print(str([sp,sp1,spNot,dataNot2]),file=file)

def isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1):
  start = timer()
  # print("=====> Start Time =", start)
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys)
  resultResilience = isResilientDT(m,"['" + maudeModule + "]",asysStr,"(" + str(t) + ").NzNat","safeSP","badSP","saferSP")
  # print(resultResilience)
  if resultResilience == []:
    print("System is resilient")
    return True
    # Print to file
  elif resultResilience[0] == "afterTicks":
    badAsys = resultResilience[1]
    res = m.parseTerm("not alwaysSP(saferSP," + str(badAsys) + ")")
    res.reduce()
    data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
    print("Error ->",getAsg(m,maude_z3.smt_model,"vv(35,\"error-pedS\")"))
    data2 = checkProperties(data,safer,safe,bad,maxdec1)
    # Print to file
    return ["afterTicks",data2]
  elif resultResilience[0] == "checkImGrSPDT":
    badAsys = resultResilience[1]
    res = m.parseTerm("checkSP(unsafeSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad,maxdec1) 
    res = m.parseTerm("checkSP(badSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad,maxdec1)
    # print to file
    return ["checkImGrSPDT",data2]
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time =", end - start)
  print(timedelta(seconds=end-start))


def runExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1):
  start = timer()
  # print("=====> Start Time =", start)
  maude.init()
  maude.load(maudeLoad)
  hook = SMT_CHECK()
  maude.connectEqHook('smtCheck',hook)
  m = maude.getModule(str(maudeModule))
  asysStr = str(asys)
  print("Checking the correctness of DT")
  resultsCheckTimeDur = checkTimeDur(m,asysStr)
  # for results in resultsCheckTimeDur:
      # print in file the results
      # return False
  resultResilience = isResilientDT(m,"['" + maudeModule + "]",asysStr,"(" + str(t) + ").NzNat","safeSP","badSP","saferSP")
  print(resultResilience)
  if resultResilience == []:
    print("System is resilient")
    # Print to file
  elif resultResilience[0] == "afterTicks":
    badAsys = resultResilience[1]
    res = m.parseTerm("not alwaysSP(saferSP," + str(badAsys) + ")")
    res.reduce()
    data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
    data2 = checkProperties(data,safer,safe,bad,maxdec1)
    # Print to file
  elif resultResilience[0] == "checkImGrSPDT":
    badAsys = resultResilience[1]
    res = m.parseTerm("checkSP(unsafeSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad,maxdec1) 
    res = m.parseTerm("checkSP(badSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad,maxdec1)
    # print to file
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time =", end - start)
  print(timedelta(seconds=end-start))

# Scenario without errors on the pedestrian sensros
# maudeLoad = "scenarios/noSensorErrors/load-pedestrian.maude"
# maudeModule = 'SCENARIO-CROSSING'
# asys = "asysPedXLine(3,3/1,2/1,1/1,1/10)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# maxdec1 = -8 
# runExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)

# maudeLoad = "scenarios/noSensorErrors/load-pedestrian.maude"
# maudeModule = 'SCENARIO-CROSSING'
# asys = "asysPedXLine(3,3/1,2/1,1/1,1/10)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# maxdec1 = -8 
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)


# Scenario with errors on the pedestrian sensros
# maudeLoad = "scenarios/errorPedS/load-pedestrian-error-pedS.maude"
# maudeModule = 'SCENARIO-CROSSING'
# asys = "asysPedXLineErrorPedS(3,3/1,2/1,1/1,1/10,1/10)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# maxdec1 = -8 
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)
# System is resilient
# # ====> Total Time = 283.143617746
# # 0:04:43.143618


# # Scenario with errors on the pedestrian sensros
# maudeLoad = "scenarios/errorPedS/load-pedestrian-error-pedS.maude"
# maudeModule = 'SCENARIO-CROSSING'
# asys = "asysPedXLineErrorPedS(3,3/1,2/1,1/1,1/10,1/2)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# maxdec1 = -8 
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)
# 0:00:57.703121
# PosX--> {'v(1)': [5.0, 5.0, 5.0, 5.0, 5.0, 5.0], 'v(2)': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]}
# PosY--> {'v(1)': [1.9375, 2.0775, 2.1774999999999998, 2.2775, 2.3775, 2.4775], 'v(2)': [4.0, 4.0, 4.0, 4.0, 4.0, 4.0]}
# Spd--> {'v(1)': [1.7999999999999998, 1.0, 1.0, 1.0, 1.0, 1.0], 'v(2)': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}
# Acc--> {'v(1)': [-7.0, -8.0, 0.0, 0.0, 0.0, 0.0], 'v(2)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
# Sen--> {'v(1)': [['"None"', '"-1/1"', -1.0], ['"ag2"', '"4"', 4.0], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5]], 'v(2)': [['"None"', '"-1/1"', -1.0], ['"ag2"', '"4"', 4.0], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5], ['"ag2"', '"9/2"', 4.5]]}
# 1/2
# Error -> 0.5
# distTar -->  [2.0625, 1.9224999999999999, 1.8225000000000002, 1.7225000000000001, 1.6225, 1.5225]
# Safer -->  [2.9025, 1.5625, 1.5625, 1.5625, 1.5625, 1.5625]
# Safe -->  [2.0025, 1.0625, 1.0625, 1.0625, 1.0625, 1.0625]
# Bad -->  [1.1024999999999998, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625]

# Experiments with timestep simple

# vlb = 5/1 instead of 1/2
# maudeLoad = "scenarios/errorPedS/load-pedestrian-error-pedS-timestepSimple.maude"
# maudeModule = 'SCENARIO-CROSSING'
# asys = "asysPedXLineErrorPedS(3,3/1,2/1,1/1,1/10,1/10)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# maxdec1 = -8 
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad,maxdec1)
# System is resilient
# ====> Total Time = 2284.998150143
# 0:38:04.998150

# Example on how to rewrite an asys
# maude.init()
# maude.load(maudeLoad)
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule(str(maudeModule))
# asysM = m.parseTerm("enforceSP(safeSP," + asys + ")")
# asysM.reduce()
# asysM.rewrite(6)
# print(asysM)



  



