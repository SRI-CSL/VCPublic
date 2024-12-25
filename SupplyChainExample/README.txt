 https://github.com/SRI-CSL/VCPublic} in the folder SuppoyChainExample.

This directory has the Maude specification of an
algorithm for checking (n,a,b)-Resilience as
defined in the paper "Time-Bounded Resilience" by
Tajana Ban Kirigin, Jesse Comer, Max Kanovich,
Andre Scedrov, and Carolyn Talcott (WRLA24 and subsequent expansion for journal publication).
Also included is a manufacturing supply chain
case study (MSC) to demonstrate application of the
algorithm.

We start with an informal description of the case
study. We then explain the algorithm isAbNRes.
Finally the files constuting the Maude
specification and experimental results are listed
with some details about the data structures and
rewrite rules.  There are also instructions 
for running examples and repeating the
experiments.

-------------- Scenario Overview -------------

An MSC configuration consists of a several actors:
a manufacturer, a customer, some part suppliers as
well as pseudo actors that hold execution time
information: the current time, the stopping time
(deadline), and a critical configuration monitor,
and a specification of potential digressions. A
customer has a sequence of product orders to send
to Mfg. Each product has a specification (global
information) giving the parts required, the
assembly time, and the base profit the
manufacturer can expect. When a manufacturer
receives a product order it takes parts from its
inventory for assembly. If more parts are needed
they are ordered from part suppliers (the
inventory may also be refilled, depending on
policy). Once parts are available, assembly is
intiated. When assembly is complete (assembly
duration time has passed) the manufacturer tells
the customer that the product is delivered.

