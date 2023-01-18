#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import copy

def get_indexes(lines):
    """This function reads the instance file and identifies the start and stop indexes of the lines 
    with the network dimension, depot id, coordinates, edges, unblocking times, components, relative prizes,
    and the teams located in each depot"""
    all_depots = []
    for l in range(len(lines)):
        line = lines[l]
        if line[:11] == "DIMENSION: ":
            nodes = int(line[11:])
        if line[:10] == "DEPOT_ID: ":
            all_depots_string = list(line[11:-2].split(", "))
            all_depots = [int(i) for i in all_depots_string]
        if line[:18] == "NODE_COORD_SECTION":
            coordinates_start = copy.deepcopy(l)+1
        if line[:30] == "LIST_OF_ALL_EDGES_DATA_SECTION":
            coordinates_end = copy.deepcopy(l)-1
            list_of_edges_start = copy.deepcopy(l)+1
        if line[:50] == "DAMAGED_EDGES_DATA_SECTION (EDGE, UNBLOCKING TIME)":
            list_of_edges_end = copy.deepcopy(l)-1
            damaged_edges_start = copy.deepcopy(l)+1
        if line[:10] == "COMPONENTS":
            damaged_edges_end = copy.deepcopy(l)-1
            components_start = copy.deepcopy(l)+1
        if line[:15] == "RELATIVE PRIZES":
            components_end = copy.deepcopy(l)-1
            prizes_start = copy.deepcopy(l)+1
        if line[:33] == "TEAMS PER DEPOT (DEPOT_ID, TEAMS)":
            prizes_end = copy.deepcopy(l)-1
            teams_depot_start = copy.deepcopy(l)+1
    teams_depot_end = len(lines)-1
    
    return nodes, all_depots, coordinates_start, coordinates_end, list_of_edges_start, list_of_edges_end, damaged_edges_start, damaged_edges_end, prizes_start, prizes_end, teams_depot_start, teams_depot_end, components_start, components_end


# In[1]:


def get_coordinates(lines, coordinates_start, coordinates_end):
    """This function reads the coordinates in the instance file and converts to matrix form"""
    coordinates = []
    for i in range(coordinates_start, coordinates_end+1):
        #Remove the "\n" from the string
        coordinates_string = list(lines[i][0:-1].split("\t"))
        #Convert the string to float numbers
        x_coord = float(coordinates_string[1])
        y_coord = float(coordinates_string[2])
        #Append the coordinates in the list of coordinates
        coordinates.append([x_coord, y_coord]) 
    return coordinates


# In[2]:


def get_edges(lines, list_of_edges_start, list_of_edges_end):
    """This function reads the instance file and creates the list of edges in the network"""
    #Create an empty list
    list_of_edges = []
    for i in range(list_of_edges_start, list_of_edges_end+1):
        #Remove the "\n" from the string
        list_of_edges_string = list(lines[i][0:-1].split("\t"))
        #Convert the string to int numbers
        node_1 = int(list_of_edges_string[0])
        node_2 = int(list_of_edges_string[1])
        #Append the edge to the list of edges
        list_of_edges.append([node_1, node_2])
    return list_of_edges 


# In[3]:


def get_damaged_edges(lines, damaged_edges_start, damaged_edges_end):
    """This function reads the instance file and creates the list of damaged edges and their unblocking times"""
    #Create an empty list
    damaged_edges = []
    for i in range(damaged_edges_start, damaged_edges_end+1):
        #Remove the "\n" from the string
        damaged_edges_string = list(lines[i][0:-1].split("\t"))
        #Convert the string to int numbers
        node_1 = int(damaged_edges_string[0])
        node_2 = int(damaged_edges_string[1])
        time = float(damaged_edges_string[2])
        damaged_edges.append([node_1, node_2, time])
    return damaged_edges


# In[4]:


def get_prizes(lines, prizes_start, prizes_end):
    """This function reads the instance file and creates the list of relative prizes"""
    #Create an empty list
    relative_prizes = []
    for i in range(prizes_start, prizes_end+1):
        #Remove the "\n" from the string
        relative_prizes_string = list(lines[i][0:-1].split("\t"))
        #Convert the string to int numbers
        node_1 = int(relative_prizes_string[0])
        node_2 = int(relative_prizes_string[1])
        prize = int(relative_prizes_string[2])
        relative_prizes.append([node_1, node_2, prize])
    return relative_prizes


# In[5]:


def get_teams_depot(lines, teams_depot_start, teams_depot_end):
    """This function reads the instance file and creates the list the teams' depots"""
    #Create an empty list
    teams_depot = []
    for i in range(teams_depot_start, teams_depot_end+1):
        #Remove the "\n" from the string
        teams_depot_string = list(lines[i][0:-1].split("\t"))
        #Convert the string to int numbers
        node = int(teams_depot_string[0])
        teams = int(teams_depot_string[1])
        teams_depot.append([node, teams])
    return teams_depot


# In[6]:


def get_components(lines, components_start, components_end):
    """This function reads the instance file and creates the list of components"""
    #Create an empty list
    all_components = []
    for i in range(components_start, components_end+1):
        #Remove the "\n" from the string
        components_string = list(lines[i][1:-2].split("\t"))
        component = list(components_string[1][1:].split(","))
        all_components.append([int(i) for i in component])
    return all_components


# In[7]:


def retrieve_file_data(instance_name):
    """This function opens the instance file and retrive all the data"""
    with open(instance_name+'.txt') as f:
        lines = f.readlines()
        nodes, all_depots, coordinates_start, coordinates_end, list_of_edges_start, list_of_edges_end, damaged_edges_start, damaged_edges_end, prizes_start, prizes_end, teams_depot_start, teams_depot_end, components_start, components_end = get_indexes(lines) 
        coordinates = get_coordinates(lines, coordinates_start, coordinates_end)
        list_of_edges = get_edges(lines, list_of_edges_start, list_of_edges_end)
        damaged_edges = get_damaged_edges(lines, damaged_edges_start, damaged_edges_end)
        relative_prizes = get_prizes(lines, prizes_start, prizes_end)
        components = get_components(lines, components_start, components_end)
        teams_depot = get_teams_depot(lines, teams_depot_start, teams_depot_end)
        
    return nodes, all_depots, coordinates, list_of_edges, damaged_edges, relative_prizes, teams_depot, components


# In[ ]:




