#!/usr/bin/env python
# coding: utf-8

# In[1]:


from geometria import *


# In[2]:


Tolerance = 10e-12


# # Funkcje pomocnicze

# In[3]:


# sprawdzanie, po której stronie odcinka leży punkt - funkcje pomocnicze
def det(a, b, c):
    return a[0] * b[1] + b[0] * c[1] + a[1] * c[0] - c[0] * b[1] - b[0] * a[1] - a[0] * c[1]

def orient(a, b, c):
    determinant = det(a, b, c)
    if determinant > Tolerance: # lewa strona
        return 1
    elif determinant < -Tolerance: # prawa strona
        return -1
    else: # współliniowe
        return 0
    
def find_left(a, b, points): # punkty leżące po lewej stronie odcinka utworzonego przez punkty a i b
    left = []
    for point in points:
        o = orient(a, b, point)
        if o == 1:
            left.append(point)
    return left

def find_right(a,b,points):  # punkty leżące po prawej stronie odcinka utworzonego przez punkty a i b
    right = []
    for point in points:
        o = orient(a, b, point)
        if o == -1:
            right.append(point)
    return right

# wyszukiwanie najdalej leżącego punktu

def find_segment(a,b): # równanie prostej, wyszukiwanie współczynników A i C dla równania postaci y = Ax + C
    A = (a[1] - b[1])/(a[0] - b[0])
    C = a[1] - A * a[0]
    return A, C

def find_distance(a,b,c): # odległość punktu c od prostej utworzonej przez punkty a i b
    A, C = find_segment(a,b) # B = -1 bo przenoszę y w równaniu: y = Ax + C -> 0 = Ax -y + C
    B = -1
    distance = abs(A*c[0] + B*c[1] + C)/ sqrt(A**2 + B**2)
    return distance

def find_furthest(a, b, points): # punkt najbardziej oddalony od prostej wyznaczonej przez punkty a i b
    result, distance = None, 0
    for point in points:
        if result is None or find_distance(a,b,point) > distance:
            distance = find_distance(a,b,point)
            result = point
    return result

# do wizualizacji kolejnych kroków algorytmu

def add_scene(points, scenes, points_in_hull, a, c):
    
    if a in points_in_hull:
        idx = points_in_hull.index(a)
        points_in_hull.insert(idx+1,c)
        
    n = len(points_in_hull)
    
    lines = [(points_in_hull[i], points_in_hull[(i + 1) % n]) for i in range(n)]
    scenes.append(Scene([PointsCollection(points, color='hotpink'),
                         PointsCollection(points_in_hull, color='green')],
                    [LinesCollection(lines, color='lime')]))


# # Główny algorytm

# In[4]:


def recursion(a, b, points_sorted, scenes, points, points_in_hull):
    if points_sorted == [] or a is None or b is None: # warunek końca rekurencji - nie ma punktów 
        return []
    
    hull = []
    c = find_furthest(a, b, points_sorted) # szukamy najbardziej oddalonego punktu
    if c is None: return []
    points_sorted.remove(c)
    
    add_scene(points, scenes, points_in_hull, a, c)
    
    # przeszukujemy punkty które znajdują się na zewnątrz 
    points1 = find_left(a, c, points_sorted)
    points2 = find_right(b, c, points_sorted)

    hull = [a] + recursion(a, c, points1, scenes, points, points_in_hull) + [c] + recursion(c, b, points2, scenes,points,points_in_hull) + [b]

    return hull


# In[5]:


def main_algo(points,  scenes):   
    if len(points) < 3: return points
    points_sorted = sorted(points, key = lambda x: (x[0], x[1]))
    result_hull = []
    
    # dwa skrajne punkty A i B - jeden o najmniejszej odciętej, drugi o największej
    a, b = points_sorted[0], points_sorted[-1]
    points_sorted.remove(a)
    points_sorted.remove(b)
    points_in_hull = [a, b] # obecna otoczka
    
    scenes.append(Scene([PointsCollection(points, color='hotpink'),
                PointsCollection(points_in_hull, color='green')],
                [LinesCollection([[a, b]], color='lime')]))
    
    # rekurencyjnie przeszukiwanie punktów powyżej oraz poniżej danego odcinka
    left, right = find_left(a, b, points_sorted), find_right(a, b, points_sorted)
    result_hull += recursion(a, b, left, scenes, points_sorted, points_in_hull) + recursion(b, a, right, scenes, points_sorted, points_in_hull)
    
    return result_hull


# In[6]:


def QuickHull(points): # funkcja wyznaczająca otoczkę oraz wizualizująca algorytm
    scenes = []
    scenes.append(Scene([PointsCollection(points, color='hotpink')]))
    result_hull = main_algo(points, scenes)
    n = len(result_hull)
    lines = [(result_hull[i], result_hull[(i + 1) % n]) for i in range(n)]
    scenes.append(Scene([PointsCollection(points, color='hotpink'),
                         PointsCollection(result_hull, color='green')],
                    [LinesCollection(lines, color='lime')]))
    
    return scenes


# # Algorytm bez wizualizacji 

# In[21]:


def recursion_(a, b, points_sorted):
    if points_sorted == [] or a is None or b is None: # warunek końca rekurencji - nie ma punktów 
        return []
    
    hull = []
    c = find_furthest(a, b, points_sorted) # szukamy najbardziej oddalonego punktu
    if c is None: return []
    points_sorted.remove(c)
    
    # przeszukujemy punkty które znajdują się na zewnątrz 
    points1 = find_left(a, c, points_sorted)
    points2 = find_right(b, c, points_sorted)

    hull = [a] + recursion_(a, c, points1) + [c] + recursion_(c, b, points2) + [b]

    return hull

def main_algo_(points):   
    if len(points) < 3: return points
    points_sorted = sorted(points, key = lambda x: (x[0], x[1]))
    result_hull = []
    
    # dwa skrajne punkty A i B - jeden o najmniejszej odciętej, drugi o największej
    a, b = points_sorted[0], points_sorted[-1]
    points_sorted.remove(a)
    points_sorted.remove(b)

    # rekurencyjnie przeszukiwanie punktów powyżej oraz poniżej danego odcinka
    left, right = find_left(a, b, points_sorted), find_right(a, b, points_sorted)
    result_hull += recursion_(a, b, left) + recursion_(b, a, right)

    return result_hull

def QuickHull_(points): # funkcja wyznaczająca otoczkę 
    return main_algo_(points)

