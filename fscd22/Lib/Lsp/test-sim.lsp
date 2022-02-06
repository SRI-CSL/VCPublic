;;; initialize sim actor
(load "pseudosim.lsp")

(define val2str (val)
  (if (apply isArray val)
    (apply prArr val)
    (concat val "")))

(define printMap (map)
  (for key (invoke map "keySet")
    (let ((val (invoke map "get" key)))
      (apply print2err (concat key " := " (apply val2str val) ))
  )))



/*
;;; initalize scenario with 2 vehicles
(let ((v0 (apply initVeh "v(0)" (double 1000) (double 25))) (v1 (apply initVeh "v(1)" (double 945) (double 20))) ) (setUID v0 "v(0)") (setUID v1 "v(1)") (apply initWorld "w0" (apply mkPair v0 v1)) )

;; execute 1 step (1 second)
(apply doActs "maude" "g2d" "w0" (array java.lang.Object (array java.lang.Object "v(0)" "acc" (double 0) (double 5)) (array java.lang.Object "v(1)" "acc" (double 0) (double 3)) ))
*/

/*

state:  (accel(v(1), 300/100) @ 1) (atloc(v(1), loc(96650/100)) @ 1) (speed(v(1), 2300/100) @ 1) (accel(v(0), 500/100) @ 1) (atloc(v(0), loc(102750/100)) @ 1) (speed(v(0), 3000/100) @ 1)
sensor:  (accel(v(1), 300/100) @ 1) (atloc(v(1), loc(96650/100)) @ 1) (speed(v(1), 2300/100) @ 1) (gapNext(v(1), 6100/100) @ 1) (accel(v(0), 500/100) @ 1) (atloc(v(0), loc(102750/100)) @ 1) (speed(v(0), 3000/100) @ 1)
189
maude
g2d
(accel(v(1), 300/100) @ 1) (atloc(v(1), loc(96650/100)) @ 1) (speed(v(1), 2300/100) @ 1) (accel(v(0), 500/100) @ 1) (atloc(v(0), loc(102750/100)) @ 1) (speed(v(0), 3000/100) @ 1)

*/

/*
op sensorKb : KB -> KB .
 
(apply printMap (apply (fetch "v(0)") (apply mkGetStateMap)))
(define smap (apply (fetch "v(0)") (apply mkGetStateMap)))
(apply printMap (apply (fetch "v(0)") (apply mkGetSensorMap)))

*/
