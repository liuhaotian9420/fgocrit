from itertools import permutations
from itertools import combinations
import itertools
import numpy as np
import pandas as pd
from damage import cardDamage

class ShowHandStrategy():


    def __init__(self,servants,enemy):

        '''
        最佳的出卡策略

        '''

        self.servants = servants
        self.enemy = enemy
        self.cards = [{c:s} for s in self.servants for c in s.getCards()]


    def _setCardPermuation(self):

        self.cardPermu = list(permutations(self.cards,3))


    def _setHandCombination(self):

        self.handCombi = list(combinations(self.cards,5))

    
    def _getCardName(self,card):

        '''
        获得卡片的唯一标识
        '''

        return list(card.values())[0]+list(card.keys())[0]


    def _checkOverlap(self,cards_out,hands):

        '''
        检查是否牌型与出牌有一致的部分
        '''

        out_name = set([self._getCardName(c) for c in cards_out])
        hands_name = set([self._getCardName(c) for c in hands])

        return len(out_name.intersection(hands_name))==len(out_name)




    def _permuteDmg(self,stars):

        solution = []

        thresh = self.enemy*(1-stars/50)

        for s in self.cardPermu:

            total = 0 

            init_red = 'b' in self._getCardName(list(s)[0])

            has_ex = set([list(c.values())[0] for c in cards])

            for idx,c in enumerate(list(s)):

                total += cardDamage(c,idx,self.enemy,False,init_red)

            if len(has_ex)==1:

                total+=cardDamage({'x':list(has_ex)[0]},3,mon,False,init_red)

            if total>=thresh:

                solution.append({"cards":list(s),"damage":total})
                



