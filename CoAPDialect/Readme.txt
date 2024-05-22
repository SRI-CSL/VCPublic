NB: This README is a work in progress
--------------------------------------------
These files implement the CoAP messaging specification
(RFC7252), active and reactive attack models, and a
generic dialect transformation that mitigates reactive
attacks.  (See the paper arXiv....)

Files
-----------
The CoAP messaging specification
-----------
  coap-msg.maude  --- message data types
  coap-conf.maude --- configuration data types, functions
  coap-time.maude  --- time model and defn of mte
  coap-rule-aux.maude --- functions for sending/receiving
                     --- messages, used in send/rcv rules
  coap-rules.maude  --- rules to send/receive messages
                        and pass time

-----------
Specification of attacker capabilities and semantics
-----------
  coap-attacker.maude  -- active and reactive capabilities
    --- specific attacks: drop, delay, redirect message 
    --- generic multi-action capability
 
-----------
Specification of CoAP dialect functions and transform
-----------
 coap-dialect.maude  --- rules for dialect wrapper
                     --- withh one family of lingos 
 
-----------
Test scenario definitions
-----------
  coap-test.maude  
    --- 2 or 3 coap endpoint scenarios 
    --- application message constructors, 
    --- definitions of properties characterizing attacks

coap-dialect-test.maude 
   --- defines functions D,UD mapping CoAP scenarios to 
       dialected form and vice-versa
   --- These functions can be used to lift CoAP scenarios
       and analyses (rew, search) to dialected systems.

You can use the the functions in the test files to define
and execution your own tests.   

-----------
Test runs and case studies
-----------
coap-test-runs.txt
coap-dialect-test-runs.txt
  --- files containing sample output of test commands
  --- these are tests to see if the execution or
  --- search proceeds as expected  
  --- each entry begins with a rew or search command
     (possibly preceeded by a command to set print 
     attribute on/off) followed by the maude output.
  --- tests are separated by a row of *s  

coap-attacks-scenarios.maude
coap-attacks-dialected-scenarios.maude
coap-reactive-attacker-scenarios.maude
   
coap-reactive-attacker-scenarios-dialected.maude

---------------------------------------
Files for loading 
---------------------
load.maude  --- loads CoAP framework and scenario generators
dload.maude --- adds dialect modules and transforms
rsload.maude --- loads 
drsload.maude

*******************************************************
To repeat the tests in coap-test-runs.txt, in a
terminal window type the folloing

maude load

To repeat the tests in coap-dialect-test-runs.txt, in a
terminal window type the following

maude dload

Then copy paste a test command into the Maude prompt.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%









%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Some implementation notes 
See technical report for more details.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

******** attributes holding device state
--------------------------------------------------------   
--------------
Attributes to track status of msgs sent/rcvd
in order to implement the rules for reliability 
(confirmable messages) and deduplication.
-----------------
w4Ack(dmsgs) --- waiting for response to CON request
w4Rsp(msgs)  --- waiting for response to NON request
             or CON request where ACK has been received
rspRcd(msgs) --- log reponses received to avoid reprocessing
rspSntD(dmsgs) --- log responses sent in case lost
       --- time component used to determine if
       --- msg token are still valid

op rsrcs : RMap -> Attr [ctor] . --- server resource state

op ctr : Nat -> Attr [ctor] .  --- for generating fresh stuff

op sendReqs : AMsgL -> Attr [ctor] . --- models app input

op config : CBnds -> Attr [ctor] .  
    --- global parameters such as max resends, 
    --- delay between resends etc. 

op toSend : DMsg -> Attr [ctor] . 
    --- used to store messages to send

op kb : DMsgS -> Attr [ctor] . --- attacker knowledge
op caps : Caps -> Attr [ctor] . --- attaker capabilities

op conf : Conf -> Attr [ctor] .  --- for dialect stated
op toLog : LogItemL -> Attr [ctor] .  
  --- holds information to be placed in the global log
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
----------------------------------------------------
Summary of rules for sending/receiving messages,
maintining w4 and rsp state and handling duplicates
----------------------------------------------------

send CON req  record w4Ack(msg@d)
send NON req record w4Rsp(msg)
send CON mt  record w4Ack(msg@d)

rcv empty ack from dst for mid, 
    if (no matching w4) ignore
    ow drop the matching w4ack element, post w4rsp(msg)

rcv ack with response from dst for tok (and mid)
    if have matching w4ack
        drop the matching w4Ack element, process the resp; post rcdRsp(dst,tok)
     ow ignore (already received or never asked)
rcv rsp from dst w mid,tok
   if matching w4ack or matching w4rsp 
   then cancel w4; process resp; post rcdRsp(dst,mid,tok)
        if rsp is CON then send matching ack
    ow if rsp is CON 
      if matches a previous req (rcdRsp) then ack      
      ow send RST
      
rcv mt CON reply w matching mt RST ; no other action
rcv mt RST
    if matching w4ack or w4rsp then cancel w4 
        and post rspRcd((dst,tok,RST ))
       (if the match is a req report to app
       (if the match is a ping --- schedule next ping? or)
       
rcv req (src,mid,tok) 
    if already responded 
         (have matching rspSnt(msg) src=msg.dst, match tok
    then if CON then resend msg else ignore fi
    else process the request, post rspSnt
    
    
rcv ill formed msg 
if CON then send matching reset 
  in anycase drop wo further processing

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Rules related duplicate detection

rcv NON req mid tok  mid not in seen
  respond NON rmid tok
  respond CON rmid tok; w4 ack

rcv NON req mid tok  mid  in seen
  ignore (assuming already processed)
   

rcv CON req mid tok  mid not seen
  respond ACK/RSP  
  or
  respond ACK mid mt
  send RSP CON rmid tok w4 ack
  
rcv CON req mid tok  mid  seen
  resend ACK (of either sort) do not reprocess

rcv NON rsp rmid tok
   if have matching w4rsp, discharge and process
   ow ignore

rcv CON rsp rmid tok
   if have matching w4rsp, discharge
   send ack and process
   if have matching rspRcd resend ack
   ow ignore

