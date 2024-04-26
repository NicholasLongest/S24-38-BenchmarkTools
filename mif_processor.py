import mif
import os
from pathlib import Path
import glob
import fnmatch
import numpy as np
import csv
import subprocess
import shutil

# mif_processor.py
# Produces a .csv file for each board containing the data from the DE1-SoC RAMs stored in .mif files.  

def write_RAMs_to_file(foldername, baseline_bool):

    # Sort PLLs
    PLLs = os.listdir(foldername + '/PLL_RAMs')  
    count = 0
    for pll in PLLs:
        if len(pll) > 6:
            count += 1

    PLLs = PLLs[count:len(PLLs)] + PLLs[0:count]

    # Load Data from PLLs
    data = []
    for pll in PLLs:
        load_PLL(data, pll, foldername)
    
    # Formatting/Writing to the CSV
    rows = []
    pll_count = 0
    for inst in range (len(data)):
        # PLL_#
        if inst % 8 == 0:
            rows.append([PLLs[pll_count]])
            pll_count += 1

        # Creates Row
        row = []
        row.append('')
        row.append('RAM ' + str((inst % 8) + 1))
        row.append('Address')
        for byteNum in range(9, 0, -1):
            row.append('Byte ' + str(byteNum))
        rows.append(row)

        # Print Ram
        for addr in range(len(data[inst])):
            cols = []
            cols.append('')
            cols.append('')
            
            #cols.append('Address ' + str(addr) + ':')
            cols.append(str(addr))
            for byte in range(len(data[inst][addr])):
                cols.append(str(data[inst][addr][byte]))
            rows.append(cols)

    # Writing the CSV
    if (baseline_bool):
        csvfname = foldername + '/Functional_Results_BL.csv'
    else:
        csvfname = foldername + '/Functional_Results.csv'
        
    with open(csvfname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
# Helper Function
def load_PLL(dataStorage, PLLname, foldername):
    p = Path('.')
    for fileNum in range(1, 9):
      filePath = p.joinpath(foldername).joinpath('PLL_RAMs').joinpath(PLLname).joinpath('RAM' + str(fileNum) + '.mif')
      f = open(filePath, 'r')
      width, mem = mif.load(f, packed=True)
      dataStorage.append(mem)
      f.close()

#write_RAMs_to_file("Board_02927_heat/firstTest")