When a part supplier receives an part order, it
`packages' the parts and schedules a delivery
itinerary based on a global transportation graph.
Using this informaion the parts are sent in a
transport message. The trasport graph consists of
links between locations (suppliers,
manufactureres, and intermediate points) and
travel time for each link. The supplier also
replies directly to the mfg giving the estimated
delivery time. (Communication between actors and
parts in transit are represented as different
kinds of message.)

Once the manufacturer knows when all the parts
will be available it informs the customer of the
expected delivery time. The customer keeps track
of outstanding order requests, and when a product
is delivered it records the  actual delivery
time and the expected delivery time. This data is
used to compute a late delivery penalty which is
subracted from the base profit of the given
product.

The base profit associated with a product
abstracts from details such as part and assembly
cost. In addition there is an overhead charge for
parts in inventory or waiting to be assembled.
This is accumulated over time. The manufacturer
profit accumulates the profit for each product
delivered. At any point in time the net profit is
the accumulated profit minus the accumulated
overhead. The overhead rate and delay penalty are
scenario parameters.

Criticallity has two parameters: cdiff and cdur.
A configuration is critical if net profit is
less than cdiff for more than cdur time units.

------------------- isAbNRes  ----------------

The function isAbNRes checks whether a system
starting in configuration iSys has an nab C
resilient trace with respect to given goal and
criticality specification. Rewriting is assumed to
terminate if a critical configuration is reached.
This can be achieved by a simple transformation of
the specification and avoids useless search steps.
(See the specification notes.)

In addition to a system configuration, the
possible updates (called digressions), and s goal
specification, isABNRes has parameters
corresponding to the parameters of the
mathematical definition of resilience:
 nu -- the number of updates,
 tab -- the maximun execution time, 
 ta -- the maximun time updates at which can be applied.
The criticallity parameters of the (journal
version) mathematical definition are part of the
the initial state. It also has auxiliary
parameters that control the search for a witness
trace with the resilience propery.

isABNRes first uses the Maude metafunctions
metaSearch and metaSearchPath to search for a goal
compliant trace (satifies the goal without becoming
critical). If no such trace is found the result is
false. If nu = 0 the found trace is a witness and
true is returned. If nu > 0, the found trace is
truncated to stop at time ta, and given to the
auxiliary function checkAbRes to check the
resilience  conditions.

checkAbRes iterates through the steps of the
(truncated) trace. For each step, it asks checkDigs
to check if there is a nu -1 resilience trace
starting with a configuration
resulting from applying an update to configuration
of the given step, keeping the other resilience
parameters the same. (checkDigs iterates over all possibly updates to a given step state.)  The
(nu-1,a,b) check recursively invokes isAbNRes.

To enumerate the possible update applications
Maude's strategy languge is used to restrict
rewrites to those that apply an update rule
(via the function metaSRewrite).  

---------- files with modules defined ---------

base.maude
 NAT-INF  --- adds infty to the sort Nat
 ID   
--------------------
 COMFIG 
   defines configurations (sort Config) as (multi) 
   sets of actors and messages
   actor terms have the form [oid : cid | attrs]
     oid -- a unique identifier
     cid -- a class identifier
     attrs -- the attributes giving the actors state
     
--------------------
 ITIN 
  defines links and itineraries (sequences of
  links).  A link has the form  
    l(src,tgt,ltype,dur) 
   dur is time to traverse
   src,tgt are identifiers of the link endpoints    

--------------------
 MSG -- the structure of messages
  m(tgt,src,content) 
      -- ordinary messages, delivered immediately
  m(tgt,src,package)
      -- packages that take time to deliver

--------------------
data.maude
  DATA  --- defines data types used in attributes
    and else where
    
--------------------
attributes.maude
  ATTRIBUTES   --- defines attributes encoding
       actor state

--------------------
rules-aux
  RULES-AUX  ---- auxiliary functions used by
     rules to compute changes 

--------------------
rules.maude
  MFG-RULES   --- rules for manufacturer behavio
  CUSTOMER-RULES  --- rules for customer behavio
  SUPPLIER-RULES  --- rules for supplier behavio
  RULES --- collects the actor rules and defines
    the tick rule for passing time

--------------------
digressions.maude
   DIGRESSION  --- data structures specifying
        digressions
   DIGRESSION-RULES
    There is one rule for applying digressions
    It is parameterized by a set of digression
    specifications.  The rule + a digression 
    corresponds to a TMSR update rule.
    
--------------------
sc-test.maude  
  defines initial configurations and goal functions
  for supply chain scenarios.  

--------------------
abres.maude
  ABRES -- defines isAbNRes and its helper functions.
     (independent of supply chain)
  MFG-ABRES-SCENARIO  -- defines initial
   configurations and resilience parameters
   for checking resilience of supply chain scenarios.

--------------- Details ------------------
------- Configurations

*** Messages
Messages are either instanteous (modeling 
voice or electronic communication) or
packages delivering  parts (delivery takes time).

There are two forms of instantaneous message
  m(tgt,src,req(...))   --- a request
  m(tgt,src,rsp(...))   --- a response
tgt,src are identifiers of sender and receiver
actors.  Requets are either product orders or
part orders, each with corresponding response.
Product delivery is also treated as a response.
The ...s stand for request specifie  parameters.
  
There is one form of message carrying parts 
  m(tgt,src,p(partId,orderId,nparts,itin))
The itin argument  is a sequence of links
l(lsrc,ltgt,ltype,dur)  where lsrc/ltgt are the
identifiers of actors at the beginning/end
of the link, ltype is the link type (air,sea,
urban, hiway) and dur is the time remaining
to travers the link.  

*** Actors   
An actor is represented by a term of the form
    [id : cid | attrs ]
Where id the actors unique identifier, cid
is its class, and attrs is a set of attributes
giving the actors state and parameters controlling
its behavior.
There are three classes of actors:
   Mfg (manufacturer),  
   Cust (customer), and
   Supplier (part supplier). 

There are also pseudo actors, simple structures
that carry information controlling the execution:
    time(t) --- holds the current time
    stop(ts) --- the stop time (deadline)
    crit(iscrit?,t0,cdiff,cdur)  --- the critical
      configuration monitor
    di(digs,n) --- specification of possible
      digressions, digs, and upper bound on
      number of applications.
    
Manufacturer Actors have the attributes listed below
  orders(mtO) --- a set of product orders in
         progress.  An order has the form
             o(i,cuId,paId,adur,mparts,idur,id))
      
  asm({... asmId(i),id,d} ...) --- a fixed set
      of assembly lines 0 <= i < k.  id is either
      a product identifier, or the constant noId.
      
  parts(... {partId,n} ...) 
        --- n in the number of partId in the
        --- current inventory 
  profit(pr,penalty) 
      ---- pr accumulated profit
      ---- initially 0
  stock( ... {prodId,n} ... )  
       --- products that have been assembled
       --- but not delivered (speculation or
       --- cancelation)
  cnt(n)  --- used to generate unique part 
        --- order identifiers, initially 0
  partPend( ... pp() ...)
  oh(rate,nparts,t0,cohc,unused) --
        ohc is the cumulative overhead 
        t0 is the last time ohc was updated
        nparts the number of parts in inventory
        or allocated to product orders
        At time t > y0  ohc is updated by
        adding nparts * (t - t0) * rate
   
 Customer Actors have the following attributes:
    ... oQ(mfgId,partId,delay) ... 
       --- product orders to send, 0 or more
    ... w4(mfgId,orderId,prodId,eta,wtime)
       --- product orders sent and not 
       --- yet delivered, 0 or more, eta is the
       --- expected delivery time, wtime is
       --- time since order was confirmed.
    ,., rcvd(mfgId,orderId,prodId,eta,dtime)  
       --- dtime is the actual delivery time
    cnt(j) --- counter used to generate order 
       --- identifiers
    grace(g)  ---


 Part Supplier Actors have two attributes
    ready(delay)  --- delay indicates time until
      parts are available,  used to model events
      such as strikes or supply chain failures.
    pending(msgs)  --- stores parts packages until
      there delay is zero.

-------------------------------  
 Manufacturer Rules 
  [mfgRcvOrder]: handles product orders from a customer
     creates an order data structure, orders parts
     if needed, if no parts are needed, sends a 
     response to the customer with the estimated 
     delivery time
  [mfgRcvCancel]:  handles order cancellation messages
    removes the associated order data
  [mfgRcvPartRsp]: handles part order response from
    a supplier, updates product order data, if all
    arrival times for ordered parts are available
    send response to customer with estiemated delivery
    time.
  [mfgRcvParts]:  handles arrival of ordered parts
    assign the parts to a product order or inventory
    as needed.
  [mfgOrder2Asm]:
     When all parts are available for an order,
     start the assembly process.  
  [mfgAsmDone]:
     when assembly is done, deliver the product to
     the customer, and update the accumulated profit
     with the product profit (subtracting a late penaly
     if the proposed delivery time has passed).


------- Customer Rules
[cuSendO]:  --- used to send a product order requeest 
    when the  delay becomes zero, a corresponding
    w4 attribute  is also created
[cuRcvORsp]:  --- handles response to a product order
   request by updating the corresponding w4 attribute
   with the expected delivery time.
[cuRcvODlv]:  --- handles a product delivery message.
  The corresponding w4 attribute is removed and a
  rcvd attribute is created to record the expected
  and actual delivery times.
    
[cuCancelO]: --- if the waiting time of a w4 attribute
    is more than the expected delivery time by at least
    the grace time, a cancel order request is sent.

------ Supplier Rule
[suReleasePendingO]  --- handles part requests, by
    computing an itinerary and sending the
    resulting package message and a response messag
    indicated the expected arrival time. If the ready
    parameter is greater than zero the package
    message is stored in the pending attribute
    until ready becomes zero.
    

----- Time passing rule
[tick] --- passes time by minimaltime needed
   to enable some rule to fire as computed by
   the function, mte.  Only fires if mte returns
   a nonzero number.
   Time stops if the configuration is critical
   or if advancing would pass the stop time.
   
   Parameters modified by passing time include
     the duration of the first link in a package
     itinerary; supplier ready delay; delay in
     customer oS attributes,  waiting time in
     customer w4 attributes, duration in manufacturer
     asm attribute, waiting time in manufacturer
     order attributes, and manufacturer overhead.
     The time and criticality  monitor elements are
     also updated.

------------   Running  MSC experiments   -----------
[You will need to have Maude installed.  It can be
downloaded from maude.cs.uiuc.edu
To execute commands, start Maude and load the file load.maude.  Specifically,  in the terminal
   cd to the SupplyChainExample directory; 
   type: maude load
This loads all the modules of the specification
leaving you in the module TEST defined in
sc-test.maude

Now you can type commands  for executing and searching starting from MSC system configuratioins (your own or copie from the test files) to the Maude prompt.

Sample commands can be found  it the files described
below.

NB: Initial states need to be System configurations
(sor System) which have the form  { config } where
config is a term of sort Config.  This is because
a term of sort Config can represent all of the
system or just a part.  The {}s say that what is
inside is all of the system state.  This is
required by the tick rule as it needs to see the
full system to determine if time can pass, and
if so how much.

test-base.txt --- commands testing auxiliary functions

sc-runs0.txt --- example executions.  You need to 
use the "set print attribute on"  command
to get the trace of rule instances printed.

sc-prelim.txt  commands for initial exploration
of parameters for isAbNRes.  For this you need to
load the resilience checking specification

maude> load abres

This loads the definition of isAbNRes and parameter
definitions

sc-results1.txt  contains commands systematically exploring resilience parameters for different initial configurations.  See sc-experiments.txt for a table
summarizing the results.

  
%%%%%%%%%%%%%%%%%%  Notes %%%%%%%%%%%%%%%%%%% 
  
isAbNRes is designed to work for any specification
the meets some minimal requirements
 -- basically being a real-time Maude actor
 theory where time is advanced by a tick rule.
 
 

  
