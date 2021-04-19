import re
import numpy as np
from Constants import *

restaurant_db = np.genfromtxt('restaurantDatabase.txt', delimiter='\t', dtype='str', usecols=list(range(5)))[1:,:]

food_types = set(restaurant_db[:, 2])
price_points = set(restaurant_db[:, 3])
locations = set(restaurant_db[:, 4])
food_types.add('any')
price_points.add('any')
locations.add('any')

policy_raw = np.loadtxt('policy.txt', delimiter=', ', dtype='str')
policy = {}
for i in range(1, len(policy_raw)):
    if policy_raw[i][6] == 'Null':
        continue
    state = tuple([int(_) for _ in policy_raw[i][:6]])
    policy[state] = policy_raw[i][6]

sys_data = [''] * NUM_OF_DATA_SLOTS
sys_state = [0] * NUM_OF_STATE_SLOTS
state_ult = [1] * NUM_OF_STATE_SLOTS

def system_prompt(sys_action: str):
    if sys_action == 'REQUEST_FOOD_TYPE':
        print('System: What type of food do you want?')
    elif sys_action == 'REQUEST_PRICE':
        print('System: How expensive a restaurant do you want?')
    elif sys_action == 'REQUEST_LOCATION':
        print('System: Where do you want the restaurant to be located?')
    elif sys_action == 'EXPLICIT_CONFIRM_FOOD_TYPE':
        if sys_data[FOOD_TYPE] == 'any':
            print('System: You said you wanted any type of food restaurant, right?')
        else:
            print('System: You said you wanted a {} restaurant, right?'
              .format(sys_data[FOOD_TYPE].lower().capitalize()))
    elif sys_action == 'EXPLICIT_CONFIRM_PRICE':
        if sys_data[PRICE] == 'any':
            print('System: You said you were ok with any price restaurant, right?')
        else:
            print('System: You said you wanted a restaurant that is {}, right?'.format(sys_data[PRICE].lower()))
    elif sys_action == 'EXPLICIT_CONFIRM_LOCATION':
        if sys_data[LOCATION] == 'any':
            print('System: You said you were ok with any location, right?')
        else:
            print('System: You said you wanted a restaurant in {}, right?'.format(sys_data[LOCATION]))

def parse_user_input(user_input: str, sys_action: str):
    user_input_words = {_.lower() for _ in re.sub('[^a-zA-Z]+', ' ', user_input).split()}
    if sys_action == 'REQUEST_FOOD_TYPE':
        for f_t in food_types:
            if f_t.lower() in user_input_words:
                sys_data[FOOD_TYPE] = f_t
                sys_state[FOOD_TYPE_FILLED] = 1
                break
    elif sys_action == 'REQUEST_PRICE':
        for p_p in price_points:
            if set(p_p.split('-')).issubset(user_input_words):
                sys_data[PRICE] = p_p
                sys_state[PRICE_FILLED] = 1
                break
    elif sys_action == 'REQUEST_LOCATION':
        for loc in locations:
            if {_.lower() for _ in loc.split()}.issubset(user_input_words):
                sys_data[LOCATION] = loc
                sys_state[LOCATION_FILLED] = 1
                break
    else:
        m = {
            'EXPLICIT_CONFIRM_FOOD_TYPE': [FOOD_TYPE_FILLED, FOOD_TYPE_CONF],
            'EXPLICIT_CONFIRM_PRICE': [PRICE_FILLED, PRICE_CONF],
            'EXPLICIT_CONFIRM_LOCATION': [LOCATION_FILLED, LOCATION_CONF]
        }
        if 'yes' in user_input_words:
            sys_state[m[sys_action][1]] = 1
        elif 'no' in user_input_words:
            sys_state[m[sys_action][0]] = 0
            sys_state[m[sys_action][1]] = 0


max_cnt = 25
cnt = 0
while sys_state != state_ult and cnt < max_cnt:
    cnt += 1
    sys_action = policy[tuple(sys_state)]
    system_prompt(sys_action)

    user_input = input('User: ')
    parse_user_input(user_input, sys_action)

# query
f_t = restaurant_db[:, 2]
p_p = restaurant_db[:, 3]
loc = restaurant_db[:, 4]
food_type = sys_data[FOOD_TYPE]
price = sys_data[PRICE]
location = sys_data[LOCATION]

restaurant_fil = restaurant_db[(f_t == (food_type if food_type != 'any' else f_t))
                               & (p_p == (price if price != 'any' else p_p))
                               & (loc == (location if location != 'any' else loc))]

if len(restaurant_fil) == 0:
    print('System: No results found.')
else:
    print('System: I found {} restaurants matching your query. '.format(len(restaurant_fil))
          + ' '.join(['{} is {} {} restaurant in {}. The phone number is {}.'
                     .format(r[0], ('an ' if r[3] == 'expensive' else 'a ') + r[3], r[2], r[4], r[1])
                      for r in restaurant_fil]))

