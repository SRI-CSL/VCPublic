This Readme describes the organization of the code for checking RTA recoverability properties detailed in the document:
Automating Recoverability Proofs for Cyber-Physical Systems with Runtime Assurance Architectures.

# Description

The code is distributed into three main directories:

- lib contains the main maude files for the Soft-Agents framework. We refer to the VNC 2020 paper below for a detailed explanation of the Maude code.
- lib_py contains the basic python libraries in particular:
  - basic_lib.py contains the machinery to collect and parse information from maude to python, e.g., function printLog collects into arrays important data of agents (speed, acceleration, position) available in the log of the system configuration.
  - maude_z3.py contains the machinery to check the satisfiability of symbolic constraints using the Z3 solver. Whenever a check for satisfiability returns true, the corresponding model is stored in the global variable smt_model.
  - isResilient.py contains the machinery to check whether a scenario is resilient.
- vehicle contains specific libraries, in the sub-directory lib-vehicle, and logical scenarios, in the directory logicalScenarios, related to autonomous vehicles. Examples of logical scenarios are pedestrian crossing and platooning.

# Dependencies

Before using the symbolic soft-agents, be sure to have installed the following tools/software:

- Python version 3.9 or later
- Maude bindings for python: The bindings can be installed by running pip, e.g., pip install maude. For more information, see https://github.com/fadoss/maude-bindings  
- Z3 bindings for python: The bindings can be installed by running pip, e.g., pip install z3-solver. For more information, see https://github.com/z3prover/z3

Soft agents has been tested on Mac using an Intel processor.  
It should work on Windows, but we have not tested it yet.  
Since the Z3 is not available for Mac M1 machines, the symbolic soft-agents does not work natively on it.

# Run Symbolic Soft-Agents by Example

We use as running example the platooning scenario available at the folder vehicle/logicalScenarios/platooning. To run the check for resilience simply:

1. cd vehicle/logicalScenarios/platooning
2. python3 platooning_z3.py

## Examples of Existing Scenarios

For a more detailed explanation of the scenarios, please see the companion paper mentioned on the top of this Readme.

- Vehicle Following: following specifies a scenario with two vehicles, a leader and a ego vehicle that is following the leader.

- Pedestrian Crossing: To run these experiments is similar to the platooning example shown above, but instead running python3 pedestrian_crossing_z3.py in the folder vehicle/logicalScenarios/pedestrian-crossing.
  - noSensorErrors (in folder vehicle/logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors) contains a pedestrian crossing scenario with one pedestrian and an ego vehicle. The ego vehicle detects the pedestrian and the measurement of the pedestrian's position, speed and direction has no errors.

  - errorPeds (in folder vehicle/logicalScenarios/pedestrian-crossing/scenarios/errorPedS) contains a pedestrian crossing scenario with one pedestrian and an ego vehicle. The ego vehicle detects the pedestrian, but the measurement of the direction of the pedestrian is erroneous. The amount of error is specified symbolically.

# Verifying RTA properties of time-sampling adequacy and t-recoverability

In the folder vehicle/rta_paper_experiments there are several example python programs for carrying out  verification. 
There are several sorts of examples:

1. rta_exp_ped_dt_bad* carry out the checking for dt-bad adequacy in pedestrian crossing scenarios. 
2. rta_exp_ped_dt_noskip* carry out the checking of whether the dt does not skip properties in the pedestrian crossing scenario.
3. rta_exp_ped_dt_prec1* carry out the checking for dt-prec1 adequacy in pedestrian crossing scenarios. 
4. rta_exp_ped_no_errors_resilience* carry out the checking for  t-recoverability for the pedestrian crossing scenarios.
5. rta_exp_ped_errors* carry out the checking for  t-recoverability for the pedestrian crossing scenarios
   with sensor errors.

There are similar python programs for the vehicle following (marked with platooning).

To execute one of the experiments:

1. Move to the directory vehicle/rta_paper_experiments
cd vehicle/rta_paper_experiments 

2. Run python, for example:
python rta_exp_ped_dt_bad.py 

3. After running the python program a txt file with the experiment results is created with name of the python program followed by the date of when the program was executed. For example, after running the program the file rta_exp_ped_dt_bad-2023-01-16.txt is created. 

In the folder vehicle/rta_paper_experiments/summary-rta-experiments, there is a numbers file (summary-rta-experiments.numbers that you need MacOS Numbers to open) which specifies which scenario corresponds to which python program.
There is a CSV file with the same name and content.
The explanation of the scenarios in these files are are as follows:

1. asysPedXLine(t,safer,safe,bad,dt):  when loaded with load-pedestrian-resilience.maude, then specifies the pedestrian crossing scenario, called pedCrBnds in the paper, with safety properties using the gap safety properties with bounds on the speed and distance; otherwise, when loaded with load-pedestrian.maude, then it is the pedestrian crossing scenario, called pedCross in the paper, without the bounds.  

2. asysPedXLineErrorPedS(t,safer,safe,bad,dt,error): specifies the pedestrian scenario, called pedCrBnds, but with errors on the sensors. 

3. asys(36,basicCond and testBounds0(safer,safe,bad,dt),t): when loaded with file following/load-platooning-manh.maude, specifies the vehicle following scenario, called folGap, using safety properties based on the time gap; otherwise, when loaded with following_RSS/load-platooning-manh.maude, specifies the vehicle following scenarios, called folRSS in the paper, using the RSS properties. 


# Some useful publications

* [Safety Proofs using Symbolic Soft Agents] V. Nigam and C. Talcott. Automating Safety Proofs about Cyber-Physical Systems using Rewriting Modulo SMT. In Rewriting Logic and its Applications (WRLA), 2022.

* [Maude Bindings in Python] R. Rubio. Maude as a library: an efficient all-purpose programming interface. In Rewriting Logic and its Applications (WRLA), 2022.

* [Non-Symbolic Soft Agents Specification of Platooning] Yuri Gil Dantas, Vivek Nigam, and Carolyn Talcott. A Formal Security Assessment Framework for Cooperative Adaptive Cruise Control. In IEEE Vehicular Networking Conference (VNC), 2020. http://nigam.info/docs/vnc20.pdf

# Contact information

For inquiries, bug-report, etc, please do not hesitate to contact:
* Vivek Nigam <vivek.nigam@gmail.com>
* Carolyn Talcott <carolyn.talcott@gmail.com>