from .relations import weakRelation,campRelation

# 指令卡伤害倍率
card_rate = [{'b':1.5,'a':1.0,'q':0.8},
             {'b':1.8,'a':1.2,'q':0.96},
             {'b':2.1,'a':1.4,'q':1.12},
             {'x':1.0}]

class_adjustment = {'saber':1,
           'archer':0.95,
           'lancer':1.05,
           'rider':1,
           'caster':0.9,
           'assassin':0.9,
           'berserker':1.1,
           'ruler':1.1,
           'avenger':1.1,
           'mooncancer':1,
           'alterego':1,
           'foreigner':1}


# 计算单张卡牌伤害
def cardDamage(servant,card,pos,enemy,crit = False, init_red=False):
    
    global card_rate
    global class_adjustment

    card_type = card.type

    rate = card_rate[pos][card_type]
    
    buffs = servant.getBuff()

    weak = weakRelation(servant.role,enemy.role)
    camp = campRelation(servant.camp,enemy.camp)

    dmg = servant.atk*0.23*(buffs['a'][card_type[0]]+0.5*init_red)*(1+crit)*(1+(buffs['c']-1)*crit)*buffs['b']*weak*class_adjustment[servant.role]*camp*rate
 
    return int(dmg)