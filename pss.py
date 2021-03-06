pss1  = 2
pss2  = 3
pss3  = 4
pss4  = 5
pss5  = 6
pss6  = 7
pss7  = 8
pss8  = 9
pss9  = 10
pss10 = 11

def calc_pss(response):
    q1  = int(response[pss1])
    q2  = int(response[pss2])
    q3  = int(response[pss3])
    q4  = 4 - int(response[pss4])
    q5  = 4 - int(response[pss5])
    q6  = int(response[pss6])
    q7  = 4 - int(response[pss7])
    q8  = 4 - int(response[pss8])
    q9  = int(response[pss9])
    q10 = int(response[pss10])

    return q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10
