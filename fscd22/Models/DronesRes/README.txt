This directory defines a simple drone capable of visiting
a finite set of points then returning home.  Two strateties
are defined for choosing the next point to visit: waypoint
and closest point.

Simple drones use the following sensors: locS, energyS, speedS.
There are also obstacleS and teS (time elapsed) sensors.
The latter is only used with SITL.  Use of obstacle information to appear.
Currently there is a location sensor fault model and a 

Drone actions are: takeOff(id,alt), land(id), goTo(id,loc), stop(id).
High level actions are refined by a controller function to incremental actions
that take speed into account.
There are takeOff, land, and goTo action fault models (only goTo has been tested).
The function transformAction, applies fault models to produce faulty actions
which are then executed by doEAct.  This separates the physical action
that could be done by Maude or by a simulator, from the fault models
(not represented in simulators).


Constructors for 1 and 2 drone scenarios are defined in  scenario.maude
Fault injection functions are also define there.  Examples of use
are at the end.



The model has a number of global parameters that are set in
scenario-params.maude  These include equations specializing
generic functions.


To use waypoint, choose the following equations in scenario-oarams
  eq nextLoc(id,kb) = nextLocSimple(id,kb) .
  eq updateTargets(id,act,kb) = updateTargetsSimple(id,act,kb) .

To use closestpoint, choose the following equations in scenario-params
  eq nextLoc(id,kb) = nextLocSCP(id,kb) .
  eq updateTargets(id,act,kb) = updateTargetsSCP(id,act,kb) .

Waypoint is deterministic.  Closestpoint uses the SCP solver 
and can return multiple action options.  

For the solver to return only the maximally ranked actions
choose the following equation in scenario-params
  eq updateRks(rks,act,rv) = updateRksMx(rks,act,rv) .

For the solver to return all ranked actions that pass
a threshold choose the following equation in scenario-params
  eq updateRks(rks,act,rv) = updateRksAll(rks,act,rv) .

When the solver returns mulitple choices, the soft-agent rule
can aribtrarily select one 
  eq selectKeK(kb,kekset) = bestKeK(kb,kekset) .
or let Maude choose (useful for search)
  eq selectKeK(kb,kekset) = allKeK(kb,kekset) .

scenario-params also includes some definitions for accumulating
meta-data and logs, which can be refined or augmented as desired.


