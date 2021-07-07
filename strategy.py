from itertools import permutations
from itertools import combinations
from random import choice
import itertools
import numpy as np
import pandas as pd
from utils.damage import cardDamage
from servant import *
from tqdm import tqdm
from collections import defaultdict
from operator import itemgetter

class ShowHandStrategy():


    def __init__(self,servants,enemy):

        '''
        最佳的出卡策略

        '''

        self.servants = servants
        self.enemy = enemy
        self.cardMap = {c:s for s in self.servants for c in s.getCards()}
        self.cards = list(self.cardMap.keys())


    def _setCardPermuation(self):

        self.cardPermu = list(permutations(self.cards,3))


    def _setHandCombination(self):

        self.handCombi = list(combinations(self.cards,5))

    def _setCardCombination(self):

        self.cardCombi = list(combinations(self.cards,3))


    def _checkOverlap(self,cards_out,hands):

        '''
        检查是否牌型与出牌有一致的部分
        '''

        out_name = set([c for c in cards_out])
        hands_name = set([c for c in hands])

        return len(out_name.intersection(hands_name))==len(out_name)


    def _mapCardHand(self):

        '''
        建立出卡和发牌之间的关联

        '''
        self.permu2combi = defaultdict(list)
        self.combi2permu = defaultdict(list)
        
        print('开始构建牌型与出牌的关系')

        for combi in tqdm(self.handCombi):

            for permu in self.cardPermu:

                if self._checkOverlap(permu,combi):

                    self.permu2combi[permu].append(sorted(combi,key=lambda x:id(x)))  
                    self.combi2permu[tuple(sorted(combi,key=lambda x:id(x)))].append(permu)

    def _permuteDmg(self,thresh:int):

        solution = defaultdict(list)

        thresh = self.enemy.hp*thresh

        for s in self.cardPermu:

            total = []

            init_red = s[0].type == 'b'
            
            servants = set()

            for idx,c in enumerate(list(s)):

                total.append(cardDamage(self.cardMap[c],c,idx,self.enemy,False,init_red))

                servants.add(self.cardMap[c])

            if len(servants)==1:

                ex_card = Card('ex',list(servants)[0].name,'x',0)

                total.append(cardDamage(list(servants)[0],ex_card,3,self.enemy,False,init_red))

            if np.array(total).sum()>=thresh:

                solution[s] = total
        
        return solution

    def  strategize(self,stars,thresh_type='naive',bet=5 ,topK=1):

        '''
        returns the strategy function that gives card out
        
        thresh_type: 计算斩杀血线的阈值，筛选出合适的出卡，具体类型如下

        - naive: 有多少星星就按照血量*(1-星星数/100)
        - aggressive: 血量*0.5
        - conservative: 血量本身

        bet: 赌狗模式，一旦有X颗星星大于此值，则认为此张牌会暴击

        - 若thresh_type为conservative，则bet = 9
        - 若thresh_type为aggressive，则bet = 1
        

        topK: 默认打出的是每次发牌当中的最高估计伤害的牌，如果不为1则从topK 当中随机打出

        
        '''
        if thresh_type == 'naive':

            thresh = (1-stars/100)

        elif thresh_type == 'aggressive':

            thresh = 0.5
            bet = 1

        elif thresh_type == 'conservative':

            thresh = 1
            bet = 9

        # 预测出一系列可以打出伤害的方案
        solution = self._permuteDmg(thresh)

        def strategy(cards,card_stars,bet=bet,topK=topK):

            # 对于拿到的手的牌型,索引其能产生成排列
            cardsAtHand = self.combi2permu[tuple(sorted(cards,key=lambda x:id(x)))]

            starMap = dict(zip(cards,card_stars))

            solutionWithBet = defaultdict(int)

            # 对于到手的三张牌,即一个确定的排列
            for c in cardsAtHand:
            
                ttdmg = 0

                # dmg 为一个伤害列表
                dmg  = solution[c]
                
                if len(dmg)==0:

                    continue

                # 赌狗根据暴击星数量选择出卡
                stars = [starMap[card]>bet for card in c]
                crits = [card.buff['c'] for card in c]

                if len(dmg)==4:

                    # EX卡绝对不暴击

                    stars.append(False)
                    crits.append(1)

                ttdmg = np.sum(np.array(dmg)*(1+np.array(stars)*np.array(crits)))

                solutionWithBet.update({c:ttdmg})
            
            sorted_bet = sorted(solutionWithBet.items(), key=itemgetter(1),reverse=True)[:topK]
            
            # print('可打:',sorted_bet)
            
            try:

                return choice(sorted_bet)[0]
            
            except IndexError:

                # 如果没有合理的暴击机会就xjb出牌

                # print('无牌可打')

                return choice(cardsAtHand)

        return strategy


    def initialize(self):

        '''
        封装一下前面的函数

        '''
        print('初始化所有卡序')
        self._setCardPermuation()

        print('初始化所有牌型')
        self._setHandCombination()

        self._mapCardHand()






    
                



