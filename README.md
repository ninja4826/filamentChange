# PrusaSlicer Filament Change script

This is mostly for personal record keeping, as the script has yet to be parameterized. 

### Currently does the following

1. Reads file to ensure that M600 filament change exists.
2. Gathers information such as travel speed from bottom of file.
3. Sets travel speed.
4. Moves to X0 Y0.
5. Moves to Z15 if head is too close to bed.
6. Sets standby temperature (currently 190).
7. Adds temperature setting to M600 command.
8. Re-Homes X and Y axis.
9. Waits for head to reach 190 degrees.