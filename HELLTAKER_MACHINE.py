# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 23:38:27 2020

@author: user
"""

from anytree import Node, RenderTree
import numpy as np
import copy
import time

world_map=np.array([[9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,0,-1,9,9],
                    [9,9,0,0,2,0,0,9,9],
                    [9,9,0,2,0,2,9,9,9],
                    [9,0,0,9,9,9,9,9,9],
                    [9,0,1,0,0,1,0,9,9],
                    [9,0,1,0,1,0,0,10,9],
                    [9,9,9,9,9,9,9,9,9]])
'''-1=player, 0=void, 1=block, 2=skul, 4=locker, 9=wall, 10=devil or goal'''

spike_map=np.array([[0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0]])
                    
'''0=void, 1=spike, 2=moving spike on, 3=moving spike off, 4=key'''

W, H= world_map.shape[1], world_map.shape[0]

def player_xy(world):
    for y in range(H):
        for x in range(W):
            if world[y][x]==-1:
                return [x,y]  
            
def goal_xy(world):
    for y in range(H):
        for x in range(W):
            if world[y][x]==10:
                return [x,y] 
def g(node):
    return node.name[2]

def update_g(g, world, spike):
    g_value = g+1
    [x, y] = player_xy(world)
    if spike[y][x]==1 or spike[y][x]==2:
        g_value = g_value+1
    return g_value

def h(node, goal):
    [x, y] = player_xy(node.name[0])
    return abs(x-goal[0])+abs(y-goal[1])
    
def close_list_overlap(close_list, value):
    if close_list==None:
        return False
    #print(node.name)
    for close_node in close_list:
        if (close_node.name[0]==value[0]).all() and (close_node.name[1]==value[1]).all():
            return True
    return False

def open_list_overlap(open_list, value):
    if open_list==None:
        return False
    #print(node.name)
    for open_node in open_list:
        if (open_node.name[0]==value[0]).all() and (open_node.name[1]==value[1]).all():
            return True
    return False

def destroy_skul(world, spike):
    for y in range(H):
        for x in range(W):
            if world[y][x]==2:
                if spike[y][x]==1 or spike[y][x]==2:
                    world[y][x]=0
                    
def update_key(world, spike, key):
    new_key=copy.deepcopy(key)
    new_spike=copy.deepcopy(spike)
    [x, y] = player_xy(world)
    if new_spike[y][x]==4:
        new_spike[y][x]=0
        new_key=True
    return new_key, new_spike
                     
def wall_move(world, wall_xy, wasd): 
    [x, y] = wall_xy
    if wasd=='d' and x+1 < W:
        if world[y][x+1]==0:
            world[y][x]=0
            world[y][x+1]=1
    elif wasd=='a' and x-1 > -1:
        if world[y][x-1]==0:
            world[y][x]=0
            world[y][x-1]=1
    elif wasd=='w' and y+1 < H:
        if world[y+1][x]==0:
            world[y][x]=0
            world[y+1][x]=1
    elif wasd=='s' and y-1 > -1:
        if world[y-1][x]==0:
            world[y][x]=0
            world[y-1][x]=1
            
def skul_move(world, skul_xy, wasd): 
    [x, y] = skul_xy
    if wasd=='d' and x+1 < W:
        if world[y][x+1]==0:
            world[y][x]=0
            world[y][x+1]=2
        else:
            world[y][x]=0
    elif wasd=='a' and x-1 > -1:
        if world[y][x-1]==0:
            world[y][x]=0
            world[y][x-1]=2
        else:
            world[y][x]=0
    elif wasd=='w' and y+1 < H:
        if world[y+1][x]==0:
            world[y][x]=0
            world[y+1][x]=2
        else:
            world[y][x]=0
    elif wasd=='s' and y-1 > -1:
        if world[y-1][x]==0:
            world[y][x]=0
            world[y-1][x]=2   
        else:
            world[y][x]=0
            
def player_move(world, key, wasd):
    world=copy.deepcopy(world)
    [x, y] = player_xy(world)
    if wasd=='d' and x+1 < W:
        if not world[y][x+1]==9:
            if world[y][x+1]==0 or world[y][x+1]==10:
                world[y][x]=0
                world[y][x+1]=-1
            elif world[y][x+1]==1:
                wall_move(world, [x+1,y], 'd')
            elif world[y][x+1]==2:
                skul_move(world, [x+1,y], 'd')
            elif world[y][x+1]==4 and key:
                world[y][x]=0
                world[y][x+1]=-1
    elif wasd=='a' and x-1 > -1:
        if not world[y][x-1]==9:
            if world[y][x-1]==0 or world[y][x-1]==10:
                world[y][x]=0
                world[y][x-1]=-1
            elif world[y][x-1]==1:
                wall_move(world, [x-1,y],'a')
            elif world[y][x-1]==2:
                skul_move(world, [x-1,y],'a')
            elif world[y][x-1]==4 and key:
                world[y][x]=0
                world[y][x-1]=-1
    elif wasd=='w' and y+1 < H:
        if not world[y+1][x]==9:
            if world[y+1][x]==0 or world[y+1][x]==10:
                world[y][x]=0
                world[y+1][x]=-1
            elif world[y+1][x]==1:
                wall_move(world, [x,y+1],'w')
            elif world[y+1][x]==2:
                skul_move(world, [x,y+1],'w')
            elif world[y+1][x]==4 and key:
                world[y][x]=0
                world[y+1][x]=-1
    if wasd=='s' and y-1 > -1:
        if not world[y-1][x]==9:
            if world[y-1][x]==0 or world[y-1][x]==10:
                world[y][x]=0
                world[y-1][x]=-1
            elif world[y-1][x]==1:
                wall_move(world, [x,y-1],'s')
            elif world[y-1][x]==2:
                skul_move(world, [x,y-1],'s')
            elif world[y-1][x]==4 and key:
                world[y][x]=0
                world[y-1][x]=-1
    return world

def spike_move(spike):
    spike=copy.deepcopy(spike)
    for y in range(H):
        for x in range(W):
            if spike[y][x]==2:
                spike[y][x]=3
            elif spike[y][x]==3:
                spike[y][x]=2
    return spike
    
def make_children(close_list, node): 
    world=copy.deepcopy(node.name[0])
    spike=copy.deepcopy(node.name[1])
    new_spike=spike_move(spike)
    destroy_skul(world, new_spike)
    key=copy.deepcopy(node.name[3])
    x, y = player_xy(world)
    if x+1 < W:
        new_world=player_move(world, key, 'd')
        new_key, new_spike=update_key(new_world, new_spike, key)
        if not world[y][x+1]==9 and not close_list_overlap(close_list, [new_world, new_spike]):
            g_value=update_g(g(node), new_world, new_spike)
            Node([new_world, new_spike, g_value, new_key, 'RIGHT'], parent=node)
    if x-1 > -1:
        new_world=player_move(world, key, 'a')
        new_key, new_spike=update_key(new_world, new_spike, key)
        if not world[y][x-1]==9 and not close_list_overlap(close_list, [new_world, new_spike]):
            g_value=update_g(g(node), new_world, new_spike)
            Node([new_world, new_spike, g_value, new_key, 'LEFT'], parent=node)
    if y+1 < H:
        new_world=player_move(world, key, 'w')
        new_key, new_spike=update_key(new_world, new_spike, key)
        if not world[y+1][x]==9 and not close_list_overlap(close_list, [new_world, new_spike]):
            g_value=update_g(g(node), new_world, new_spike)
            Node([new_world, new_spike, g_value, new_key, 'DOWN'], parent=node)
    if y-1 > -1:
        new_world=player_move(world, key, 's')
        new_key, new_spike=update_key(new_world, new_spike, key)
        if not world[y-1][x]==9 and not close_list_overlap(close_list, [new_world, new_spike]):
            g_value=update_g(g(node), new_world, new_spike)
            Node([new_world, new_spike, g_value, new_key, 'UP'], parent=node)
    

def A_star(start, spike, goal, debug=False):
    start_time = time.time()
    
    open_list=[]
    close_list=[]
    start_node=Node([start, spike, 0, False, 'ORIGIN'])
    
    open_list.append(start_node)
    
    while True:
        if open_list == []:
            print('All node searched.')
            print("WorkingTime: %s sec" %(time.time()-start_time))
            return None
    
        f_list=[]
        
        for node in open_list:
            f_list.append(g(node)+h(node, goal))

            if debug:
                print('('+str(g(node))+','+str(h(node, goal))+')',end=', ')
        if debug:             
            print('\n')     
        for node in open_list:
            if player_xy(node.name[0]) == goal:
                print("WorkingTime: %s sec" %(time.time()-start_time))
                return node 
            if g(node)+h(node, goal) == min(f_list):
                            
                open_list.remove(node)
                close_list.append(node)
                make_children(close_list,node)
                    
                for child in node.children:
                    
                    if open_list_overlap(open_list, child.name):
                        for open_node in open_list:
                            if (open_node.name[0]==child.name[0]).all() and (open_node.name[1]==child.name[1]).all():
                                if g(open_node) > g(child):
                                    open_list.remove(open_node)
                                    open_list.append(child)
                    else:
                        open_list.append(child)
def draw_path(node):
    if node==None:
        print('not exist')
    else:
        for i in node.path:
            print(i.name)
            print('')

def simple_path(node):
    if node==None:
        print('not exist')
    else:
        for i in node.path:
            print(str(i.name[2]) + ':' + i.name[4])
            
def draw_tree(node):
    if node==None:
        print('not exist')
    else:
        root=node.root
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))

def number_of_nodes(node):
    if node==None:
        print('not exist')
    else:
        print(len(node.root.descendants))

start=world_map
goal=goal_xy(world_map)     
goal_node=A_star(start,spike_map,goal,debug=True)

#draw_path(goal_node)
#draw_tree(goal_node)

simple_path(goal_node)
number_of_nodes(goal_node)
     
def auto_play(node):
    import pyautogui
    
    unit_time = 0.05
    if node==None:
        print('not exist')
    else:
        for i in node.path:
            time.sleep(3*unit_time)
            if i.name[4]=='UP':
                pyautogui.press('w')
            elif i.name[4]=='DOWN':
                pyautogui.press('s')
            elif i.name[4]=='LEFT':
                pyautogui.press('a')
            elif i.name[4]=='RIGHT':
                pyautogui.press('d')
   
            
        print('Done')

auto_play(goal_node)
