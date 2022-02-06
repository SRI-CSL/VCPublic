/*
vehicle kb
  id :: IdStr
  road  :: Id  --- not used 
  acts ::   ActSet 
  sensors :: SensorKb
  state :: VStateKb
 
 vStateKb
   pos (lat,lon) in meters  
   vel (vlat,vlon) in m/s
   acc (alat,alon) in m/s/s
*/

(import "plambda.util.StringBuffer")
(define StringBuilder plambda.util.StringBuffer.StringBuffer)
(define lp "(")
(define rp ")")

(import "plambda.actors.actorlib")
(define send plambda.actors.actorlib.send)

  
;;; (import "plambda.actors.console")
;;; (define console () (apply plambda.actors.console.launch))


(import "sys")
;;; (define print2err (string)  (invoke sys.stderr "write" (concat string "\n")))

(define print2err (str)
  (apply sys.stderr.write str)
  (apply sys.stderr.write '\n')
  (apply sys.stderr.flush)
  )
  
  
(define dbl2ratstr (d) (concat (apply round (*  d (float 100))) "/" "100"))

(define state2op (mkdict "pos" "atloc" "vel" "speed"  "acc" "accel"))

(define mkstateItem (time vname key val)    
 (let ((strb (apply StringBuilder))
       (kop (invoke state2op "get" key))
       (kval (apply dbl2ratstr (get val (int 1)))) 
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
    (apply str strb)
 ))

/*
(define res (apply mkstateItem (int 2) "v(0)" "pos" (mklist (float 0) (float 1.1))))
*/

;;;;;;;;;;;;;;;

/*   
 vSensorKb
   pos (lat,lon) in meters
   vel (vlat,vlon) in m/s
   acc (alat,alon) in m/s/s
   gapNext (glon)  in m
*/

(define sensor2op (mkdict "pos" "atloc" "vel" "speed" "acc" "accel" "gapNext" "gapNext"))

;;; all vals but gap are double arrays of len 2
(define mksensorItem (time vname key val)    
 (let ((strb (apply StringBuilder))
       (kop (invoke sensor2op "get" key))
       (kval (if (= key "gapNext") 
               (if (isobject val)
                   (apply dbl2ratstr val)
                   "-1")
               (apply dbl2ratstr (get val (int 1)))
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
   (apply str strb)
 ))
 
 /*
 (define res1 (apply mksensorItem (int 2) "v(0)" "gapNext" (float 50.5)))
 (define res2 (apply mksensorItem (int 2) "v(0)" "gapNext" None))
 */
 
;;;;;;;;;;;;;;;;;;;;

/*
act [alat,alon] m/s/s  
*/  

;; floats
(define mkAAct (alat alon)
   (mkList "aact" (mklist alat alon)))
(define isAAct (q)
  (if (and (apply isinstance q  list)
           (> (apply len  q) (int 0)) )
     (is (get q  (int 0)) "aact")
     (boolean false) 
     )
   )  
(define getALat (q) (get (get q  (int 1)) (int 0)))
(define getALon (q) (get (get q (int 1)) (int 1)))

/*
(define act0 (apply mkAAct (float .5) (float 2)))
(apply isAAct act0)
(apply getALat act0)
*/

(define mkAddAct (act) (mklist "addAct" act))
(define isAddAct (q)
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q (int 0)) "addAct")
     (boolean false) ))
(define getQAddAct (q)(get q (int 1)))

/*

(define adda0 (apply mkAddAct act0))
(apply isAddAct adda0)
(apply getQAddAct adda0)

*/  
(define mkGetName ()(mklist "getName"))
(define isGetName (q)
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q (int 0)) "getName")
     (boolean false) ))
  
(define mkClearActs () (mklist "clearActs"))
(define isClearActs (q)
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q (int 0)) "clearActs")
     (boolean false) ))
  
(define mkGetActs ()(mklist "getActs"))
(define isGetActs (q)
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "getActs")
     (boolean false) ))
