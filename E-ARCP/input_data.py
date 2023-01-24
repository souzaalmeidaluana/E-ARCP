#!/usr/bin/env python
# coding: utf-8

# # Input Data

# ## Network properties

# In[1]:


#Name of the instance file without the extension (.txt)
instance_name = "MPC-10"
#Time horizon in hours
t_max = 7
#Traversing speed of the road clearing teams (km/h)
speed = 50


# ## Solver properties

# In[2]:


#Solver processing time limit in seconds
processing_time_limit = 3600
#Choice of a solver (GUROBI or Other)
solver = "GUROBI"


# ## Visualization

# In[3]:


#Display the results? (True if yes and False if no)
display_results = True
#Color of the intact roads
open_road_color = "green"
#Color of the closed roads
closed_road_color = "red"
#Color and size of the nodes
nodesize = 150
nodecolor = "white"
nodeboundary = "black"
#Color of the road clearing teams' routes
team_color = "blue"

