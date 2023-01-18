#!/usr/bin/env python
# coding: utf-8

# In[1]:


def get_f_values(model, K):
    """This function reads the decision variables 
    and creates a nested list with the edges visited by each team"""
    #Create list with the edges in the path
    all_paths = []
    
    for rcteam in K:
        path_edges = []
        #Check the flow value of every team 
        for var in model.variables(): 
            if var.name[0] == "f":
                #If variable f has a positive flow value, separate it by team
                if var.varValue>0: 
                    #Finding the indexes that will be used in the string slicing
                    open_parenthesis = var.name.find("(")
                    close_parenthesis = var.name.find(")")
                    first_comma = var.name.find(",")
                    second_underscore = var.name.find("_", first_comma)
                    third_underscore = var.name.find("_", second_underscore+1)
                    second_comma = var.name.find(",", second_underscore)
                    
                    #Identify the i, j and the team k
                    i = int(var.name[open_parenthesis+1:first_comma])
                    j = int(var.name[second_underscore+1:second_comma])
                    k = int(var.name[third_underscore+1:close_parenthesis])

                    if k == rcteam:
                        path_edges.append((int(var.varValue), i, j))  
        path_edges.sort(reverse=True)
        all_paths.append(path_edges)
    return all_paths


# In[2]:


def organize_teams_routes(all_paths):
    """This function reads the order of every edge of every team, 
    and organizes the edges according to the 
    decreasing order"""
    
    #Create the list that will hold the results
    all_routes = []
    #Go over the set of edges that every team visits
    for team in all_paths:
        #Start the team's route
        teams_route = []
        #Organize the order of the edge
        for i in range(len(team)):
            if i == 0:
                #If it is the first edge visited, both i and j should be added to the route
                edge_i = team[i][1]
                edge_j = team[i][2]
                teams_route.append(edge_i)
                teams_route.append(edge_j)
            else:
                #If this is not the first edge visite,d then only add vertex j to the route
                edge_j = team[i][2]
                teams_route.append(edge_j)
        all_routes.append(teams_route)
    return all_routes


# In[3]:


def save_RC_variables(processing_time, instance_name, teams, 
                      objective_function, all_routes, prob):
    
    """This function reads the outputs of the Linear Programing model 
    and creates a text file with the results"""
    
    import datetime

    today = datetime.datetime.now()
    date_customized = str(today.year)+str(today.month)+str(today.day)+"_"+str(today.hour)+"h"+str(today.minute)+"m"+str(today.second)+"s"
    
    #Save the objetive function and the routes in a text file 
    filename = "MPC-ARCP_"+instance_name+"_solution_"+date_customized+".txt"
    RCfile = open(filename, "w")
    RCfile.write("----------INPUT INFORMATION----------\n\n")
    RCfile.write("Instance = "+instance_name+"\n")
    RCfile.write("Total # of teams = "+str(teams)+"\n")
    RCfile.write("\n----------RESULTS----------\n\n")
    RCfile.write("Processing time (seconds) = "+ str(processing_time) + "\n")
    RCfile.write("Objective function = " + str(objective_function) + "\n")
    #Add each one of the routes to the file
    for i in range(len(all_routes)):
        team = all_routes[i]
        RCfile.write("Team "+str(i)+" = " + str(team) + "\n")
    #Save the decision variables
    RCfile.write("\n\n----------VARIABLES----------\n\n")
    for var in prob.variables():
        if var.varValue > 0:
            RCfile.write(str(var.name) + " = " + str(var.varValue)+"\n")
    RCfile.close


# In[4]:


def data_visualization(E_no_sink, coordinates, open_road_color, closed_road_color, nodesize,
                      nodecolor, nodeboundary, instance_name, all_routes, B, team_color):
    
    """This function reads the outputs of the Linear Programing model 
    and plots the results in a network"""
    
    import networkx as nx
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    
    #Create a new graph and add the edges
    G = nx.Graph()
    G.add_edges_from(E_no_sink)
    #Determine the position of the nodes
    pos = {i: (coordinates[i][0], coordinates[i][1]) for i in range(len(coordinates))}
    
    #Determine the colors of the edges (open = open_road_color, blocked = closed_road_color)
    colors = []
    for edge in G.edges():
        if edge not in B:
            colors.append(open_road_color)
        else:
            colors.append(closed_road_color)
            
    #Setting up the graph
    options = {
        "font_size": 12,
        "node_size": nodesize,
        "node_color": nodecolor,
        "edgecolors": nodeboundary,
        "edge_color": colors,
        "linewidths": 1,
        "width": 1,
    }
    #Creating a list with all the edges in the teams route
    all_teams_routes = []
    for team in all_routes:
        teams_edges = []
        for i in range(len(team)-2):
            teams_edges.append((team[i], team[i+1]))
        all_teams_routes.append(teams_edges)
        
    #Display the graph of the route of each team
    for team in range(len(all_teams_routes)):
        nx.draw_networkx(G, 
                         pos,
                         **options)
        nx.draw_networkx_edges(G, 
                               pos, 
                               arrows = True,
                               edgelist=all_teams_routes[team],
                               width=3,
                               alpha=0.8,
                               edge_color=team_color)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.title("Team #"+str(team))
        plt.savefig(instance_name+"_team_"+str(team)+"_route.png")
        plt.show()

