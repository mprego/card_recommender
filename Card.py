"""
This class create an object for a credit card and returns rewards based on actions
"""

import pandas as pd

class Card(object):
    def __init__(self, card_dict, open_month):
        self.name = card_dict['card']
        
        self.rewards_curr = card_dict['rewards']['currency']
        self.rewards_base = card_dict['rewards']['base_rate']
        if 'categories' in card_dict['rewards'].keys():
            self.rewards_cat = card_dict['rewards']['categories']
        else:
            self.rewards_cat = {}
        if self.rewards_curr == 'chase':
            self.rewards_conversion = .01
        else:
            self.rewards_conversion = 1
        
        if 'esb' in card_dict.keys():
            self.esb_months = card_dict['esb']['months']
            self.esb_spend = card_dict['esb']['spend']
            self.esb_reward = card_dict['esb']['reward']        
            self.esb_currency = card_dict['esb']['currency']
        else:
            self.esb_months = 0
            self.esb_spend = 0
            self.esb_reward = 0
            self.esb_currency = 'cash'
        if self.esb_currency == 'chase':
            self.esb_conversion = .01
        else:
            self.esb_conversion = 1
        
        if 'amf' in card_dict.keys():
            self.amf_amount = card_dict['amf']['amount']
            self.amf_waive = card_dict['amf']['first year waive']  
        else:
            self.amf_amount = 0
            self.amf_waive = False
        
        if 'credits' in card_dict.keys():
            self.credits_cat = card_dict['credits']
        else:
            self.credits_cat = {}
            
        self.open_month = pd.to_datetime(open_month)
        
    def calc_rewards(self, trans_dict):
        trans_amount = trans_dict['amount']
        
        # if credit category exists
        if trans_dict['category'] in self.credits_cat.keys():
            credits_used = min(trans_amount, self.credits_cat[trans_dict['category']])
            self.credits_cat[trans_dict['category']] -= credits_used
            trans_amount -= credits_used
            
        # if reward category exists
        if trans_dict['category'] in self.rewards_cat.keys():
            rewards = self.rewards_cat[trans_dict['category']] * trans_amount * self.rewards_conversion
            return rewards - trans_amount
        else:
            rewards = self.rewards_base * trans_amount * self.rewards_conversion
            return rewards - trans_amount

    def apply_to_esb(self, trans_dict, curr_month):
        # if esb promotion is still happening
        if int((pd.to_datetime(curr_month) - self.open_month).days/30) <=self.esb_months:
            spend_used = min(self.esb_spend, trans_dict['amount'])
            self.esb_spend = max(0, self.esb_spend - spend_used)
            # if we've met the esb spend threshold'
            if self.esb_spend == 0:
                reward = self.esb_reward * self.esb_conversion
                self.esb_reward = 0
                return reward
            else:
                return 0
        return 0
            
    def calc_amf(self, curr_month):
        # if it's an anniversary
        if pd.to_datetime(curr_month).month == self.open_month.month:
            # if it's the first year and it's waivable
            if pd.to_datetime(curr_month).year == self.open_month.year and self.amf_waive:
                return 0
            else:
                return -1 * self.amf_amount
            
    def apply_transactions(self, trans_dict, curr_month):
        payment = 0
        payment += self.calc_amf(curr_month)
        payment += self.apply_to_esb(trans_dict, curr_month)
        payment += self.calc_rewards(trans_dict)
        return payment
            
            
            
            
            