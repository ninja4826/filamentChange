
import sys
import re
import os

sourceFile = sys.argv[1]

travelSpeed = 0

zSpeed = 0

f = open(sourceFile, "r")
line = f.read()
if not re.search('^M600', line, re.MULTILINE):
    print('M600 not found')
    f.close()
    sys.exit()

print('M600 found')
f.close()

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
f.close()
destFile = re.sub('\.gcode$', '', sourceFile)
os.rename(sourceFile, destFile+'.filamentChange.bak')
destFile = re.sub('\.gcode$', '', sourceFile)
destFile = destFile + '.gcode'

with open(destFile, "w") as of:
    for lIndex in list(range(len(lines))):
        oline = lines[lIndex]
        parts = oline.split(';', 1)
        if len(parts) > 1:
            # print(parts)
            comment = parts[1].strip()
            if comment:
                stringMatch = re.search('^travel_speed\s=\s([+-]?(?:\d*\.)?\d+)', comment)
                if stringMatch:
                    travelSpeed = float(stringMatch.group(1)) * 48
                    print('found travel speed: '+str(travelSpeed))
                stringMatch = re.search('^machine_max_feedrate_z\s=\s([+-]?(?:\d*\.)?\d+)', comment)
                if stringMatch:
                    zSpeed = float(stringMatch.group(1)) * 60
                    print('found z speed: '+str(zSpeed))

    for lIndex in list(range(len(lines))):
        oline = lines[lIndex]
        # Parse gcode line
        parts = oline.split(';', 1)
        if len(parts) > 1:
            comment = parts[1].strip()
            if comment:
                stringMatch = re.search('^Z:([+-]?(?:\d*\.)?\d+)', comment)
                if stringMatch:
                    currZ = float(stringMatch.group(1))
        if len(parts) > 0:
            # Parse command
            command = parts[0].strip()

            if command:
                stringMatch = re.search('^M600', command)
                if stringMatch:
                    # Insert code for filament change
                    of.write('; post processing script : filamentChange.py\n')
                    of.write("; most code comes from Cura's PauseAtHeight.py script" + '\n')
                    of.write('G1 F'+str(travelSpeed)+' ; set travel speed\n')
                    of.write('G1 X0 Y0\n')
                    if currZ < 15:
                        of.write('G1 Z15 ; too close to bed--move to at least 15mm\n')
                    of.write('M104 S190 ; standby temperature\n')
                    of.write('M600 R190 ; Do the actual filament change\n')
                    of.write('G28 X0 Y0 ; Home X and Y\n')
                    of.write('M109 S190 ; resume temperature\n')
                else:
                    of.write(oline)
            else:
                of.write(oline)
            
            # Write the original line
            # of.write(oline)
of.close()