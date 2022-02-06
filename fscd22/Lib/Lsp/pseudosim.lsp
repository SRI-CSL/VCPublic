;; Fake simulator to test the IOPMaude  actors 
/*
SoftAgents/SA1/Lib/meta-cp-e  
   -- just stats control doRun with randIx randInc
SoftAgents/Maude4/Lib/meta-cp-e

*/

;;; (load "/Users/clt/Repositories/imaude/jlib/jl-util.lsp")
(load "../../../../imaude/jlib/jl-util.lsp")

/* 
 road 
  id :: Id
  start :: meters
  stop ::  meters
  [width]
  vehicles ::
*/  

/*
vehicle kb
  id :: IdStr
  road  :: Id
  acts ::   ActSet 
  sensors :: SensorKb
  state :: VStateKb
 
 vStateKb
   pos (lat,lon) in meters
   vel (vlat,vlon) in m/s
   acc (alat,alon) in m/s/s
*/

(define dbl2ratstr (d) 
(concat (sinvoke "java.lang.Math" "round" (*  d (double 100)))
"/" "100")
)
   
(define state2op (apply mkMap2 "pos" "atloc" "vel" "speed"))
(invoke state2op "put" "acc" "accel")


 ;;; all vals are double arrays of len 2
(define mkstateItem (time vname key val)    
 (let ((strb (object ("java.lang.StringBuffer")))
       (kop (invoke state2op "get" key))
       (kval (apply dbl2ratstr (aget val (int 1))) )
      )
    (invoke strb "append" lp)
     (invoke strb "append" kop)
     (invoke strb "append" lp)
     (invoke strb "append"  vname)
     (invoke strb "append" ", ")
     (invoke strb "append" 
        (if (= key "pos") (concat "loc" lp kval rp) kval))
     (invoke strb "append" rp)
     (invoke strb "append" " @ ")
     (invoke strb "append" time)
    (invoke strb "append" rp)
    (invoke strb "toString")
 ))

/*   
 vSensorKb
   pos (lat,lon) in meters
   vel (vlat,vlon) in m/s
   acc (alat,alon) in m/s/s
   gapNext (glon)  in m
*/
(define sensor2op (apply mkMap2 "pos" "atloc" "vel" "speed"))
(invoke sensor2op "put" "acc" "accel")
(invoke sensor2op "put" "gapNext" "gapNext")

;;; all vals but gap are double arrays of len 2
(define mksensorItem (time vname key val)    
 (let ((strb (object ("java.lang.StringBuffer")))
       (kop (invoke sensor2op "get" key))
       (kval (if (= key "gapNext") 
               (if (isobject val)
                   (apply dbl2ratstr (aget val (int 0)))
                   "-1")
               (apply dbl2ratstr (aget val (int 1)))
               ) ) 
       )
   (if (or (!= key "gapNext") (!= kval "-1"))
    (seq
    (invoke strb "append" lp)
     (invoke strb "append" kop)
     (invoke strb "append" lp)
     (invoke strb "append"  vname)
     (invoke strb "append" ", ")
     (invoke strb "append" 
        (if (= key "pos") (concat "loc" lp kval rp) kval))
     (invoke strb "append" rp)
     (invoke strb "append" " @ ")
     (invoke strb "append" time)
    (invoke strb "append" rp)
     ))
   (invoke strb "toString")
 ))
  
/*
act [alat,alon] m/s/s  
*/  

(define mkAAct (alat alon)
   (apply mkPair "aact" (array double alat alon)))
(define isAAct (q)
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "aact")
     (boolean false) 
     )
   )  
(define getALat (q) (aget (invoke q "get" (int 1)) (int 0)))
(define getALon (q) (aget (invoke q "get" (int 1)) (int 1)))


(define mkAddAct (act)(apply mkPair "addAct" act))
(define isAddAct (q)
  (if (and  (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "addAct")
     (boolean false) ))
(define getQAddAct (q)(invoke q "get" (int 1)))
  
(define mkGetName ()(apply mkSingle "getName"))
(define isGetName (q)
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getName")
     (boolean false) ))
  
(define mkClearActs ()(apply mkSingle "clearActs"))
(define isClearActs (q)
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "clearActs")
     (boolean false) ))
  
(define mkGetActs ()(apply mkSingle "getActs"))
(define isGetActs (q)
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getActs")
     (boolean false) ))
