
;; (supdate "g2d.util.ActorMsg" "VERBOSE" (boolean true))
;; (supdate "g2d.Main" "DEBUG" (boolean true))


(define makeInteger (int_or_string)
  (sinvoke "java.lang.Integer" "valueOf" int_or_string))

(define makeDouble (double_or_string)
  (sinvoke "java.lang.Double" "valueOf" double_or_string))


(define doRun (handle)
  (sinvoke "g2d.util.ActorMsg"  "send" "maude" handle "doRun")
  )

;; replies with  (apply runResult "handle" val)


(define runResult (handle val)
  (let ((statsObject (fetch handle)))
    (if (isobject statsObject)
		 (seq
;;  	(invoke statsObject "recordRunResult" (apply makeDouble val))
     	(invoke statsObject "recordRunResult" val)
      (invoke java.lang.System.err "println" (concat "runResult: " val))
      (sinvoke "g2d.util.ActorMsg"  "send" "maude" "g2d" "OK")
      (apply doStatsAux handle statsObject (invoke statsObject "done"))
      )) ))
	

(define doStats (handle)
  (let ((statsObject (fetch handle)))
    (if (isobject statsObject)
	(apply doStatsAux handle statsObject (boolean false)))
    )
  )

(define doStatsAux (handle statsObject isDone)
  (if isDone
      (invoke java.lang.System.err "println" statsObject)
    (seq
  	  (invoke java.lang.System.err "println" (concat "calling doRun"))
      (apply doRun handle)
     )) )

