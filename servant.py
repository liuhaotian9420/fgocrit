
import numpy as np
from collections import Counter


star_rate={'saber':100,
           'archer':150,
           'lancer':90,
           'rider':200,
           'caster':50,
           'assassin':100,
           'berserker':10,
           'ruler':100,
           'avenger':30,
           'mooncancer':50,
           'alterego':100,
           'foreigner':150
}

class Card():

    def __init__(self,name:str,owner:str,type:str,star_rate):

        '''
        抽象卡片这个实体，为了应对色卡集星和方便统计

        '''

        self.name = name

        self.owner = owner
        
        self.type = type
        
        self.star_rate = star_rate

        #本身色卡具有的buff
        self.buff = {'a':1,'b':1,'c':1}


    def __repr__(self):

        return self.owner+self.name

    def _addStarrate(self,rate):

        self.star_rate*= rate

    def _setStarrate(self,rate):

        self.star_rate = rate

    def _setBuff(self,buff):

        self.buff = buff






class Servant():

    def __init__(self,name:str,role:str,camp:int,cards:list,atk:int):

        '''
        从者模板
        
        role: 从者职介
        camp: 从者阵营
        cards: 从者配卡
        atk: 从者ATK

        '''

        global star_rate

        assert 'b1' in cards,'无红卡'
        assert 'q1' in cards,'无绿卡'
        assert 'a1' in cards,'无蓝卡'
        assert len(cards)==5,'每个从者5张卡'
        assert cards.count(max(cards,key=cards.count))<=3,'任意一种色卡能超过三张'
        assert role in list(star_rate.keys()),'职介有误'
        assert camp in [-1,0,1],'请加上从者阵营(人，地，天)'

        self.name = name
        self.role = role 

        self.camp = camp
        self.atk = atk

        # A,B,C类三种buff,默认为1
        # 其中A类buff有三种
        self.buff = {'a':{'b':1,'a':1,'q':1,'x':1},'b':1,'c':1}

        # 随机生成一个从者的暴击星集中率
        self.star_rate = star_rate[role]*np.random.uniform(0.97,1.04)

        # 生成角色的卡组
        self.cards = [Card(c,self.name,c[0],self.star_rate) for c in cards]

    def __repr__(self):

        return self.name

    def _setATK(self,atk):

        self.atk = atk

    def _setStarRate(self,rate,card_type = None):

        if card_type:

            self._addCardStarRate(rate,card_type)

        else:

            self.star_rate *= rate
            self._sync()

        
    
    
    def _addCardStarRate(self,rate,card_type):

        for c in self.cards:

            if c.type == card_type:

                c._addStarrate(rate)



    def getBuff(self):

        return self.buff

    def getCards(self):

        return self.cards

    def _addBuff(self,buff_type,buff):

        assert buff_type in ['a','b','c'],'buff类型有误'

        if buff_type == 'a':
        
            assert type(buff)==dict,'请检查buff内容'

            self.buff['a'] = dict(Counter(self.buff['a'])+Counter(buff))

            self._sync()
        
        else:
        
            self.buff[buff_type]+=buff
            
            self._sync()
        

    def _sync(self):

        buffs = self.getBuff()

        for c in self.cards:

            c._setBuff({'a':buffs['a'][c.type],'b':buffs['b'],'c':buffs['c']})
            c._setStarrate(self.star_rate)

# 敌人模板
class Enemy():
   
    def __init__(self,name:str,role:str,camp:int,hp:int):
   
        assert role in list(star_rate.keys()),'职介有误'
        assert camp in [-2,-1,0,1,2],'请加上敌人阵营'
   
        self.role = role
        self.name = name
        self.camp = camp
        self.hp = hp

    def getCamp(self):
        return self.camp

    def getRole(self):
        return self.role
    
    def getHp(self):
        return self.hp

    def setHp(self,hp):
        self.hp = hp