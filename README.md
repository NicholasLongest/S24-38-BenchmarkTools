# S24-38-BenchmarkTools
Benchmarking Tools for the Verification of Microelectronics Protections Technology project.


The given code is to be used with the DE1-SoC Board.

TestScript.py is the script that needs to be run.

When running the script, make sure your computer is connected to a multimeter via ethernet connection, if the meter is not a rigolDM3068, then line 56 of the script should be changed
from rigolDM3608Agilent to whichever is used for your multimeter in python IVI documentation.

There are other parameters from lines 16-28, make sure METER_IP, quartus_path, and powershellPath are all correct.

Frequencies variable on line 26 contains the frequencies that you would like to run for the test, note that the names of the .cdf files are all of the possible frequencies available.

Each test besides the baseline test will have a folder name that corresponds to the date and time that the test was run, feel free to change this folder name after the test has finished running.

Output graphs are stored in the non baseline test folders, make sure that you have run a baseline before running any other tests for that board, or else there will be no data to compare against.
