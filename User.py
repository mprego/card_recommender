"""
This class create an object for a user who owns several credit card accounts
"""

import pandas as pd

class User(object):
    def __init__(self):
        self.card_accts = {}
        
    # mirror after blackjack class.  but i think i'll need a definiton of all possible states, and a next possible states move, and list of all possible actions (combo of opening cards and assigning spend to each one)