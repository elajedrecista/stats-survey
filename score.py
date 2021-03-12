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
# i know it's not robust, but i probably shouldn't overengineer
# some code for an AP stats class which only I will ever run
if len(sys.argv) < 3:
    print("usage: $ python3 score.py input.csv output.csv [--no-print]")
    sys.exit()

printing = True
if len(sys.argv) == 4 and sys.argv[3] == '--no-print':
    printing = False

pss_scores = []
psqi_scores = []

# main routine
with open(sys.argv[1], "r", encoding='utf8') as fin:
    reader = csv.reader(fin)
    next(reader)

    with open(sys.argv[2], "w", encoding='utf8') as fout:
        writer = csv.writer(fout)

        # write output field names
        fout.write("Timestamp,Grade,PSS,PSQI,Exercise,Screen Time,Extracurriculars\n")

        print("**************************************")
        for response in reader:
            pss_score = pss.calc_pss(response)
            psqi_score = psqi.calc_psqi(response, printing)

            pss_scores.append(pss_score)
            psqi_scores.append(psqi_score)

            # if printing:
            print('| ' + response[timestamp], end='')
            print(f"  PSS {pss_score:02d}", end='')
            print(f"  PSQI {psqi_score:02d} |")
            print("**************************************")

            row = [
                response[timestamp], response[grade],
                pss_score, psqi_score, response[exercise],
                response[screen_time], response[extracurr]
                ]
            writer.writerow(row)

def mean(ls):
    total = 0
    for n in ls:
        total += n
    return total / len(ls)

print(f"\n\nSCORING COMPLETE.")
print(f"{len(pss_scores):d} SUBJECTS ANALYZED.\n")

print(f"MEAN PSQI  {mean(psqi_scores):.02f}")
print(f"MEAN PSS   {mean(pss_scores):.02f}")
