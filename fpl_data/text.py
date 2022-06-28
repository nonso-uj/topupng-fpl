referrals = ['abc', 1, 2, 1, 3, 4, 1, 2, 'abc', 3, 2, 1]
dct = {}
for r in referrals:
    if r in dct:
        dct[r] += 1
    else:
        dct[r] = 1

print(dct)