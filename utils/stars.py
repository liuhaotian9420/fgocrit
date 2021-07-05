import math
import numpy as np
import pandas as pd
from random import choice
from copy import deepcopy

from collections import Counter

rand_weight = [50,20,20,0,0]
init_cards = 5

# assign stars to different cards

def assignWeight(card_weights,rand_weights):
    global init_cards
    
    true_weights = []
    rweights = deepcopy(rand_weights)
    
    for i in range(init_cards):
    
        r = choice(rweights)
        true_weights.append(r + card_weights[i])
    
        try:
            rweights.pop(rweights.index(r))
    
        except:
    
            continue

    return true_weights/(np.array(true_weights).sum())

# assign stars given weight
def assignStars(stars,weights):

    card_stars = np.zeros(len(weights))
    stars_weights = np.random.rand(stars)
    
    assert sum(weights)>0.99,'incorrect weights'
    
    cum_weights = np.cumsum(weights)
    
    for s in stars_weights:

        # for any given star assign it to a card when equal, assign it to the next star
        
        tens = np.where(card_stars<10)[0]
        card_stars[tens[(s < cum_weights).sum()-1]]+=1
        
        # if a card already has 10 stars, ignore it
        # and assign stars based on remaining weights
        
        new_weights = (card_stars < 10)*weights
        
        if new_weights.sum()== 0:
        
            continue
        
        cum_weights = np.cumsum(new_weights/new_weights.sum())*(card_stars < 10)
        
    assert card_stars.sum() == stars,'有星星未被分配'
    assert (card_stars<=10).all(),'暴击星数量大于10'

    return card_stars