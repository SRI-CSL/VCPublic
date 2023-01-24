def parseToNum(strNum):
  strNum = str(strNum)
  nums = strNum.split("/")
  num = int(nums[0])
  if len(nums) == 2:
    den = int(nums[1])
  else:
    den = 1
  return num / den

def toMaudeSmtModel(maude,smt_model):
  strAcc = ""
  for var in smt_model:
    # print(var)
    if "vv" in var:
      varStr = (var.rstrip("\"")).lstrip("\"")
      if "," in var:
        varStr = (varStr.replace(",",",\"")).replace(")","\")")
      strAcc = strAcc + " (" + varStr + " |-> " + "\"" + str(smt_model[var]) + "\")"
  # print(strAcc)
  smtModel = maude.parseTerm(strAcc)
  smtModel.reduce()
  return smtModel

def getAsg(m,smt_model,sym):
  vv = m.parseTerm("getVVs(" + str(sym) + ",none)")
  vv.reduce()
  if str(vv) in smt_model:
    print(smt_model[str(vv)])
    return parseToNum(smt_model[str(vv)])
  else:
    return False

def printLog(m,smt_model,asys,ids):
  maudeSmt = toMaudeSmtModel(m,smt_model)
  asysStr = str(asys)
  asysLog = m.parseTerm("evalLog(" + str(maudeSmt) +  "," + asysStr + ")")
  asysLog.reduce()
  # ids = m.parseTerm("getIds(" + asysStr + ")")
  # ids.reduce()
  # print(ids)
  return prettyPrint(m,asysLog,ids)

def getLog(m,asys):
  log = m.parseTerm("getSymLog(" + str(asys) + ")")
  log.reduce()
  return log

def prettyPrint(m,log,ids):
  # print(log)
  posX = dict()
  posY = dict()
  spd = dict()
  acc = dict()
  sen = dict()
  logs = str(log).split("::")
  for id in ids:
    posX[id] = []
    posY[id] = []
    spd[id] = []
    acc[id] = []
    sen[id] = []
  for log in logs:
    for id in ids:
      px = m.parseTerm("getPosX(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      px = px.replace("\"","")
      posX[id].append(parseToNum(px))
      px = m.parseTerm("getPosY(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      px = px.replace("\"","")
      posY[id].append(parseToNum(px))
      px = m.parseTerm("getSpd(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      px = px.replace("\"","")
      spd[id].append(parseToNum(px))
      px = m.parseTerm("getAcc(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      px = px.replace("\"","")
      acc[id].append(parseToNum(px))
      px = m.parseTerm("getSenPedId(" + id + "," + log + ")")
      px.reduce()
      id1 = str(px)
      px = m.parseTerm("getSenPedX(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      px1 = parseToNum(px.replace("\"",""))
      px = m.parseTerm("getSenPedY(" + id + "," + log + ")")
      px.reduce()
      px = (str(px).replace("rs(","")).replace(")","")
      py = parseToNum(px.replace("\"",""))
      sen[id].append([id1,px,py])
  print("PosX-->",posX)    
  print("PosY-->",posY)    
  print("Spd-->",spd)    
  print("Acc-->",acc)    
  print("Sen-->",sen)    
  # print(posY)    
  return [posX,posY,spd,acc,sen]




