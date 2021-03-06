# Quantities
NUM_OF_DATA_SLOTS = 3
NUM_OF_STATE_SLOTS = 6
NUM_OF_SYSTEM_ACTIONS = 6

# DM system data
FOOD_TYPE = 0
PRICE = 1
LOCATION = 2
# DM system states
FOOD_TYPE_FILLED = 0
PRICE_FILLED = 1
LOCATION_FILLED = 2
FOOD_TYPE_CONF = 3
PRICE_CONF = 4
LOCATION_CONF = 5

# DM system actions
REQUEST_FOOD_TYPE = 0
REQUEST_PRICE = 1
REQUEST_LOCATION = 2
EXPLICIT_CONFIRM_FOOD_TYPE = 3
EXPLICIT_CONFIRM_PRICE = 4
EXPLICIT_CONFIRM_LOCATION = 5

# Simulated user actions
PROVIDE_FOOD_TYPE = 0
PROVIDE_PRICE = 1
PROVIDE_LOCATION = 2
CONFIRM_POS_FOOD_TYPE = 3
CONFIRM_NEG_FOOD_TYPE = -3
CONFIRM_POS_PRICE = 4
CONFIRM_NEG_PRICE = -4
CONFIRM_POS_LOCATION = 5
CONFIRM_NEG_LOCATION = -5
IRRELEVANT = 6

system_actions = \
    [
        'REQUEST_FOOD_TYPE',
        'REQUEST_PRICE',
        'REQUEST_LOCATION',
        'EXPLICIT_CONFIRM_FOOD_TYPE',
        'EXPLICIT_CONFIRM_PRICE',
        'EXPLICIT_CONFIRM_LOCATION'
    ]

# Possible user actions based on system actions
# system action: user action
POS = 0
NEG = 1
action_map = \
    {
        REQUEST_FOOD_TYPE: PROVIDE_FOOD_TYPE,
        REQUEST_PRICE: PROVIDE_PRICE,
        REQUEST_LOCATION: PROVIDE_LOCATION,
        EXPLICIT_CONFIRM_FOOD_TYPE: [CONFIRM_POS_FOOD_TYPE, CONFIRM_NEG_FOOD_TYPE],
        EXPLICIT_CONFIRM_PRICE: [CONFIRM_POS_PRICE, CONFIRM_NEG_PRICE],
        EXPLICIT_CONFIRM_LOCATION: [CONFIRM_POS_LOCATION, CONFIRM_NEG_LOCATION]
    }

# user action effect on system states
# user action: affected system state
FILLED = 0
CONF = 1
effect_map = \
    {
        PROVIDE_FOOD_TYPE: FOOD_TYPE_FILLED,
        PROVIDE_PRICE: PRICE_FILLED,
        PROVIDE_LOCATION: LOCATION_FILLED,
        CONFIRM_POS_FOOD_TYPE: [FOOD_TYPE_FILLED, FOOD_TYPE_CONF],
        CONFIRM_POS_PRICE: [PRICE_FILLED, PRICE_CONF],
        CONFIRM_POS_LOCATION: [LOCATION_FILLED, LOCATION_CONF],
        CONFIRM_NEG_FOOD_TYPE: [FOOD_TYPE_FILLED, FOOD_TYPE_CONF],
        CONFIRM_NEG_PRICE: [PRICE_FILLED, PRICE_CONF],
        CONFIRM_NEG_LOCATION: [LOCATION_FILLED, LOCATION_CONF]
    }