from servant import *
from simulator import *
from strategy import *
import numpy as np
from random import *
from collections import defaultdict
from tqdm import tqdm
import pandas as pd

# 创建敌方和己方从者
mon = Enemy('mon','archer',1,67114)
fuliduo = Servant('弗栗多','lancer',1,['b1','a1','a2','q1','q2'],14332)
baiqiang  = Servant('白枪','lancer',1,['b1','b2','a1','q1','q2'],12995)
caber  = Servant('C呆','caster',1,['b1','a1','a2','a3','q1'],12546)

servants = [fuliduo,baiqiang,caber]


#来一手buff
fuliduo._addBuff('b',0.2)
fuliduo._addBuff('b',0.18)
fuliduo._addBuff('a',{'a':0.3})
fuliduo._addBuff('a',{'a':0.08})
fuliduo._addBuff('a',{'q':0.08})
fuliduo._addBuff('a',{'b':0.08})
fuliduo._addBuff('a',{'a':0.5})
fuliduo._addCardStarRate(5,'a')
baiqiang._addBuff('b',0.2)
baiqiang._addBuff('b',0.18)
baiqiang._addBuff('a',{'a':0.08})
baiqiang._addBuff('a',{'q':0.08})
baiqiang._addBuff('a',{'b':0.08})
caber._addBuff('b',0.18)
caber._addBuff('b',0.2)
caber._addBuff('a',{'a':0.08})
caber._addBuff('a',{'q':0.08})
caber._addBuff('a',{'b':0.08})

seed(2021)

# 生成一组的随机数种子
sim = Simulator(servants,[mon],20,(uniform(0,1) for i in range(500000)))

strat = ShowHandStrategy(servants,mon)
strat.initialize()

naive_func = strat.strategize(20)
passTurn = 0
totalDmg = [] 

hand_counter = defaultdict(int)
success_counter=defaultdict(int)

for i in tqdm(range(10000)):
   
   cards = sim._shuffle(0)
   hand_counter[tuple(sorted(cards,key=lambda x:id(x)))]+=1
#    print(cards)
   is_pass,out = sim.showHand(naive_func,cards)
   if is_pass:
       success_counter[tuple(sorted(cards,key=lambda x:id(x)))]+=1
#    print(out,'\n\n')
   passTurn+=is_pass
   if i%500==0 and i!=0:

       totalDmg.append({'simulation_runs':i,'success':passTurn,'rate':passTurn/i*100})

pd.DataFrame(totalDmg).plot(x='simulation_runs',y='rate')