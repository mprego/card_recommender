import pandas as pd
from Card import Card
from User import User

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
    
    card = Card(card_dict, 1)
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
    
    card = Card(card_dict, 1)    
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
    
    card = Card(card_dict, 1)    
    esb = card.apply_to_esb(trans_dict, 2)    
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
    
    card = Card(card_dict, 1)   
    amf = card.calc_amf(1)
    assert amf == -550, amf
    
    amf2 = card.calc_amf(13)
    assert amf2 == -550, amf2
    
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
    
    card = Card(card_dict, 1) 
    payment = card.apply_transactions(trans_dict, 13)
    
    assert payment == (-485), payment
    
def test_user_creation():
    card_dict_list = [{'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}, 
                      
                      {'card': 'Chase Sapphire Reserve2',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}]
    
    trans_dict = {'category':'dining', 'amount':500}
    trans_info = pd.DataFrame({'category':['dining'], 'amount':[500], 'month':[0]})
    user = User(card_dict_list, trans_info)
    
    assert user.state == {'Chase Sapphire Reserve':0, 'Chase Sapphire Reserve2':0, 'month':0, 'category':'dining'}, user.state
    
def test_next_possible_actions():    
    card_dict_list = [{'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}, 
                      
                      {'card': 'Chase Sapphire Reserve2',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}]
    
    trans_dict = {'category':'dining', 'amount':500}
    trans_info = pd.DataFrame({'category':['dining'], 'amount':[500], 'month':[0]})
    user = User(card_dict_list, trans_info)
    
    assert user.next_possible_actions() == [('Chase Sapphire Reserve','Chase Sapphire Reserve'), ('Chase Sapphire Reserve2', 'Chase Sapphire Reserve2')], user.next_possible_actions()
    
    
def test_user_step():
    card_dict_list = [{'card': 'Chase Sapphire Reserve',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}, 
                      
                      {'card': 'Chase Sapphire Reserve2',
                 'rewards': {'currency': 'chase', 
                             'base_rate': 1,
                             'categories': {'travel': 3, 'dining': 3}},
                 'esb': {'months': 3,
                         'spend': 4000,
                         'reward': 50000,
                         'currency': 'chase'},
                 'amf': {'amount': 550, 
                         'first year waive': False},
                 'credits': {'travel': 300}}]
    
    trans_dict = {'category':'dining', 'amount':500}
    trans_info = pd.DataFrame({'category':['dining'], 'amount':[500], 'month':[0]})
    user = User(card_dict_list, trans_info)
    
    action = ('Chase Sapphire Reserve', 'Chase Sapphire Reserve')
    step = user.step(action)
    
    assert step[0] == {'Chase Sapphire Reserve':1, 'Chase Sapphire Reserve2':0, 'month':0, 'category':None}, step[0]
    assert step[1] == -485-550, step[1]

    
test_creation()
test_calc_rewards()
test_apply_to_esb()
test_calc_amf()
test_apply_transactions()  
test_user_creation()
test_next_possible_actions()
test_user_step()