(define getQActs (q) (invoke q "get" (int 1)))

(define mkGetStateMap ()(apply mkSingle "getStateMap"))
(define isGetStateMap (q) 
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getStateMap")
     (boolean false) ))
  
(define mkSetStateMap (smap)(apply mkPair "setStateMap" smap))
(define isSetStateMap (q) 
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "setStateMap")
     (boolean false) ))
(define getQStateMap (q) (invoke q "get" (int 1)))
  
(define mkGetSensorMap ()(apply mkSingle "getSensorMap"))
(define isGetSensorMap (q) 
  (if (and (instanceof q "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getSensorMap")
     (boolean false) ))
  
(define mkSetSensorMap (smap)(apply mkPair "setSensorMap" smap))
(define isSetSensorMap (q) 
  (if (and (instanceof q "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "setSensorMap")
     (boolean false) ))
(define getQSensorMap (q) (invoke q "get" (int 1)))
  
(define mkVehicle (kb)
(lambda (q)
  (if (apply isClearActs q)
    (seq (invoke kb "put" "acts" (apply mkMt)) "Ok")
  (if (apply isAddAct q)
    (let ((acts (invoke kb "get" "acts")))
      (invoke acts "add" (apply getQAddAct q)) "Ok")
  (if (apply isGetName q)
     (invoke kb  "get" "name") 
  (if (apply isGetActs q)
     (invoke kb  "get" "acts") 
  (if (apply isGetStateMap q)
    (invoke kb "get" "state")
  (if (apply isGetSensorMap q)
    (invoke kb "get" "sensors" )
    (object null) ))))))
 ))
 
/*
worldKb
  time : Nat sec?
  vehicles : VId -> Vehicle
  vlen: Float --- for crash calculation  default 4 meters
future
  roads : RoadSet
  network :
   
Queries
 addVeh(vehs)
 doStep  -- 1s time passes
 getVehMap
 
*/ 

(define mkDoStep ()(apply mkSingle "doStep"))
(define isDoStep (q)
  (if (and (instanceof q "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "doStep")
     (boolean false) ))

(define mkGetVehMap ()(apply mkSingle "getVehMap"))
(define isGetVehMap (q) 
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getVehMap")
     (boolean false) ))
  
(define mkGetTime ()(apply mkSingle "getTime"))
(define isGetTime (q) 
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 0)) )
     (= (invoke q "get" (int 0)) "getTime")
     (boolean false) ))

(define mkAddVeh (vid veh)(apply mkTriple "addVeh" vid veh))
(define isAddVeh (q) 
  (if (and (instanceof q  "java.util.ArrayList")
           (> (invoke q "size") (int 2)) )
     (= (invoke q "get" (int 0)) "addVeh")
     (boolean false) ))
(define getQVeh (q) (invoke q "get" (int 2)))
(define getQVid (q) (invoke q "get" (int 1)))
  
(define mkWorld (kb)
(lambda (q)
  (if (apply isAddVeh q)
    (invoke (invoke kb "get" "vehicles") "put"
                (apply getQVid q) (apply getQVeh q))
  (if (apply isGetTime q)
    (aget (invoke kb "get" "time") (int 0) )
  (if (apply isGetVehMap q)
    (invoke kb "get" "vehicles")
  (if (apply isDoStep q)
    (let ((vmap (invoke kb "get" "vehicles") )
          (t (aget (invoke kb "get" "time") (int 0)) )
          )
     (apply doVehActs (invoke vmap "values"))
     (let ((gapMap (apply computeGapCrash vmap
                   (apply dget kb "vlen" (double 4)))) )
        (apply updateSensors vmap gapMap)
        (invoke kb "put" "time" (array int (+ t (int 1)))) 
      ) 
    )
  (object null)
   )) ))
 ))

;;; one macro time step all veh
;;; keep original pos for crash test
(define doVehActs (vehs) 
  (for veh vehs
    (let ((vstate (apply veh (apply mkGetStateMap)))
          (acts (apply veh (apply mkGetActs)))
          )
      (invoke vstate "put" "opos" (invoke vstate "get" "pos") )        
      (apply veh (apply mkClearActs))
      (for act acts 
         (apply doVehAAct vstate (apply getALat act) (apply getALon act)))
   ) )
  (boolean true)
 )

