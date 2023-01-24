import sys
sys.path.append('../../../lib_py')
import maude
from maude_z3 import *
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
from basic_lib import * 

def checkProperties(data,safer,safe,bad):
  posX = data[0]
  posY = data[1]
  spd = data[2]
  acc = data[3]
  saferL = []
  safeL = []
  badL = []
  distTar = []
  vminD = []
  numTicks = len(posX["v(0)"])
  for t in range(numTicks):
    posV0 = posY["v(0)"][t]
    posV1 = posY["v(1)"][t]
    v0 = spd["v(0)"][t]
    v1 = spd["v(1)"][t]
    distTar.append(posV0 - posV1)
    saferL.append((v1 * (safer + 1)) - v0)
    safeL.append((v1 * (safe + 1)) - v0)
    badL.append((v1 * (bad + 1)) - v0)
    vminD.append(((posV0 - posV1 + v0) / (safer + 1)) - 1)
  print("vminD --> ", vminD)
  print("dist --> ", distTar)
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

def isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad):
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
    data = printLog(m,resultResilience[2],str(badAsys),["v(0)","v(1)"])
    # data = printLog(m,maude_z3.smt_model,str(badAsys),["v(0)","v(1)"])
    data2 = checkProperties(data,safer,safe,bad)
    return ["afterTicks",data2]
    # Print to file
  elif resultResilience[0] == "checkImGrSPDT":
    badAsys = resultResilience[1]
    res = m.parseTerm("checkSP(unsafeSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad) 
    res = m.parseTerm("checkSP(badSP," + str(badAsys) + ")")
    res.reduce()
    if res == "(true).Bool":
      data = printLog(m,maude_z3.smt_model,str(badAsys),["v(1)","v(2)"])
      data2 = checkProperties(data,safer,safe,bad)
    return ["checkImGrSPDT",data2]
    # print to file
  end = timer()
  # print("====> End Time =", end)
  print("====> Total Time =", end - start)
  print(timedelta(seconds=end-start))
  


# maudeLoad = "scenarios/following/load-platooning-manh.maude"
# maudeModule = 'SCENARIO-PLATOONING'
# asys = "asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)"
# t = 4
# safer = 3
# safe = 2 
# bad = 1
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad)
# PosX--> {'v(0)': [0.0, 0.0, 0.0, 0.0, 0.0], 'v(1)': [0.0, 0.0, 0.0, 0.0, 0.0]}
# PosY--> {'v(0)': [12.0, 12.3490625, 12.6934375, 13.0296875, 13.356582031250001], 'v(1)': [1.5, 1.885, 2.241455078125, 2.5841259765625, 2.9259672851562497]}
# Spd--> {'v(0)': [3.5, 3.4812500000000024, 3.406250000000002, 3.3187500000000023, 3.2191406250000023], 'v(1)': [4.0, 3.7, 3.4291015625, 3.4243164062500004, 3.4125097656250003]}
# Acc--> {'v(0)': [0.0, -0.18749999999997644, -0.75, -0.875, -0.99609375], 'v(1)': [-7.0, -3.0, -2.708984375, -0.04785156249999769, -0.11806640624999791]}
# Sen--> {'v(0)': [['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0]], 'v(1)': [['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0]]}
# vminD -->  [2.5, 2.486328125000001, 2.4645581054687504, 2.4410778808593756, 2.4124388427734385]
# dist -->  [10.5, 10.4640625, 10.451982421875, 10.4455615234375, 10.430614746093752]
# Safer -->  [12.5, 11.318749999999998, 10.310156249999999, 10.378515624999999, 10.430898437499998]
# Safe -->  [8.5, 7.618749999999999, 6.881054687499999, 6.9541992187499995, 7.018388671874999]
# Bad -->  [4.5, 3.918749999999998, 3.451953124999998, 3.5298828124999986, 3.6058789062499983]
# ====> Total Time = 136.488987767
# 0:02:16.488988

# maudeLoad = "scenarios/following/load-platooning-manh.maude"
# maudeModule = 'SCENARIO-PLATOONING'
# asys = "asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)"
# t = 5
# safer = 3
# safe = 2 
# bad = 1
# isResilientDTExperiment(maudeLoad,maudeModule,asys,t,safer,safe,bad)

