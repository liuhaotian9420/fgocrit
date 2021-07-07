import itertools
import math
import numpy as np
from random import *
from utils.stars import assignStars,assignWeight
from utils.damage import cardDamage

rand_weight = [50,20,20,0,0]


class Simulator():

    def __init__(self, servants, enemies,stars,gen):

        self.servants = servants
        self.enemies = enemies
        self.stars  = stars
        self.gen = gen
        self.cardMap = {c:s for s in self.servants for c in s.getCards()}
        self.cards = list(self.cardMap.keys())
        self.seed = seed


    # 发牌
    def _shuffle(self,idx):

        seed(int(next(self.gen)*100))
        
        shuffle(self.cards)
        
        turns = [self.cards[0:5],self.cards[5:10],self.cards[10::]]  
        
        return turns[idx]

    # 分星
    def _allocateStars(self,cards):

        global rand_weight
        
        init_weight = [ c.star_rate for c in cards]
        
        init_star = self.stars
        
        return assignStars(init_star,assignWeight(init_weight,rand_weight))
    
    # 暴击测试
    def _crits(self,stars,rands):

        return rands<=stars/10    


    # 出牌,反馈是否击杀
    def showHand(self,func,cards):

        rands = itertools.islice(self.gen,5)
        
        stars = self._allocateStars(cards)
        
        crits = self._crits(stars,np.array(list(rands)))

        # 经过func选出要打出的三张卡

        cards = func(tuple(cards),stars)
        
        init_red = cards[0].type == 'b'

        total = 0

        for idx,card in enumerate(cards):

            # 随机数种子
            r = (round(next(self.gen)/5-0.1,2))+1
           
            # print(card,'暴击?:',crits[idx],'种子:',r,cardDamage(self.cardMap[card],card,idx,self.enemies[0],crits[idx],init_red)*r)

            total+=cardDamage(self.cardMap[card],card,idx,self.enemies[0],crits[idx],init_red)*r

        return total>=self.enemies[0].hp,cards





