import pandas as pd
from Card import Card

def test_creation():
    card_dict = {'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}
    
    card = Card(card_dict, '2020-01-01')
    assert card.rewards_curr == 'chase'
    assert card.rewards_base == 1
    assert len(card.rewards_cat.keys()) == 2
    assert card.esb_months == 3
    assert card.amf_amount == 550
    assert len(card.credits_cat.keys()) == 1
    
def test_calc_rewards():
    trans_dict = {'category':'dining', 'amount':500}
    
    card_dict = {'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}
    
    card = Card(card_dict, '2020-01-01')    
    payment = card.calc_rewards(trans_dict)    
    assert payment == -485, payment
    
    trans_dict2 = {'category':'travel', 'amount':500}
    payment2 = card.calc_rewards(trans_dict2)
    assert payment2 == -194, payment2
    payment3 = card.calc_rewards(trans_dict2)
    assert payment3 == -485, payment3
    
    
def test_apply_to_esb():
    trans_dict = {'category':'dining', 'amount':5000}
    
    card_dict = {'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}
    
    card = Card(card_dict, '2020-01-01')    
    esb = card.apply_to_esb(trans_dict, '2020-04-01')    
    assert esb == 500, esb
    
def test_calc_amf():
    card_dict = {'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}
    
    card = Card(card_dict, '2020-01-01')   
    amf = card.calc_amf('2020-01-01')
    assert amf == -550, amf
    
def test_apply_transactions():
    card_dict = {'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}
    
    trans_dict = {'category':'dining', 'amount':500}
    
    card = Card(card_dict, '2020-01-01') 
    payment = card.apply_transactions(trans_dict, '2021-01-01')
    
    assert payment == (-485-550), payment
    

test_creation()
test_calc_rewards()
test_apply_to_esb()
test_calc_amf()
test_apply_transactions()                 