# PosX--> {'v(0)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'v(1)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
# PosY--> {'v(0)': [11.0, 11.245, 11.48, 11.705, 11.923579521054688, 12.135738563164061], 'v(1)': [1.0, 1.7974999999999999, 2.58886875, 3.371447203125, 4.1423295210546875, 4.898910614183594]}
# Spd--> {'v(0)': [2.5, 2.4, 2.3, 2.2, 2.171590421093746, 2.0715904210937457], 'v(1)': [8.0, 7.95, 7.877375, 7.7741940625, 7.64345229609375, 7.488169566484375]}
# Acc--> {'v(0)': [-1.0, -1.0, -1.0, -1.0, -0.2840957890625444, -1.0], 'v(1)': [-1.0, -0.5, -0.72625, -1.031809375, -1.3074176640625, -1.55282729609375]}
# Sen--> {'v(0)': [['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0]], 'v(1)': [['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0], ['"None"', '"-1/1"', -1.0]]}
# vminD -->  [7.5, 7.123749999999999, 6.745565625, 6.3667763984375005, 6.062215421093746, 5.69000439558398]
# dist -->  [10.0, 9.4475, 8.89113125, 8.333552796875, 7.78125, 7.236827948980467]
# Safer -->  [11.0, 11.100000000000001, 11.15475, 11.148388125, 10.943723750000009, 10.83315829078126]
# Safe -->  [5.5, 5.550000000000001, 5.577375, 5.5741940625, 5.4718618750000045, 5.41657914539063]
# Bad -->  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# ====> Total Time = 391.958468074
# 0:06:31.958468


# maude.init()
# maude.load("scenarios/following/load-platooning-manh.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)")
# asys.reduce()
# asys.rewrite(3)
# data = printLog(m,maude_z3.smt_model,str(asys),["v(0)","v(1)"])
# checkProperties(data,3,2,1)


# asys = m.parseTerm("enforceSP(safeSP,asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2))")
# asys.reduce()
# print(asys)
# asys.rewrite(3)
# data = printLog(m,maude_z3.smt_model,str(asys),["v(0)","v(1)"])
# checkProperties(data,3,2,1)





# maude.init()
# maude.load("scenarios/following/load-platooning-manh.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)")
# asys.reduce()
# asys.rewrite(3)
# data = printLog(m,maude_z3.smt_model,str(asys),["v(0)","v(1)"])
# checkProperties(data,3,2,1)


















# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP.maude")
# maude.load("vehicle/examples/platooning/load-platooning-4SP.maude")
# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP-timesteps.maude")
# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP-timesteps-split.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')

############ CHECK DUR TESTS
# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)")
# asys.reduce()

# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/20),2)")
# asys.reduce()

# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/40),2)")
# asys.reduce()

# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/100),2)")
# asys.reduce()

# ====> End Time = 38.198704663
# ====> Total Time = 37.790693429
# 0:00:37.790693
# asys = m.parseTerm("asys(36,basicCond and testBounds0(5/1,3/1,1/1,1/10),2)")
# asys.reduce()

# Found false on safe -> safer
# asys = m.parseTerm("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/1),2)")
# asys.reduce()

# Terminates
# asys = m.parseTerm("asys(36,basicCond and testBounds1(3/1,2/1,1/1,1/10),2)")
# asys.reduce()


# Resilience terminated
# asys = m.parseTerm("asys(36,basicCond and testBounds1(5/1,4/1,1/1,1/10),2)")
# asys.reduce()

# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds2(3/1,2/1,1/1,1/10),2)")
# asys.reduce()

# asys = m.parseTerm("asys(36,basicCond and testBounds2(50/1,20/1,10/1,1/10),2)")
# asys.reduce()


# Found false on safe -> safer
# asys = m.parseTerm("as0(2,3/1,2/1,1/1,1/1)")
# asys.reduce()

# asys = m.parseTerm("asys(36,basicCond and testBounds3(3/1,2/1,1/1,1/10),2)")
# asys.reduce()

# ====> End Time = 38.208381902
# ====> Total Time = 37.776897577
# 0:00:37.776898
# asys = m.parseTerm("asys(36,basicCond and testBounds3(5/1,3/1,1/1,1/10),2)")
# asys.reduce()

# ====> Total Time = 38.264596544
# 0:00:38.264597
# asys = m.parseTerm("asys(36,basicCond and testBounds3(5/1,4/1,1/1,1/10),2)")
# asys.reduce()