(define getQActs (q) (get q  (int 1)))

(define mkGetStateMap ()(mklist "getStateMap"))
(define isGetStateMap (q) 
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "getStateMap")
     (boolean false) ))
  
(define mkSetStateMap (smap)(mklist  "setStateMap" smap))
(define isSetStateMap (q) 
  (if (and (apply isinstance q  list )
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "setStateMap")
     (boolean false) ))
(define getQStateMap (q) (get q  (int 1)))
  
(define mkGetSensorMap ()(mklist "getSensorMap"))
(define isGetSensorMap (q) 
  (if (and (apply isinstance q list )
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "getSensorMap")
     (boolean false) ))
  
(define mkSetSensorMap (smap)(mklist  "setSensorMap" smap))
(define isSetSensorMap (q) 
  (if (and (apply isinstance q list )
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "setSensorMap")
     (boolean false) ))
(define getQSensorMap (q) (get q  (int 1)))


/*
(define smap1 (apply mkSetSensorMap (mkdict "pos" (mklist (float 0) (float 50.5)))))
(apply isSetSensorMap smap1)
(apply getQSensorMap smap1)
 
*/


(define mkVehicle (kb)
  (lambda (q)
    (if (apply isClearActs q)
      (seq (modify kb  "acts" (mklist)) "Ok")
    (if (apply isAddAct q)
      (let ((acts (invoke kb "get" "acts")))
        (invoke acts "append" (apply getQAddAct q)) "Ok")
    (if (apply isGetName q)
       (invoke kb  "get" "name") 
    (if (apply isGetActs q)
       (invoke kb  "get" "acts") 
    (if (apply isGetStateMap q)
      (invoke kb "get" "state")
    (if (apply isGetSensorMap q)
      (invoke kb "get" "sensors" )
      None ))))))
 ))

;;;; for testing 
(define mkVkb (vid pos vel)
  (mkdict 
    "acts" (mklist)
    "name" vid
    "state" (mkdict
               "pos" (mklist (float 0) pos)
               "vel" (mklist (float 0) vel)
               "acc" (mklist (float 0) (float 0))
              )
    "sensors" (mkdict)
  ))

/*
(define vkb0 (apply mkVkb "v(0)" (float 50) (float 20)))

(define v0 (apply mkVehicle (apply mkVkb "v(0)" (float 50) (float 20))))
(apply v0 (apply mkGetName))
(apply v0 (apply mkGetStateMap))
(apply v0 (apply mkAddAct act0))
(apply v0 (apply mkGetActs))

*/

/*

(define vkb1 (apply mkVkb "v(1)" (float 120) (float 20)))
(define v1 (apply mkVehicle (apply mkVkb "v(1)" (float 120) (float 20))))

*/

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

(define mkDoStep ()(mklist "doStep"))
(define isDoStep (q)
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "doStep")
     (boolean false) ))

(define mkGetVehMap ()(mklist "getVehMap"))
(define isGetVehMap (q) 
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q (int 0)) "getVehMap")
     (boolean false) ))
  
(define mkGetTime ()(mklist "getTime"))
(define isGetTime (q) 
  (if (and (apply isinstance q list)
           (> (apply len q) (int 0)) )
     (is (get q  (int 0)) "getTime")
     (boolean false) ))

(define mkAddVeh (vid veh)(mklist "addVeh" vid veh))
(define isAddVeh (q) 
  (if (and (apply isinstance q list)
           (> (apply len q) (int 2)) )
     (is (get q (int 0)) "addVeh")
     (boolean false) ))
(define getQVeh (q) (get q  (int 2)))
(define getQVid (q) (get q  (int 1)))
  
