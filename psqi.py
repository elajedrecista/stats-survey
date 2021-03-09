from datetime import datetime

# field indexes
psqi1     = 12
psqi2     = 13
psqi3     = 14
psqi4     = 15
psqi5a    = 16
psqi5b    = 17
psqi5c    = 18
psqi5d    = 19
psqi5e    = 20
psqi5f    = 21
psqi5g    = 22
psqi5h    = 23
psqi5i    = 24
psqi5jcom = 25
psqi5j    = 26
psqi6     = 27
psqi7     = 28
psqi8     = 29
psqi9     = 30

# PSQI response scores
psqi = {
    # Q5,Q7,Q8
    "Not during the past month":0,
    "Less than once a week":1,
    "Once or twice a week":2,
    "Three or more times a week":3,

    # Q6
    "Very good":0,
    "Fairly good":1,
    "Fairly bad":2,
    "Very bad":3,

    # Q9
    "No problem at all":0,
    "Only a very slight problem":1,
    "Somewhat of a problem":2,
    "A very big problem":3
}

def calc_durat(q4):
    tmp = float(q4)
    if tmp >= 7:
        return 0
    elif 6 <= tmp < 7:
        return 1
    elif 5 <= tmp < 6:
        return 2
    elif tmp < 5:
        return 3
    else:
        print(f"ERROR: calc_durat param q4 = {q4}")
        print(f"ERROR: calc_durat var tmp = {tmp}")
        return 2**16

def calc_distb(distb_answers, q5jcom, q5j):
    # not answered
    if q5j == '' or q5jcom == '':
        tmp_q5j = 0
    # was answered, so score the question
    else:
        tmp_q5j = psqi[q5j]

    total = 0
    for answer in distb_answers:
        total += psqi[answer]
    total += tmp_q5j

    if total == 0:
        return 0
    elif 1 <= total <= 9:
        return 1
    elif 9 < total <= 18:
        return 2
    elif total > 18:
        return 3
    else:
        print(f"ERROR: calc_distb var total = {total}")
        return 2**16

def calc_laten(q2, q5a):
    tmp_q2 = float(q2)
    tmp_q5a = int(psqi[q5a])

    if 0 <= tmp_q2 <= 15:
        q2new = 0
    elif 15 < tmp_q2 <= 30:
        q2new = 1
    elif 30 < tmp_q2 <= 60:
        q2new = 2
    elif tmp_q2 > 60:
        q2new = 3
    else:
        print(f"ERROR: calc_laten param q2 = {q2}")
        print(f"ERROR: calc_laten var tmp_q2 = {tmp_q2}")
        return 2**16

    tmp = q2new + tmp_q5a
    if tmp == 0:
        return 0
    elif 1 <= tmp <= 2:
        return 1
    elif 3 <= tmp <= 4:
        return 2
    elif 5 <= tmp <= 6:
        return 3
    else:
        print(f"ERROR: calc_laten var tmp = {tmp}")
        print(f"ERROR: calc_laten var tmp = q2new + tmp_q5a = {q2new} + {tmp_q5a}")
        return 2**16

def calc_daydys(q8, q9):
    tmp = psqi[q8] + psqi[q9]
    if tmp == 0:
        return 0
    elif 1 <= tmp <= 2:
        return 1
    elif 3 <= tmp <= 4:
        return 2
    elif 5 <= tmp <= 6:
        return 3
    else:
        print(f"ERROR: calc_daydys var tmp = {tmp}")
        print(f"ERROR: calc_daydys param q8 = {q8}")
        print(f"ERROR: calc_daydys param q9 = {q9}")
        return 2**16

# Bless this person's heart
# https://stackoverflow.com/a/3096984/13471272
def to_military(time):
    fmt = "%I:%M %p"
    try:
        time = datetime.strptime(time, fmt)
    except ValueError:
        time = datetime.strptime(time, "%I:%M:%S %p")
    return time

def calc_hse(q1, q3, q4):
    q1_time = to_military(q1)
    q3_time = to_military(q3)

    # PSQI scoring does q1 - q3, but because of datetime's quirks,
    # I must do it the other way around
    tdelta = q3_time - q1_time
    diff_sec = tdelta.seconds
    diff_hour = abs(diff_sec) / 3600
    if diff_hour > 24:
        newtib = diff_hour - 24
    elif diff_hour <= 24:
        newtib = diff_hour
    else:
        print(f"ERROR: calc_hse var diff_hour = {diff_hour}")
        return 2**16

    tmphse = (float(q4) / newtib) * 100
    if tmphse >= 85:
        return 0
    elif 75 <= tmphse < 85:
        return 1
    elif 65 <= tmphse < 75:
        return 2
    elif tmphse < 65:
        return 3
    else:
        print(f"ERROR: calc_hse var tmphse = {tmphse}")
        return 2**16

def calc_slpqual_meds(q):
    return psqi[q]

def calc_psqi(response, printing):
    # read in PSQI responses as their original strings
    q1     = response[psqi1].strip()
    q2     = response[psqi2].strip()
    q3     = response[psqi3].strip()
    q4     = response[psqi4].strip()
    q5a    = response[psqi5a].strip()
    q5b    = response[psqi5b].strip()
    q5c    = response[psqi5c].strip()
    q5d    = response[psqi5d].strip()
    q5e    = response[psqi5e].strip()
    q5f    = response[psqi5f].strip()
    q5g    = response[psqi5g].strip()
    q5h    = response[psqi5h].strip()
    q5i    = response[psqi5i].strip()
    q5jcom = response[psqi5jcom].strip()
    q5j    = response[psqi5j].strip()
    q6     = response[psqi6].strip()
    q7     = response[psqi7].strip()
    q8     = response[psqi8].strip()
    q9     = response[psqi9].strip()
    distb_answers = [q5b, q5c, q5d, q5e, q5f, q5g, q5h, q5i]

    durat = calc_durat(q4)
    distb = calc_distb(distb_answers, q5jcom, q5j)
    laten = calc_laten(q2, q5a)
    daydys = calc_daydys(q8, q9)
    hse = calc_hse(q1, q3, q4)
    slpqual = calc_slpqual_meds(q6)
    meds = calc_slpqual_meds(q7)
    psqi_score = durat + distb + laten + daydys + hse + slpqual + meds

    if printing:
        print(f"durat   = {durat:d}")
        print(f"distb   = {distb:d}")
        print(f"laten   = {laten:d}")
        print(f"daydys  = {daydys:d}")
        print(f"hse     = {hse:d}")
        print(f"slpqual = {slpqual:d}")
        print(f"meds    = {meds:d}")
        print(f"PSQI    = {psqi_score:d}")
    return psqi_score
