The following files define the syntax and semantics of CPSPs.

 term.maude      ---  the algebra of terms, various sets of terms,
                 ---  substitution operations ...
 protocol.maude  ---  defines events, roles, protocols
                 --- also some manipulation of SMT terms
 constraints.maude  --- the constraint mechanism used by smart/symbolic intruders
 exe.maude       --- 


load-timed.maude  --- loads the above modules
                  --- uncomment the protocol of interest to load it as well.
  


Case studies
 
distance-bounding.maude   
   --- a simple timed challenge response, showing the In-between-ticks attack 
	 --- due to the verifier using discrete time to measure a continuous time
	 --- interval.
	 
distance-bounding-run.txt

paywave.maude 
   --- a simplified model of the contactless payment protocol
   --- with a time constraint added to avoid 
	 
paywave-full.maude

paywave-full-run.txt

brands.maude 
 brands-run.txt
 
 