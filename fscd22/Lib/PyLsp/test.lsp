(let ((v0 (apply initVeh "v(0)" (float 1000) (float 25))) (v1 (apply initVeh "v(1)" (float 945) (float 20))) ) (setUID v0 "v(0)") (setUID v1 "v(1)") (apply initWorld "w0" (mklist v0 v1) (float 4)) ))

(apply doActs "maude" "plambda" "w0"  (mklist (mklist "v(0)" "acc" (float 0) (float 2.5)) (mklist "v(1)" "acc" (float 1) (float 2.5)) ))


/*
state:  (atloc(v(0), loc(102625/100)) @ 1) (speed(v(0), 2750/100) @ 1) (accel(v(0), 250/100) @ 1) (atloc(v(1), loc(96625/100)) @ 1) (speed(v(1), 2250/100) @ 1) (accel(v(1), 250/100) @ 1)
sensor:  (atloc(v(0), loc(102625/100)) @ 1) (speed(v(0), 2750/100) @ 1) (accel(v(0), 250/100) @ 1)  (atloc(v(1), loc(96625/100)) @ 1) (speed(v(1), 2250/100) @ 1) (accel(v(1), 250/100) @ 1) (gapNext(v(1), 6000/100) @ 1)
193
maude
plambda
(atloc(v(0), loc(102625/100)) @ 1) (speed(v(0), 2750/100) @ 1) (accel(v(0), 250/100) @ 1) (atloc(v(1), loc(96625/100)) @ 1) (speed(v(1), 2250/100) @ 1) (accel(v(1), 250/100) @ 1) None
*/