;;; one sec time step one vehf
;;; the only acts are acc alat alon  
/* accelerate for 1 sec
distance traveled in time dt at constant acc starting at sp0
dist(dt,sp0,a) = dt * sp0 + 1/2 * a * dt^2   
               = dt ( sp0 + 1/2 * a * dt)
speed after constant accelleration a for time dt starting from speed sp0
sp(sp0,a,dt) =  sp0 + (a * dt)
*/
(define doVehAAct (vstate alat alon)
  (let ((opos (invoke vstate "get" "pos"))
        (ovel (invoke vstate "get" "vel"))
        (oacc (invoke vstate "get" "acc"))
        (oplon (aget opos (int 1)))
        (ovlon (aget ovel (int 1)))
        (nplon (+ (+ oplon  ovlon) (* (double .5)  alon)))
        (nvlon (+ ovlon alon))
        (oplat (aget opos (int 0)))
        (ovlat (aget ovel (int 0)))
        (nplat (+ (+ oplat  ovlat) (* (double .5)  alat)))
        (nvlat (+ ovlat alat))
        )
     (invoke vstate "put" "pos" (array double nplat nplon))   
     (invoke vstate "put" "vel" (array double nvlat nvlon))   
     (invoke vstate "put" "acc" (array double alat alon))   
     (boolean true)
  ))

;;; intervals [pi opi], [pj,opj] should not intersect
;; assume pi >= opi ...
(define _crashed (pi opi pj opj) 
  (if (= pi pj)
    (boolean true)
  (if (> pi  pj)
      (< opi pj) 
  (if (> pj  pi)
      (< opj pi) 
  ))))    

/*
if opi < opj (opj - opi > vlen)
then crash if npj - npi < vlen 
[ i ]   [ j ] >>  [  i [] j]
*/
(define crashed (pi opi pj opj vlen) 
  (if (< opi opj)  ;;; vj leads
   (not (> (- pj pi) vlen))
   (not (> (- pi pj) vlen))
   ))    


/*   
 vSensorKb
   pos (lat,lon) in meters
   vel (vlat,vlon) in m/s
   acc (alat,alon) in m/s/s
   gapNext (glon)  in m
*/
;;; vehs is map
;;; (apply updateSensors vmap gapMap)
(define updateSensors (vmap gapMap)
  (for key (invoke vmap "keySet")
    (let ((veh (invoke vmap "get" key))
          (vstate (apply veh (apply mkGetStateMap)))
          (vsensors (apply veh (apply mkGetSensorMap)))
          (status (invoke vstate "get" "status"))
          )
     (if (= status "crashed")  
       (boolean false)
       (seq
         (invoke vsensors "put" "pos" (invoke vstate "get" "pos"))
         (invoke vsensors "put" "vel" (invoke vstate "get" "vel"))
         (invoke vsensors "put" "acc" (invoke vstate "get" "acc"))
         (invoke vsensors "put" "gapNext" (invoke gapMap "get" key)) 
         (boolean true)
       ) )
  ) ))



