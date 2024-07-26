import pandas as pd

states = ['California', 'Texas', 'Florida', 'New York']
populations = [39613493, 29730311, 21944577, 19299981]

dict_states = {'State': states, 'Population': populations}

df_states = pd.DataFrame.from_dict(dict_states)

# print(df_states)

df_states.to_csv('states.csv', index=False)

# Handling exceptions
new_list = [2, 4, 6, "California", 8, 10]

for element in new_list:
    print(element/2)