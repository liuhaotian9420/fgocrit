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
        self.cards = [{c:s} for s in self.servants for c in s.getCards()]

    # 发牌
    def _shuffle(self,idx):

        shuffle(self.cards)
        
        turns = [self.cards[0:5],self.cards[5:10],self.cards[10::]]  
        
        return turns[idx]

    # 分星
    def _allocateStars(self,cards):

        global rand_weight
        
        # 暂时不考虑特定色卡集星
        init_weight = [list(servant.values())[0].star_rate for servant in cards]
        
        init_star = self.stars
        
        return assignStars(init_star,assignWeight(init_weight,rand_weight))
    
    # 暴击测试
    def _crits(self,stars,rands):

        return rands<=stars/10    



    # 出牌,反馈是否击杀
    def showHand(self,func,cards):

        rands = itertools.islice(self.gen,5)
        
        turn = self._shuffle(0)
        stars = self._allocateStars(turn)
        
        crits = self._crits(stars,rands)

        # 经过func选出要打出的三张卡

        cards = func(cards,stars)
        
        init_red = list(cards[0].keys())[0].startswith('b')

        total = 0

        for idx,card in enumerate(cards):

            # 随机数种子
            r = (next(self.gen)/5-0.1)+1

            total+=cardDamage(card,idx,self.enemies[0],crits[idx],init_red)*r

        return total>=self.enemies[0].hp