(define mkWorld (kb)
(lambda (q)
  (if (apply isAddVeh q)
    (modify (invoke kb "get" "vehicles") 
            (apply getQVid q) (apply getQVeh q))
  (if (apply isGetTime q)
     (invoke kb "get" "time") 
  (if (apply isGetVehMap q)
     (invoke kb "get" "vehicles")
  (if (apply isDoStep q)
    (let ((vmap (invoke kb "get" "vehicles") )
          (t (invoke kb "get" "time") )
          )
     (apply doVehActs (invoke vmap "values"))
     (let ((gapMap (apply computeGapCrash vmap 
                          (invoke kb "get" "vlen" (float 4)))) )
        (apply updateSensors vmap gapMap)
        (modify kb  "time" (+ t (int 1))) 
      ) 
    )
  None
   )) ))
 ))

/*

(define wkb0 (mkdict "time" (int 0) "vehicles" (mkdict)))

(define w0 (apply mkWorld (mkdict "time" (int 0) "vehicles" (mkdict))))

(apply w0 (apply mkAddVeh "v(0)" (apply mkVehicle (apply mkVkb "v(0)" (float 50) (float 20)))))
(apply w0 (apply mkAddVeh "v(1)" (apply mkVehicle (apply mkVkb "v(1)" (float 120) (float 20)))))

(apply w0 (apply mkGetTime))
(apply w0 (apply mkGetVehMap))


*/
;;; one macro time step all veh
;;; keep original pos for crash test
(define doVehActs (vehs) 
  (for veh vehs
    (let ((vstate (apply veh (apply mkGetStateMap)))
          (acts (apply veh (apply mkGetActs)))
          )
      (modify vstate  "opos" (invoke vstate "get" "pos") )        
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
        (oplon (get opos (int 1)))
        (ovlon (get ovel (int 1)))
        (nplon (+ (+ oplon  ovlon) (* (float .5)  alon)))
        (nvlon (+ ovlon alon))
        (oplat (get opos (int 0)))
        (ovlat (get ovel (int 0)))
        (nplat (+ (+ oplat  ovlat) (* (float .5)  alat)))
        (nvlat (+ ovlat alat))
        )
     (modify vstate "pos" (mklist nplat nplon))   
     (modify vstate "vel" (mklist  nvlat nvlon))   
     (modify vstate "acc" (mklist  alat alon))   
     (boolean true)
  ))
  
/*

(define vst0 (mkdict "pos" (mklist (float 0) (float 50)) "vel" (mklist (float 0) (float 20)) "acc" (mklist (float 0) (float 0)) )
(apply doVehAAct vst0 (float 1.5) (float 3))

(define vehs0 (mklist (apply mkVehicle (apply mkVkb "v(0)" (float 50) (float 20))) (apply mkVehicle (apply mkVkb "v(1)" (float 120) (float 20))) ))

(apply (get vehs0  (int 0)) (apply mkAddAct (apply mkAAct (float .5) (float 5))))

(apply (get vehs0 (int 1)) (apply mkAddAct (apply mkAAct (float 0) (float 2))))

(apply doVehActs vehs0)

(apply (get vehs0 (int 0)) (apply mkGetStateMap))
{'pos': [0.25, 72.5], 'vel': [0.5, 25.0], 'acc': [0.5, 5.0], 'opos': [0.0, 50.0]}

(apply (get vehs0 (int 1)) (apply mkGetStateMap))
{'pos': [0.0, 141.0], 'vel': [0.0, 22.0], 'acc': [0.0, 2.0], 'opos': [0.0, 120.0]}
*/  

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

(define listKeys (d) (let ((res (mklist))) (for k (invoke d "keys") (invoke res "append" k)) res))

