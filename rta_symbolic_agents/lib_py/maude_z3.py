import maude
from z3 import *

class SMT_CHECK(maude.Hook):
  global smt_model
  smt_model = dict()
  solver = Tactic('qfnra').solver()
  def run (self,term,data):
    try:
      module = term.symbol().getModule();
      # solver = Solver();
      # See https://gu-youngfeng.github.io/blogs/smtsolver.html
      solver = Tactic('qfnra').solver()
      # solver.setLogic("QF_NRA")
      arg = next(term.arguments());
      arg.reduce()
      vvs = module.parseTerm("getVVs(" + str(arg) + ",none)")
      vvs.reduce()
      vvsMap = dict();
      # mkVars only if there are variables.
      if(str(vvs) != "(none).Strings"):
        vvsMap = mkVars(vvs,vvsMap,solver)
      # print(term)
      form = mkBool(arg,module,vvsMap,solver);
      # print(form)
      solver.add(form)
      r2 = solver.check()
      print(r2)
      if (str(r2) == "sat"):
        m = solver.model()
        for d in m.decls():
          smt_model[d.name()] = m[d]
          # print(smt_model)
        return module.parseTerm("(true).Bool");
      elif (str(r2) == "unsat"): 
        return module.parseTerm("(false).Bool");
      print("UNDEFINED: NOT ABLE TO DETERMINE SAT")
    except:
      print("ERROR IN EVALUATING SAT ")
      return module.parseTerm("(false).Bool");

def mkVars(vvs,vvsMap,solver):
  args = list(vvs.arguments());
  # Case only one symbol
  if len(args) == 0:
    vvVar = Real(str(vvs))
    vvsMap[str(vvs)] = vvVar
    return vvsMap;  
  for vv in list(vvs.arguments()):
    vvVar = Real(str(vv))
    vvsMap[str(vv)] = vvVar
  return vvsMap;

def mkBool(term,module,vvsMap,solver):
  op = str(term.symbol())
  if (op == "true"):
    return 1 == 1;
  if (op == "false"):
    return 1 == 2;    
  if (op == "_and_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return And(b1,b2);
  if (op == "_or_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return Or(b1,b2);
  if (op == "_implies_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    b3 = Implies(b1, b2)
    return b3;
  if (op == "_xor_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return Xor(b1, b2);
  if (op == "not_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    return Not(b1);
  if (op == "_===_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    arg = next(args)
    t2 = mkArith(arg,module,vvsMap,solver)
    t3 = (t1 == t2);
    return t3;
  if (op == "_<=_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    t3 = t1 <= t2;
    return t3;
  if (op == "_<_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return t1 < t2;
  if (op == "_>=_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return t1 >= t2;
  if (op == "_>_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return t1 > t2;
  print("Term did not match ===> " + term)  
  return 1 / 0;

def mkArith(term,module,vvsMap,solver):
  op = str(term.symbol())
  sort = str(term.getSort())
  # print(term)
  # print(op)
  # print(sort)
  # print(list(term.arguments()))
  # print(term.toFloat())
  if (op == "vv"):
    vvs = module.parseTerm("getVVs(" + str(term) + ",none)")
    vvs.reduce()
    return vvsMap[str(vvs)] 
  # PosRat
  if (list(term.arguments()) == []):
    return term.toFloat()
  if (op == "_+_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return first + second
  if (op == "-_"):    
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    return  - first
  if (op == "_-_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    try:
      second = mkArith(next(args),module,vvsMap,solver)
      return first - second
    except:
      return - first
  if (op == "_*_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return first * second
  if (op == "_/_" and sort == "SymReal"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    # print(first)
    # print(second)
    return  first / second
  if (op == "_/_" and sort == "SymTerm"):
    args = term.arguments()
    # print(term)
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return first / second
  # print(term)
  # print(op)
  # print(sort)
  return 1 / 0

