import random
from Constants import *

class SimulatedUser(object):
    def __init__(self, irrelevant_prob_provide=0.4, irrelevant_prob_confirm=0.2, neg_confirm_prob=0.2):
        self.irrelevant_prob_provide = irrelevant_prob_provide
        self.irrelevant_prob_confirm = irrelevant_prob_confirm
        self.neg_confirm_prob = neg_confirm_prob

    def respond(self, system_action: int) -> int:
        if system_action in {REQUEST_FOOD_TYPE, REQUEST_PRICE, REQUEST_LOCATION}:
            if random.random() < self.irrelevant_prob_provide:
                return IRRELEVANT
            else:
                return action_map[system_action]
        else:
            rand = random.random()
            if rand < self.irrelevant_prob_confirm:
                return IRRELEVANT
            elif rand < self.irrelevant_prob_confirm + self.neg_confirm_prob:
                return action_map[system_action][NEG]   # CONFIRM_NEG_XXXX
            else:
                return action_map[system_action][POS]   # CONFIRM_POS_XXXX




