import collections
import random
import numpy as np
import itertools
from plyer import notification

from Constants import *
from SimulatedUser import *

class DialogManager(object):
    def __init__(self):
        self.data = [None] * NUM_OF_DATA_SLOTS
        self.state = [0] * NUM_OF_STATE_SLOTS
        self.Q_values = collections.defaultdict(lambda: np.zeros(NUM_OF_SYSTEM_ACTIONS))
        self.wrong_policy_cnt = 0

    def get_new_sys_state(self, user_action):
        state_new = self.state.copy()
        if user_action in {PROVIDE_FOOD_TYPE, PROVIDE_PRICE, PROVIDE_LOCATION}:
            state_new[effect_map[user_action]] = 1
        elif user_action in {CONFIRM_POS_FOOD_TYPE, CONFIRM_NEG_FOOD_TYPE, CONFIRM_POS_PRICE,
                             CONFIRM_NEG_PRICE, CONFIRM_POS_LOCATION, CONFIRM_NEG_LOCATION}:
            if user_action < 0:     # negative confirm
                state_new[effect_map[user_action][FILLED]] = 0
                state_new[effect_map[user_action][CONF]] = 0
            else:                   # positive confirm
                if self.state[effect_map[user_action][FILLED]]:
                    state_new[effect_map[user_action][CONF]] = 1
                # if property is not filled, then confirmation does nothing

        return state_new

    def train(self, user: SimulatedUser, max_num_episodes=1000, max_num_actions=30, gamma=0.99,
              exploration_rate=0.5, explore_decay_rate=0.001, Q_update=True, print_history=False,
              store_policy=True, policy_file='policy.csv', episode_history_file='training_history.txt'):

        state_ult = [1] * NUM_OF_STATE_SLOTS

        f_w = open(episode_history_file, 'w')
        for e in range(max_num_episodes):
            alpha = 1 / (1+e)
            if exploration_rate > 0 and e % 10 == 0:
                exploration_rate -= explore_decay_rate

            self.state = [0] * NUM_OF_STATE_SLOTS
            num_actions = 0
            total_reward = 0

            while self.state != state_ult and num_actions < max_num_actions:
                num_actions += 1
                if random.random() < exploration_rate:
                    # choose random action [0 ~ 5]
                    sys_action = random.randint(REQUEST_FOOD_TYPE, EXPLICIT_CONFIRM_LOCATION)
                else:
                    # choose the best action based on Q values
                    sys_action = np.argmax(self.Q_values[tuple(self.state)])

                user_action = user.respond(sys_action)
                state_new = self.get_new_sys_state(user_action)
                reward = 500 if state_new == state_ult else -5
                total_reward += reward
                if print_history:
                    print('system state: {}, system action: {}, user action: {}, reward: {}'
                          .format(self.state, sys_action, user_action, reward))

                # update Q values
                if Q_update:
                    self.Q_values[tuple(self.state)][sys_action] = \
                        (1 - alpha) * self.Q_values[tuple(self.state)][sys_action] + \
                        alpha * (reward + gamma * np.max(self.Q_values[tuple(state_new)]))

                # update system state
                self.state = state_new

            print('episode {} completed, total reward = {}'.format(e + 1, total_reward), file=f_w)

        f_w.close()

        for state, Q_values in self.Q_values.items():
            action = np.argmax(Q_values)
            if state == (1, 1, 1, 1, 1, 1):
                continue
            if (action < 3 and state[action] == 1) or (action >= 3 and (state[action-3] == 0 or state[action] == 1)):
                self.wrong_policy_cnt += 1
                print('wrong: {}    {}'.format(state, action))

        if store_policy:
            with open(policy_file, 'w') as f_w:
                print('FOOD_TYPE_FILLED, PRICE_FILLED, LOCATION_FILLED, '
                      'FOOD_TYPE_CONF, PRICE_CONF, LOCATION_CONF, BEST_ACTION', file=f_w)

                for state in list(itertools.product({0, 1}, repeat=6)):
                    if state in self.Q_values.keys():
                        print(', '.join([str(_) for _ in state] + 
                                        [system_actions[np.argmax(self.Q_values[state])]]), file=f_w)
                    else:
                        # for redundant state (those never happens)
                        print(', '.join([str(_) for _ in state] + ['Null']), file=f_w)

        return

    def test(self, user, max_num_episodes, print_history=False):
        self.train(user, max_num_episodes=max_num_episodes, exploration_rate=0, Q_update=False,
                   print_history=print_history, episode_history_file='test_history.txt')

if __name__ == '__main__':
    # user = SimulatedUser(irrelevant_prob_provide=0.4, irrelevant_prob_confirm=0.2, neg_confirm_prob=0.4)
    # DM = DialogManager()
    # DM.train(user, max_num_episodes=5000, store_policy=True, policy_file='policy.txt')
    # user_test = SimulatedUser(irrelevant_prob_provide=0, irrelevant_prob_confirm=0, neg_confirm_prob=0.4)
    # DM.test(user_test, max_num_episodes=10, print_history=True)

    # max_cnt = 9000
    # explor_rate = 0.3
    # decay_rate = 0.0003
    #
    # ir_provide = 0.4
    # ir_confirm = 0.2
    # neg_confirm = 0.2

    isTuning = 0

    if isTuning:
        cnts = [5000]
        exp = [[1, 0.001]]
        ir_prov = [0.16, 0.18, 0.2]
        ir_conf = [0.1, 0.12]
        neg_conf = [0.1]

        for cnt, e, irprov, irconf, negconf in itertools.product(cnts, exp, ir_prov, ir_conf, neg_conf):
            user = SimulatedUser(irrelevant_prob_provide=irprov, irrelevant_prob_confirm=irconf,
                                 neg_confirm_prob=negconf)

            wrong_policy_cnt = 0
            for i in range(1000):
                print('test {}'.format(i + 1))
                DM = DialogManager()
                DM.train(user, max_num_episodes=cnt, store_policy=False,
                         exploration_rate=e[0], explore_decay_rate=e[1])
                wrong_policy_cnt += DM.wrong_policy_cnt


            print("wrong policy cnt: {}".format(wrong_policy_cnt))
            with open('tuning.txt', 'a+') as f:
                f.write('{} {} {} || {} {} {} || {}\n'
                        .format(cnt, e[0], e[1], irprov, irconf, negconf, wrong_policy_cnt))
    else:
        cnt = 5000
        e = [1, 0.001]
        irprov = 0.2
        irconf = 0.1
        negconf = 0.1

        user = SimulatedUser(irrelevant_prob_provide=irprov, irrelevant_prob_confirm=irconf,
                             neg_confirm_prob=negconf)

        wrong_policy_cnt = 0
        for i in range(1000):
            print('test {}'.format(i + 1))
            DM = DialogManager()
            DM.train(user, max_num_episodes=cnt, store_policy=False,
                     exploration_rate=e[0], explore_decay_rate=e[1])
            wrong_policy_cnt += DM.wrong_policy_cnt

        print("wrong policy cnt: {}".format(wrong_policy_cnt))
        with open('tuning.txt', 'a+') as f:
            f.write('{} {} {} || {} {} {} || {}\n'
                    .format(cnt, e[0], e[1], irprov, irconf, negconf, wrong_policy_cnt))

    notification.notify('End', 'End')
