
weak_relation = ['saber','lancer','archer','mooncancer','avenger','ruler','rider','caster','assassin','alterego']



# 阵营克制 
def campRelation(camp1,camp2,special=False):
    '''
    camp1 对camp2的阵营克职
    '''
    flat = 1
    if not special:
        reverse = abs(camp1-camp2)!=2
        return flat+((camp1 - camp2)/10)*reverse - (1-reverse)*((camp1-camp2)/20) 
    else:
        return flat

# 职介克制
def weakRelation(role1,role2):
    '''
    role 1打role2 的克职系数
    '''
    global weak_relation
    if role2 == 'berserker' and role1 != 'berserker':
        return 2
    if role1 == 'berserker' and role2 != 'foreigner':
       return 1.5

    weak = 1
    r1_index = weak_relation.index(role1)
    r2_index = weak_relation.index(role2)
    
    if role1 == 'alterego':

        return (r2_index//3)/2-0.5+weak

    if  (r1_index//3 != r2_index//3):

        return weak
    
    else:
        # 克职循环内
        rel = r1_index%3-r2_index%3
        if rel == 1 or rel == -2:
            return 0.5
        if rel == -1 or rel == 2:
            return 2
        if rel == 0:
            return 1

