This is the implementation reported in our submission to FCSD22

On the Formalization and Complexity of Resilience Problems for Cyber-Physical Systems

It is constructed on top of the Soft Agents framework.
Details about the Soft Agent framework, please refer to the paper [1].

You also need to download the Maude engine from [2].

The experiments can be found in the file:

Models/DronesRes/experiments-simple.maude

To load the machinery, just:

  cd Models/DroneRes
  maude load-mp
  Maude> load experiments-simple.maude

Then starting at line 31 of the file experiments-simple.maude, you can run the search commands with the different experiments.

For example:

search [1] {iC(easyTargets,mvHigh,easyDeadline)} =>+ asys:ASystem such that not goalAchieved(easyDeadline,asys:ASystem) .

checks the resilience property an UAV carry out an easy mission, with easy deadline when there is a single update mvH.


[1] Carolyn Talcott, Vivek Nigam, Farhad Arbab, and Tobias Kappé. Formal specification and analysis of robust adaptive distributed cyber-physical systems. In Marco Bernardo, Rocco De Nicola, and Jane Hillston, editors,Formal Methods for the Quantitative Evaluation of Collective Adaptive Systems, LNCS. Springer, 2016. 16th edition in the series of Schools on Formal Methods (SFM), Bertinoro (Italy), 20-24 June 2016

[2] http://maude.cs.illinois.edu/w/index.php/The_Maude_System
