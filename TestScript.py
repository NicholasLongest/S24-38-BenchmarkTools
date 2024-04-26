import subprocess
from pathlib import Path
import csv
import time
import ivi
import sys
from datetime import datetime
import os

# VBA
import xlwings as xw

# MIFS
import mif_processor as mif

powershellPath = 'C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe'

# Code will output the voltage readings to a csv file with this name
voltage_filename = "voltageReadings.csv"

time_per_test = 120 # Time between tests in seconds

# NOTE: MAKE SURE AUTOIP IS ON IN THE MULTIMETER
METER_IP = "169.254.196.11"

frequencies = ["115", "120", "125", "130", "135", "140", "145", "150", "155", "160", "165", "170", "175", "180", "185"] #["60", "70", "80", "90", "100", "125", "150", "155", "160", "165"]

quartus_path = '\intelFPGA_lite\\23.1std\quartus\\bin64\\'

# ------------------------- END PARAMS ----------------------------

board_number = input("Enter the Board Number: ")

board_ID = "Board_" + str(board_number)

if(not os.path.exists(board_ID)):
    subprocess.run("mkdir " + board_ID)

if(input("Is this test a baseline? (y/n): ").lower() == "y"):
    baseline = True
    print("BASELINE TEST")
else:
    baseline = False
    print("NON-BASELINE TEST")

# ----------- Following code connects to multimeter through LAN connection -------------

tries = 0
max_tries = 10 # How many times the program will try to connect to the multimeter before exiting

not_connected = 1
while not_connected:
    try:
        # rigolDM3068 is the version of multimeter we are using, if using another find the correct Agilent
            # to use in python-ivi documentation
        meter = ivi.rigol.rigolDM3068Agilent("TCPIP0::"+METER_IP+"::INSTR")
        not_connected = 0
    except:
        tries += 1
        if tries == max_tries:
            print("Exiting program, error connecting")
            sys.exit()
        print("Failure to connect, trying again in 5 seconds. ("+str(tries)+"/"+str(max_tries)+")")
        time.sleep(5)

# ------------ END CONNECTING TO MULTIMETER ---------------

# ------------ FOLDERS ---------------------
if (baseline):
    folderName = "./" + board_ID + "/Baseline"
    if(os.path.exists(folderName)):
        subprocess.run("rm -r " + folderName)
else:
    date = datetime.today()
    year, month, day = str(date.year), str(date.month), str(date.day)
    clock = [str(date.hour), str(date.minute), str(date.second)]

    for i in range(3):
        if len(clock[i]) == 1:
            clock[i] = "0" + clock[i]

    dateString = month + "-" + day + "-" + year + "_;_" + clock[0] + ";" + clock[1] + ";" + clock[2]
    folderName = "./" + board_ID + "/" + dateString

subprocess.run("mkdir " + folderName)

folderName2 = folderName + "/PLL_RAMs"
subprocess.run("mkdir " + folderName2)
# ------------------- END FOLDERS -------------------------

count_dup = 0
lastFreq = "DIFFERENT"
csvList = list()
for frequency in frequencies:

    if lastFreq == frequency:
        count_dup += 1
    else:
        count_dup = 0

    folderName3 = folderName2 + "/PLL_" + frequency
    if count_dup:
        folderName3 += "_" + str(count_dup + 1)

    subprocess.run("mkdir " + folderName3)


    testFile = frequency + "MHz"

    # If the last frequency flashed is the same, do not reflash the board
    if not count_dup:
        print("Flashing test: " + testFile)
        subprocess.run(quartus_path + "quartus_pgm -c \"DE-SoC [USB-1]\" " + testFile + ".cdf")
        print ("Done Flashing")
    else:
        print("\"Flashing\"")
    
    voltageList = list()
    timeList = list()
    start_time = time.time() # time.time + N => N second wait
    while time.time() < start_time + time_per_test:
        
        # Voltage and Time stored in separate Lists
        voltageList.append((meter.measurement.read(1)))
        timeList.append(time.time()-start_time)
        time.sleep(0.1)

        
    minim = str(min(voltageList))
    ave = str(sum(voltageList)/len(voltageList))
    maxim = str(max(voltageList))
    voltageList.insert(0, "Running Voltages:")
    voltageList.insert(0, minim)
    voltageList.insert(0, "Min Voltage")
    voltageList.insert(0, ave)
    voltageList.insert(0, "Average Voltage:")
    voltageList.insert(0, maxim)
    voltageList.insert(0, "Max Voltage:")

    voltageList.insert(0, str(frequency) + "MHz Voltages")

    timeList.insert(0, str(frequency) + "MHz Running Times:")

    csvList.append(voltageList)
    csvList.append(timeList)
    
    print("Started TCL Script")

    subprocess.run("C:\\intelFPGA_lite\\23.1std\\quartus\\bin64\\quartus_stp -t " 
                   + "\'C:\\Users\\nicho\\Homework\\Spring_2024\\MDE\\PythonShenanigans\\DE1_Test_Script\\memDump.tcl\'",
                   shell = True,
                   executable=powershellPath)

    for i in range(4):
        subprocess.run("rm ./RAM" + str(i) + ".mif")

    for i in range(8):
        subprocess.run("mv ./RAM" + str(i+4) + ".mif " + folderName3 + "/RAM" + str(i+1) + ".mif")

    lastFreq = frequency


with open (folderName + "/" + voltage_filename, 'w', newline = '') as file:

    writer = csv.writer(file)
    writer.writerows(csvList)

# MIFS
mif.write_RAMs_to_file(folderName, baseline)
# mif.write_RAMs_to_file("Board_02689/Baseline")

# GRAPHS

# wb = xw.Book("./mif_template.xlsm")
if (not baseline):
    wb = xw.Book("./mif_template.xlsm")
    
    voltageMacro = wb.macro("Sheet1.VoltageChart")
    compare60 = wb.macro("Sheet1.compareTo60")
    compare60_BL = wb.macro("Sheet1.compareTo60_BL")
    exportCorrect = wb.macro("Sheet1.exportCorrect")

    voltageMacro("\\" + board_ID + "\Baseline\\", "\\" + folderName + "\\", "VoltageReadings.csv")

    numFrequencies = len(frequencies)
    compare60("\\" + board_ID, "firstTest", numFrequencies)
    compare60_BL("\\" + board_ID, "firstTest", numFrequencies)

    exportCorrect("\\" + folderName)

    wb.save()
    wb.close()

    subprocess.run("cp .\mif_template.xlsm .\\" + folderName + "\processed_data.xlsm")

print("Testing script finished")