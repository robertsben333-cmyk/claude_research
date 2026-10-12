# Q3-26 sales rebuild from J&J's own disclosed lines (Q2-26 level x assumed sequential change), $m
q2 = dict(darz=4207, carv=657, tec=260, tal=174, ryb=289, erl=995, imb=599, onc_other=7406-4207-657-260-174-289-995-599,
          trem=2046, stel=740, simp=618, remi=338, oth_imm=104,
          neuro=2337, ph=1143, id_=763, cvm=889)
seq_lo = dict(darz=0.02, carv=0.05, tec=0.06, tal=0.05, ryb=0.06, erl=0.00, imb=-0.05, onc_other=-0.02,
              trem=0.00, stel=-0.12, simp=-0.04, remi=-0.05, oth_imm=0.40, neuro=0.01, ph=0.0, id_=-0.02, cvm=-0.02)
seq_hi = dict(darz=0.05, carv=0.10, tec=0.12, tal=0.10, ryb=0.12, erl=0.02, imb=-0.03, onc_other=0.0,
              trem=0.08, stel=-0.05, simp=-0.02, remi=-0.02, oth_imm=0.80, neuro=0.04, ph=0.01, id_=0.0, cvm=0.0)
fx_seq_intl = -0.004   # Q3 vs Q2 2026 translation on intl (EUR 1.1632->1.1506, CNY +0.9%, JPY flat), ~40% intl in IM
def im(seq):
    tot = sum(v*(1+seq[k]) for k,v in q2.items())
    return tot*(1+fx_seq_intl*0.4)
im_lo, im_hi = im(seq_lo), im(seq_hi)
# MedTech: Q2-26 8926 x 2025 seasonal Q3/Q2 (8430/8541) x seq FX (intl ~47%); low case adds tougher-comp drag of -1%
mt_mid = 8926*(8430/8541)*(1+fx_seq_intl*0.47)
mt_lo, mt_hi = mt_mid*0.99, mt_mid*1.005
q3_25 = dict(im=15563, mt=8430, tot=23993)
for lab, a, b in [('low', im_lo, mt_lo), ('high', im_hi, mt_hi)]:
    t = a+b
    print(f"{lab}: IM {a:,.0f} ({(a/q3_25['im']-1)*100:+.1f}%)  MT {b:,.0f} ({(b/q3_25['mt']-1)*100:+.1f}%)  total {t:,.0f} ({(t/q3_25['tot']-1)*100:+.1f}%)  vs cons 25,382: {(t/25382-1)*100:+.2f}%")
mid = ((im_lo+im_hi)/2 + mt_mid)
print(f"mid total {mid:,.0f} vs cons {(mid/25382-1)*100:+.2f}%  yoy {(mid/23993-1)*100:+.1f}%")
# Guidance-implied H2 and FX on Q4
H1 = 24062+25310; FYmid=101100; H2=FYmid-H1
print('H1',H1,'H2 implied at guide mid',H2, 'H2-25', 23993+24564, 'H2 growth %.1f%%'%((H2/(23993+24564)-1)*100))
print('Q4 implied if Q3=mid:', FYmid-H1-mid)
eur_q4 = 0.53*0.42*26300  # Europe ~53% of intl, intl ~42% of sales, Q4 ~$26.3bn
print('Q4 Europe sales ~', round(eur_q4), 'FX at 1.116 vs 1.15:', round(eur_q4*(1.116/1.15-1)))
