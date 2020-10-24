"""
This class create an object for a user who owns several credit card accounts
"""

import pandas as pd
from collections import OrderedDict 
from dateutil.relativedelta import *
from Card import Card

"""
States: month (int), ordered dict of cards opened (0/1), and transaction category
Actions: tuple of open new card, apply transaction to card
"""


class User(object):
    def __init__(self, card_dict, trans_info):
        
        self.card_dict = card_dict
        self.state = OrderedDict()
        for card in self.card_dict:
            self.state[card['card']] = 0
            
        self.trans_idx = 0
        self.trans_info = trans_info
        self.cur_trans_cat = self.trans_info.iloc[self.trans_idx]['category']
        self.cur_trans_amt = self.trans_info.iloc[self.trans_idx]['amount']        
        self.state['month'] = self.trans_info.iloc[self.trans_idx]['month']    
        
        # states
        self.state['category'] = self.cur_trans_cat
        
        # cards
        self.cards = {}
        
        self.done = False
        
        # actions
        # open a card and assign spend to a card


    def next_possible_actions(self):
        # possible cards to open
        cards_to_open = []
        # possible cards to apply spend to
        cards_to_spend = []
        for c in self.state.keys():
            if c != 'category' and c!= 'month':
                if self.state[c] == 0:
                    cards_to_open.append(c)
                else:
                    cards_to_spend.append(c)
                    
        possible_actions = []
        for o in cards_to_open:
            for s in cards_to_spend:
                possible_actions.append((o, s))
            # include spending on card we just opened
            possible_actions.append((o, o))
        
        # include spending on card without opening new one
        for s in cards_to_spend:
            possible_actions.append(('', s))
            
        return possible_actions
        
        
    def step(self, action):
        # if opened a new account
        if action[0] != '':
            opened_card = action[0]
            # add card to card list
            opened_card_dict = None
            for c in self.card_dict:
                if c['card'] == opened_card:
                    opened_card_dict = c
            self.cards[opened_card] = Card(opened_card_dict, self.state['month'])
            # add card to state
            self.state[opened_card] = 1
        
        # assign spend to account
        card_to_spend = action[1]
        reward = self.cards[card_to_spend].apply_transactions({'category':self.state['category'], 'amount':self.cur_trans_amt}, self.state['month'])
        
        # calculate AMFs
        amfs = 0
        for c in self.cards:
            amfs += self.cards[c].calc_amf(self.state['month'])
  
        # get next observation
        self.trans_idx += 1
        if self.trans_idx >= len(self.trans_info):
            self.cur_trans_cat = None
            self.cur_trans_amt = None
            self.done = True
        else:
            self.cur_trans_cat = self.trans_info.iloc[self.trans_idx]['category']
            self.cur_trans_amt = self.trans_info.iloc[self.trans_idx]['amount']  
            self.state['month'] = self.trans_info.iloc[self.trans_idx]['month']  
        self.state['category'] = self.cur_trans_cat
        
        return (self.state, reward + amfs, self.done)
        
            
            
        
        
        
    # mirror after blackjack class.  but i think i'll need a definiton of all possible states, and a next possible states move, and list of all possible actions (combo of opening cards and assigning spend to each one)