;; sets status crashed if needed
;; returns gapMap : vkey -> gapNext
(define computeGapCrash (vmap vlen)
 (let ((gapMap (mkdict))
       (keys (apply listKeys vmap))
       (num (apply len keys))
       )
  (for i (- num (int 1))
    (let ((ki (get keys i))
          (vi (apply (invoke vmap "get" ki) (apply mkGetStateMap)))
          (pi (get (invoke vi "get" "pos") (int 1))) 
          (opi (get (invoke vi "get" "opos") (int 1))) 
          (i1 (+ i (int 1)))
         )
         (for j (- num i1)
          (let ((kj (get keys (+ j i1 )))
              (vj (apply (invoke vmap "get" kj) (apply mkGetStateMap)))
              (pj (get (invoke vj "get" "pos") (int 1))) 
              (opj (get (invoke vj "get" "opos") (int 1))) 
              )
         (if (apply crashed pi opi pj opj vlen)
            (seq
              (modify vi  "status" "crashed")
              (modify vj  "status" "crashed")
             )
          (let ((gni (invoke gapMap "get" ki (int -1)) ) 
                (gnj  (invoke gapMap "get" kj (int -1))) 
              )
           (if (> pi pj)
             ;; check pi is next in front of pj
             (if  (or (< gnj (int 0)) (> gnj (- pi pj)))
                  (modify gapMap kj  (- pi pj)) )
                  ;; ow current gap is closer
             ;; assume pi is < pj ow crashed
             ;; check pj is next in front of pi
             (if  (or (< gni (int 0)) (> gni (- pj pi)))
                  (modify gapMap  ki (- pj pi)) )
                  ;; ow current gap is closer
             )            
          ))  ;; if crashed         
      )) ))  ;; for let for let
    ;; clear opos
    (for veh (invoke vmap "values")
      (let ((vstate (apply veh (apply mkGetStateMap))))
        (invoke vstate "pop" "opos" None))
    )  
     gapMap
   ))

/*

(define v0 (apply mkVehicle (apply mkVkb "v(0)" (float 50) (float 20))))
(define v1 (apply mkVehicle (apply mkVkb "v(1)" (float 120) (float 20))))

(define vmap0 (mkdict "v(0)" v0 "v(1)"  v1))

(apply v0 (apply mkAddAct (apply mkAAct (float .5) (float 5))))

(apply v1 (apply mkAddAct (apply mkAAct (float 0) (float 2))))

(apply doVehActs (mklist v0 v1))

(define gapmap0 (apply computeGapCrash vmap0))

(define v0x (apply mkVehicle (apply mkVkb "v(0)" (float 50) (float 25))))
(define v1x (apply mkVehicle (apply mkVkb "v(1)" (float 55) (float 20))))
(define vmap0x (mkdict "v(0)" v0x "v(1)" v1x))

(apply v0x (apply mkAddAct (apply mkAAct (float 0) (float 5))))
(apply v1x (apply mkAddAct (apply mkAAct (float 0) (float 0))))

(apply doVehActs (mklist v0x v1x))

(define gapmap0x (apply computeGapCrash vmap0x))

(define v0y (apply mkVehicle (apply mkVkb "v(0)" (float 10) (float 25))))
(define v1y (apply mkVehicle (apply mkVkb "v(1)" (float 50) (float 20))))
(define v2y (apply mkVehicle (apply mkVkb "v(2)" (float 80) (float 20))))

(apply v0y (apply mkAddAct (apply mkAAct (float 0) (float 5))))
(apply v1y (apply mkAddAct (apply mkAAct (float 0) (float 3))))
(apply v2y (apply mkAddAct (apply mkAAct (float 0) (float -5))))

(apply doVehActs (mklist v0y v1y v2y))

(define vmap0y (mkdict "v(0)" v0y "v(1)" v1y "v(2)" v2y))
(define gapmap0y (apply computeGapCrash vmap0y (float 4)))

(apply v2y (apply mkGetStateMap))
*/

