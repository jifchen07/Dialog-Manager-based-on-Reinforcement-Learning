import numpy as np
import collections

restaurant_db = np.genfromtxt('restaurantDatabase.txt', delimiter='\t', dtype='str', usecols=list(range(5)))[1:,:]
restaurant_dict = {r[0]: r[1:] for r in restaurant_db}
# food_types = np.unique(restaurant_db[:, 2])
# prices = np.unique(restaurant_db[:, 3])
# locations = np.unique(restaurant_db[:, 4])

r_by_type = collections.defaultdict(list)
r_by_price = collections.defaultdict(list)
r_by_location = collections.defaultdict(list)
for r in restaurant_db:
    r_by_type[r[2]].append(r[0])
    r_by_price[r[3]].append(r[0])
    r_by_location[r[4]].append(r[0])


