The following files define the syntax and semantics of CPSPs.

 term.maude      ---  the algebra of terms, various sets of terms,
                 ---  substitution operations ...
								 ---  this serves and the language that can be used to
								      construct protocol messages
 protocol.maude  ---  defines events, roles, protocols
                 --- also some manipulation of SMT terms
 constraints.maude  --- the constraint mechanism used by smart/symbolic intruders
 exe.maude       --- defines the structure of configurations and the execution rules


load-timed.maude  --- loads the above modules
                  --- uncomment the protocol of interest to load it as well.


The timed intruder model makes use of two kinds of constraints: message constraints
and timing constraints. An intruder generates symbolic terms, rather than concrete
instances, starting with terms seen, or known initially, and terms that guesable,
and the message constraints ensure that instances of these terms are intruder
derivable.

The (symbolic) timing constraints are accumulated as protocol steps with
time information are executed.  The integrated SMT solver is used to check
satisfiability of the accumulated constraints, and execution does not
proceed when the constraints are not satisfiable.
In principle we should use Maudes command for rewriting mod SMT,
but there are many limitiation, so we define our own search strategy
and use reflection to access the SMT solver.

A system configuration has the following components:
 
PlayerConf --- an multiset of player objects (honest or intruder)
       and honest player object has the current step, the remaining
			 code to execute, and a set of keys known to the player
TimeSym  --- a symbol representing the current time
DSet     --- the message constraints
Boolean  --- a boolean expression in the language of the SMT solver --
             the current timing constraints
Execution -- an event diagram/bundle recording the message transmissions
   (sender/receiver) and an index for each player indicating the number of
	 steps each has executed.
  


The examples folder contains the following case studies.
In each case there is an informal presentation of the protocol
and a citation if relevant, along with sample analysis commands
and the resulting output.
 
attack-in-between-ticks.maude
   --- a simple timed challenge response, showing the In-between-ticks attack 
	 --- due to the verifier using discrete time to measure a continuous time
	 --- interval.

brands.maude 
  --- a distance bounding protocol adapted from Brands and Chaum

meadows.maude
	 --- a collusion attack on a distance bounding protocol from a 
	     paper by Meadows et. al.

paywave.maude 
   --- a simplified model of the contactless payment protocol
   --- with a time constraint added to avoid 
	 
paywave-full.maude
  --- full(er) version of paywave
 