;;; vehs is map
;;; (apply updateSensors vmap gapMap)
(define updateSensors (vmap gapMap)
  (for key (invoke vmap "keys")
    (let ((veh (invoke vmap "get" key))
          (vstate (apply veh (apply mkGetStateMap)))
          (vsensors (apply veh (apply mkGetSensorMap)))
          (status (invoke vstate "get" "status"))
          )
     (if (is status "crashed")  
       (boolean false)
       (seq
         (modify vsensors  "pos" (invoke vstate "get" "pos"))
         (modify vsensors  "vel" (invoke vstate "get" "vel"))
         (modify vsensors  "acc" (invoke vstate "get" "acc"))
         (modify vsensors  "gapNext" (invoke gapMap "get" key)) 
         (boolean true)
       ) )
  ) ))

/*
(apply updateSensors vmap0y gapmap0y)
(apply v0y (apply mkGetStateMap))
(apply v0y (apply mkGetSensorMap))

*/
;;;;;;; generating replies
;;; (apply genKb wrld (apply mkGetStateMap) mkstateItem)
;;; (apply genKb wrld (apply mkGetSensorMap) mksensorItem)
 
;;; returns a string ... (atloc(id,lon)  @ t) ....
(define genKb (world cmd mkItemFn)
 (let ((time (apply world (apply mkGetTime)))
       (vmap (apply world (apply mkGetVehMap)))
       (vehs (invoke vmap "values"))
       (res (apply StringBuilder))
       )
   (for veh vehs
     (let ((vname (apply veh (apply mkGetName) ))
           (vstate (apply veh cmd))
           )
        (for key (invoke vstate "keys")
         (let ((val (invoke vstate "get" key)))
            (invoke res "append" (apply mkItemFn time vname key val))
            (invoke res "append" " ")
          )
        ))  )       
     (apply str res)
    ))

/*
(define w0y (apply mkWorld(mkdict "time" (int 2) "vlen" (float 4) "vehicles" vmap0y)))
(setUID w0y "w(0)")

(define states0y (apply genKb w0y (apply mkGetStateMap) mkstateItem))
(atloc(v(0), loc(3750/100)) @ 2) (speed(v(0), 3000/100) @ 2) (accel(v(0), 500/100) @ 2) 
(atloc(v(1), loc(7150/100)) @ 2) (speed(v(1), 2300/100) @ 2) (accel(v(1), 300/100) @ 2) 
(atloc(v(2), loc(9750/100)) @ 2) (speed(v(2), 1500/100) @ 2) (accel(v(2), -500/100) @ 2)

(define sensors0y (apply genKb w0y (apply mkGetSensorMap) mksensorItem))
(atloc(v(0), loc(3750/100)) @ 2) (speed(v(0), 3000/100) @ 2) (accel(v(0), 500/100) @ 2) (gapNext(v(0), 3400/100) @ 2) 
(atloc(v(1), loc(7150/100)) @ 2) (speed(v(1), 2300/100) @ 2) (accel(v(1), 300/100) @ 2) (gapNext(v(1), 2600/100) @ 2) 
(atloc(v(2), loc(9750/100)) @ 2) (speed(v(2), 1500/100) @ 2) (accel(v(2), -500/100) @ 2)

*/

;;; jl acts ~ (array object (array object vid acc (double 0) (double  alon)))
;;; py acts (mklist (mklist vid acc (float 0) (float alon)) ...)

