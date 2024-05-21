--------------------------------------------
Files

The CoAP messaging specification
  coap-msg.maude  --- message data types
  coap-conf.maude --- configuration data types and functions
  coap-time.maude  --- time model and defn of mte
  coap-rule-aux.maude --- functions for sending/receiving
                          messages, used in the send/rcv rules
  coap-rules.maude  --- rules to send/receive messages
                        and pass time

Specification of attacker capabilities and semantics
  coap-attacker.maude  -- active and reactive capabilities
     --- specific attacks: drop, delay, or redirect a message 
     --- generic multi-action capability
 
Test scenario definitions
  coap-test.maude  
    2  or 3 coap endpoint scenarios without and with attacker
    application message constructors, 
    definitions of properties to use in searches for attacks.

     
coap-dialect.maude  --- rules for dialect wrapper
                    --- withh one family of lingos 
coap-dialect-test.maude 
   --- scenario using the dialect
   coap-test scenarios for dialected coap endpoints


The files coap-test.maude and coap-dialect-test.maude
contain definitions of initial system configuration
constructors, a collection of applcation messages to
select from, and some properties of target search
states. You 
can use these to define and execution your
own tests


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load.maude  --- loads CoAP framework and scenario generators
dload.maude  --- adds dialect modules and scenario generators

coap-test-runs.txt  
coap-dialect-test-runs.txt
  --- files containing sample output of test commands
  --- these are tests to see if the execution proceeds
      as expected  
  --- each entry begins with a rew or search command
  (possibly preceeded by a set attributes command) 
  followed by the maude output.
  --- tests are separated by a row of *s  

To repeat the tests in coap-test-runs.txt, in a
terminal window type the folloing

maude load

To repeat the tests in coap-dialect-test-runs.txt, in a
terminal window type the following

maude dload

Then copy paste a test command into the Maude prompt.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The file dialect-scenario-runs.txt contains the
commands and output summary for the experiment set
discussed in the tech report section 6,(which describes
the messages, attacks, and goals).

The a few of the commands are rewrites just to see
a sample execution.

The remaining tests are reachability analyses with
attacker. They consist of three searches using plain
CoAP: (1) search for one way the attacker can achieve
its goal; (2) search for all the ways the attacker can
reach its goal; (3) search for all the ways the
attacker uses its capabilities but the underlying coap
goal is achieved. (2) and (3) are repeated for the
dialected system.

In each case, the command and a summary of output are recorded. Examples are separated by a row of %s.
You can try repeating these by 

maude dload

and copy pasting command into the Maude prompt.
You can also make you own test by changing the
application message lists and server initial resources.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Some implementation notes -- see technical report for
more details
--------------------------------------------------------   
******** attributes holding device state
--------------------------------------------------------   
attributes to track status of msgs sent/rcvd
in order to implement the rules for reliability (confirmable
messages) and deduplication.

w4Ack(dmsgs) --- waiting for response to CON request
w4Rsp(msgs)  --- waiting for response to NON request
             or CON request where ACK has been received
rspRcd(msgs) --- log reponses received to avoid reprocessing
rspSnt(msgs) --- log responses sent in case lost

Note the untimed messages could have a timer to implement
LIFETIME of mids and ack to model resource limitation on
number of available ids.


op rsrcs : RMap -> Attr [ctor] . --- server resource state
op ctr : Nat -> Attr [ctor] .  --- for generating fresh stuff
op sendReqs : AMsgL -> Attr [ctor] .  --- modeling app input
op config : CBnds -> Attr [ctor] .  
    --- global parameters such as max resends, delay between
    --- resends ....

op toSend : DMsg -> Attr [ctor] . 
    --- used to store messages to send

op toApp : ABnds -> Attr [ctor] . --- reporting to App

op kb : DMsgS -> Attr [ctor] . --- attacker knowledge
op caps : Caps -> Attr [ctor] . --- attaker capabilities

op conf : Conf -> Attr [ctor] .  --- for dialect stated
   
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