;; sets status crashed if needed
;; returns gapMap : vkey -> (array double gapNext) 
(define computeGapCrash (vmap vlen)
 (let ((gapMap (apply mkMtMap))
       (keys (apply toArrl (invoke vmap  "keySet")))
       (len (invoke keys "size"))
       )
  (for i (- len (int 1))
    (let ((ki (invoke keys "get" i))
          (vi (apply (invoke vmap "get" ki) (apply mkGetStateMap)))
          (pi (aget (invoke vi "get" "pos") (int 1))) 
          (opi (aget (invoke vi "get" "opos") (int 1))) 
          (i1 (+ i (int 1)))
         )
;;;   (for j (object ("g2d.jlambda.Range" (+ i (int 1)) len (int 1)))
      (for j (- len i1)
        (let ((kj (invoke keys "get" (+ j i1)))  ;;; j
              (vj (apply (invoke vmap "get" kj) (apply mkGetStateMap)))
              (pj (aget (invoke vj "get" "pos") (int 1))) 
              (opj (aget (invoke vj "get" "opos") (int 1))) 
              )
         (if (apply crashed pi opi pj opj vlen)
            (seq
              (invoke vi "put" "status" "crashed")
              (invoke vj "put" "status" "crashed")
             )
          (let ((gni (invoke gapMap "get" ki) ) 
                (gnj  (invoke gapMap "get" kj)) 
                (gniv (if (isobject gni) (aget gni (int 0)) (double -1)))
                (gnjv (if (isobject gnj) (aget gnj (int 0)) (double -1)))
                )
           (if (> pi pj)
             ;; check pi is next in front of pj
             (if  (or (< gnjv (int 0)) (> gnjv (- pi pj)))
                  (invoke gapMap "put" kj (array double (- pi pj))))
                  ;; ow current gap is closer
             ;; assume pi =/= pj ow crashed
             ;; check pj is next in front of pi
             (if  (or (< gniv (int 0)) (> gniv (- pj pi)))
                  (invoke gapMap "put" ki (array double (- pj pi))))
                  ;; ow current gap is closer
             )            
          ))  ;; if crashed         
      )) ))  ;; for let for let
    ;; clear opos
    (for veh (invoke vmap "values")
      (let ((vstate (apply veh (apply mkGetStateMap))))
        (invoke vstate "remove" "opos"))
    )  
     gapMap
   ))

;;;;;;; generating replies

;;; (apply genKb wrld (apply mkGetStateMap) mkStateItem)
;;; (apply genKb wrld (apply mkGetSensorMap) mkSensorItem)
 
;;; returns a string ... (atloc(id,lon)  @ t) ....
(define genKb (world cmd mkItemFn)
 (let ((time (apply world (apply mkGetTime)))
       (vmap (apply world (apply mkGetVehMap)))
       (vehs (invoke vmap "values"))
       (res (object ("java.lang.StringBuffer")))
       )
   (for veh vehs
     (let ((vname (apply veh (apply mkGetName) ))
           (vstate (apply veh cmd))
           )
        (for key (invoke vstate "keySet")
         (let ((val (invoke vstate "get" key)))
            (invoke res "append" (apply mkItemFn time vname key val))
            (invoke res "append" " ")
          )
        ))  )       
     (invoke res "toString")
    ))


;;; acts ~ (array object (array object vid acc (double 0) (double  alon)))
 
(define doActs (mname simname wid acts)
(let ((wrld (fetch wid)))
  (if (not (isobject wrld))
   (seq (apply print2err (concat "no such world " wid))
        (sinvoke "g2d.util.ActorMsg"  "send" "maude" "g2d"   "none"))
  (let ((vmap (apply wrld (apply mkGetVehMap))) )
  ;; set acts
    (for act acts
     (let ((vid (aget act (int 0)))
           (actid (aget act (int 1)))
           (alat (aget act (int 2)))
           (alon (aget act (int 3)))
           (veh (invoke vmap "get" vid))
          )
      (apply veh (apply mkAddAct (apply mkAAct alat alon)))
      ))
  ;; do step
    (apply wrld (apply mkDoStep))
  ;; prepare reply
    (let ((statestr (apply genKb wrld (apply mkGetStateMap) mkstateItem))
          (sensorstr (apply genKb wrld (apply mkGetSensorMap) mksensorItem))
         )
(apply print2err (concat "state:  " statestr))
(apply print2err (concat "sensor:  " sensorstr))
;;;; (sinvoke "g2d.util.ActorMsg" "send" mname simname (concat statestr " " sensorstr) )
(sinvoke "g2d.util.ActorMsg" "send" mname simname  statestr) 
    ) 
   ))
  ))
  
(define initVeh (vid loc spd)
 (let ((vkb (apply mkMtMap))
       (state (apply mkMtMap)))
  (invoke vkb "put" "name" vid)
  (invoke vkb "put" "acts" (apply mkMt))
  (invoke vkb "put" "state" state)
  (invoke vkb "put" "sensors" (apply mkMtMap))
  (invoke state "put" "pos" (array double (int 0) loc))
  (invoke state "put" "vel" (array double (int 0) spd))
  (invoke state "put" "acc" (array double (int 0) (int 0)))
 (apply mkVehicle vkb)
 ))  

(define initWorld (wid vehs)
 (let ((wkb (apply mkMtMap))
       (vmap (apply mkMtMap)) )
   (invoke wkb "put" "vehicles" vmap)      
   (invoke wkb "put" "time" (array int (int 0)))
   (for veh vehs (invoke vmap "put" (apply veh (apply mkGetName)) veh))      
   (let ((world (apply mkWorld wkb))) (setUID world wid) )
 ))