(define doActs (mname simname wid acts)
(let ((wrld (fetch wid)))
  (if (not (isobject wrld))
   (seq (apply print2err (concat "no such world " wid))
        (apply send mname simname "none"))
  (let ((vmap (apply wrld (apply mkGetVehMap))) )
  ;; set acts
    (for act acts
     (let ((vid (get act (int 0)))
           (actid (get act (int 1)))
           (alat (get act (int 2)))
           (alon (get act (int 3)))
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
;;;; (apply send mname simname (concat statestr " " sensorstr) )
    (apply send mname simname  statestr) 
    ) 
   ))
  ))
  
(define initVeh (vid loc spd)
 (let ((vkb (mkdict
             "name" vid
             "acts" (mklist)
             "state" (mkdict
                       "pos" (mklist (float 0) loc)
                       "vel" (mklist (float 0) spd)
                       "acc" (mklist (float 0) (float 0))
                       )
             "sensors" (mkdict)
              )))
 (apply mkVehicle vkb)
 ))  

(define initWorld (wid vehs vlen)
 (let ((vmap (mkdict))
       (wkb (mkdict "time" (int 0) "vehicles" vmap "vlen" vlen))
      )
   (for veh vehs (modify vmap (apply veh (apply mkGetName)) veh))      
   (let ((world (apply mkWorld wkb))) (setUID world wid) )
 ))

/*
;;; py acts (mklist (mklist vid acc (float 0) (float alon)) ...)
(define pyacts (mklist (mklist "v(0)" "acc" (float 0) (float 2.5)) (mklist "v(1)" "acc" (float 1) (float 2.5)) (mklist "v(2)" "acc" (float 0) (float -5))) )


(apply doActs "maude" "plambda" "w(0)" pyacts)
state:  (atloc(v(0), loc(6875/100)) @ 3) (speed(v(0), 3250/100) @ 3) (accel(v(0), 250/100) @ 3) (atloc(v(1), loc(9575/100)) @ 3) (speed(v(1), 2550/100) @ 3) (accel(v(1), 250/100) @ 3) (atloc(v(2), loc(11000/100)) @ 3) (speed(v(2), 1000/100) @ 3) (accel(v(2), -500/100) @ 3)

sensor:  (atloc(v(0), loc(6875/100)) @ 3) (speed(v(0), 3250/100) @ 3) (accel(v(0), 250/100) @ 3) (gapNext(v(0), 2700/100) @ 3) 
(atloc(v(1), loc(9575/100)) @ 3) (speed(v(1), 2550/100) @ 3) (accel(v(1), 250/100) @ 3) (gapNext(v(1), 1425/100) @ 3) (atloc(v(2), loc(11000/100)) @ 3) (speed(v(2), 1000/100) @ 3) (accel(v(2), -500/100) @ 3)

280
maude
plambda
(atloc(v(0), loc(6875/100)) @ 3) (speed(v(0), 3250/100) @ 3) (accel(v(0), 250/100) @ 3) 
(atloc(v(1), loc(9575/100)) @ 3) (speed(v(1), 2550/100) @ 3) (accel(v(1), 250/100) @ 3) 
(atloc(v(2), loc(11000/100)) @ 3) (speed(v(2), 1000/100) @ 3) (accel(v(2), -500/100) @ 3)

(define v20 (apply initVeh "v20" (float 20) (float 25)))
(define v40 (apply initVeh "v40" (float 40) (float 20)))
(apply initWorld "ww" (mklist  v20 v40) (float 4))

(apply doActs "maude" "plambda" "ww" (mklist (mklist "v20" "acc" (float 0) (float 2)) (mklist "v40" "acc" (float 1) (float 4)) ))

state:  
(atloc(v20, loc(4600/100)) @ 1) (speed(v20, 2700/100) @ 1) (accel(v20, 200/100) @ 1) 
(atloc(v40, loc(6200/100)) @ 1) (speed(v40, 2400/100) @ 1) (accel(v40, 400/100) @ 1)
sensor:  
(atloc(v20, loc(4600/100)) @ 1) (speed(v20, 2700/100) @ 1) (accel(v20, 200/100) @ 1) (gapNext(v20, 1600/100) @ 1) 
(atloc(v40, loc(6200/100)) @ 1) (speed(v40, 2400/100) @ 1) (accel(v40, 400/100) @ 1)
184
maude
plambda
(atloc(v20, loc(4600/100)) @ 1) (speed(v20, 2700/100) @ 1) (accel(v20, 200/100) @ 1) 
(atloc(v40, loc(6200/100)) @ 1) (speed(v40, 2400/100) @ 1) (accel(v40, 400/100) @ 1) 
None
*/