# ====> Total Time = 37.420199673
# 0:00:37.420200
# asys = m.parseTerm("asys(36,basicCond and testBounds3(4/1,3/1,1/1,1/10),2)")
# asys.reduce()

# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds3(4/1,2/1,1/1,1/10),2)")
# asys.reduce()

# Does not terminate
# asys = m.parseTerm("asys(36,basicCond and testBounds3(4/1,2/1,1/2,1/10),2)")
# asys.reduce()

# ====> End Time = 38.385381189
# ====> Total Time = 37.826043348
# 0:00:37.826043
# asys = m.parseTerm("asys(36,basicCond and testBounds3(4/1,5/2,1/2,1/10),2)")
# asys.reduce()

# checkTimeDur(m,asys)
# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(2).NzNat","safeSP","badSP","saferSP")


# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP-timesteps-split.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')
# asys = m.parseTerm("asys(36,basicCond and testBounds1(5/1,4/1,1/1,1/1),2)")
# asys.reduce()
# # ====> Total Time = 59.256820975000004
# # 0:00:59.256821
# # checkTimeDur(m,asys)
# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(3).NzNat","safeSP","badSP","saferSP")
# # ====> Total Time = 164.71378402899998
# # 0:02:44.713784

# maude.load("vehicle/examples/platooning/load-platooning-manh-simple.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')
# asys = m.parseTerm("asys(36,basicCond and testBounds1(5/1,4/1,1/1,1/1),2)")
# asys.reduce()
# 0:00:59.256821
# checkTimeDur(m,asys)
# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(3).NzNat","safeSP","badSP","saferSP")
# 0:00:17.151283

# maude.load("vehicle/examples/platooning/load-platooning-manh-simple.maude")
# hook = SMT_CHECK()
# maude.connectEqHook('smtCheck',hook)
# m = maude.getModule('SCENARIO-PLATOONING')
# asys = m.parseTerm("asys(36,basicCond and testBounds1(5/1,4/1,1/1,1/10),1)")
# asys.reduce()
# 0:00:59.256821
# checkTimeDur(m,asys)

# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(1).NzNat","safeSP","badSP","saferSP")


# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(2).NzNat","safeSP","badSP","saferSP")
# System is not resilient.
# ====> End Time = 58.748187671
# ====> Total Time = 58.409322665
# 0:00:58.409323

# isResilient(m,"['SCENARIO-PLATOONING]",str(asys),"(3).NzNat","safeSP","badSP","saferSP")



















# asys2 = m.parseTerm("enforceSP(" + "safeSP,setStopTime(" + str(asys) + ",1))")
# res1 = m.parseTerm("afterTicksSP(['SCENARIO-PLATOONING],upTerm(" + str(asys2) + "),1,saferSP)")
# res1.reduce()
# res2 = m.parseTerm("afterTicksSP(['SCENARIO-PLATOONING],upTerm(" + str(asys2) + "),1,safeSP)")
# res2.reduce()
# res3 = m.parseTerm("afterTicksSP(['SCENARIO-PLATOONING],upTerm(" + str(asys2) + "),1,unsafeSP)")
# res3.reduce()

# print(res1)
# print(res2)
# print(res3)


# asys2 = m.parseTerm("enforceSP(" + "safeSP," + str(asys) + ")")
# asys2.rewrite(3)
# test = m.parseTerm("alwaysSP(safeSP," + str(asys2) + ")")
# test.reduce()
# test2 = m.parseTerm("alwaysSP(saferSP," + str(asys2) + ")")
# test2.reduce()

# print(test)
# print(test2)

# asys.rewrite(3)
# # print(asys)
# log = basic_lib.printLog(m,smt_model,asys)
# print(log)


# start = timer()
# print("=====> Start Time =", start)
# # TODO: Figure out the correct parameters for the isResilient call, e.g., which SPs to use.
# t = m.parseTerm("isResilient(['SCENARIO-PLATOONING], as0(2), 2, safeSP,badSP,saferSP)")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))


# start = timer()
# print("=====> Start Time =", start)
# t = m.parseTerm("isResilientDT(['SCENARIO-PLATOONING], as0(2), 2, safeSP,badSP,saferSP)")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# (false).Bool
# With all theories
# # ====> End Time = 47.215433006
# # ====> Total Time = 46.853273083
# # 0:00:46.853273
# (false).Bool
# Only QF_NRA
# ====> End Time = 35.042378104
# ====> Total Time = 34.641758278
# 0:00:34.641758





