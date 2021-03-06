import csv
import sys

import pss
import psqi

# indexes of field names
timestamp = 0
grade = 1
exercise = 31
screen_time = 32
extracurr = 33

# validate cmdline arguments
# i know it's not robust, but i probably shouldn't overengineer this bit
# of code for an AP stats class which only I'll ever run
if len(sys.argv) < 3:
    print("usage: $ python3 score.py input.csv output.csv [--no-print]")
    sys.exit()

if len(sys.argv) == 4 and sys.argv[3] == '--no-print':
    printing = False
else:
    printing = True

# main routine
with open(sys.argv[1], "r") as fin:
    reader = csv.reader(fin)
    next(reader)

    with open(sys.argv[2], "w") as fout:
        writer = csv.writer(fout)

        # write field names
        fout.write("Timestamp,Grade,PSS,PSQI,Exercise,Screen Time,Extracurriculars\n")

        for response in reader:
            pss_score = pss.calc_pss(response)
            psqi_score = psqi.calc_psqi(response, printing)

            if printing:
                print(response[timestamp])
                print("PSS SCORE:  " + str(pss_score))
                print("PSQI SCORE: " + str(psqi_score))
                print("************************************************************")

            row = [
                response[timestamp], response[grade],
                pss_score, psqi_score, response[exercise],
                response[screen_time], response[extracurr]
                ]
            writer.writerow(row)