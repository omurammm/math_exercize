#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def f1(x):
    A = np.array([
        [9, 12, -6, -3],
        [12, 41, 2, 11],
        [-6, 2, 24, -8],
        [-3, 11, -8, 62]
    ])
    b = np.array([-27, -42, 32, -23])
    c = 163
    return (1/2)*np.dot(np.dot(x.T, A), x) + np.dot(b.T, x) + c

def f1_d(x):
    A = np.array([
        [9, 12, -6, -3],
        [12, 41, 2, 11],
        [-6, 2, 24, -8],
        [-3, 11, -8, 62]
    ])
    b = np.array([[-27, -42, 32, -23]]).T
    return np.dot(A, x) + b

def f2(x):
    A = np.array([
        [16, 8, 12, -12],
        [8, 29, 16, 9],
        [12, 16, 29, -19],
        [-12, 9, -19, 35]
    ])
    b = np.array([7, 5, -2, 9])
    c = 5
    return (1/2)*np.dot(np.dot(x.T, A), x) + np.dot(b.T, x) + c

def f2_d(x):
    A = np.array([
         [16, 8, 12, -12],
        [8, 29, 16, 9],
        [12, 16, 29, -19],
        [-12, 9, -19, 35]
    ])
    b = np.array([[7, 5, -2, 9]]).T
    return np.dot(A, x) + b

def f3(x):
    x1 = x[0][0]
    x2 = x[1][0]
    return np.array([[(x1-1)**2 + 10*(x1**2 - x2)**2]])

def f3_d(x):
    x1 = x[0][0]
    x2 = x[1][0]
    return np.array([[2*(x1-1) + 40*x1*(x1**2 - x2), -20*(x1**2 - x2)]]).T

def gradient_descent(f, f_d, init_x, lr):
    iter_max = 10000  
    x = np.array([init_x]).T
    count = 0
    for i in range(iter_max):
        count = i
        d = f_d(x)
        x = x - lr * d
        #print(i, x.T[0], f(x))
        if np.linalg.norm(lr*d) < 1e-4:
            break
        
    return x.T[0], f(x), count

def conjugate_gradient(f, f_d, init_x):
    iter_max = 10000
    eps = 1e-4
    x = np.array([init_x]).T
    s = - f_d(x)
    count = 0
    for i in range(iter_max):
        count = i
        a = golden_section(f, x, s)
        x_ = x + a * s
        #print(i, x_.T[0], f(x_))
        if np.linalg.norm(x_ - x) < eps:
            break
        s = - f_d(x_) + s * np.dot(f_d(x_).T, f_d(x_)) / np.dot(f_d(x).T, f_d(x))
        x = x_
    return x_.T[0], f(x_), count


def golden_section(f, x, s):
    a = -1
    b = 1
    #　τ
    t = (-1+5**(1/2))/2
    for i in range(100):
        #λ1
        r2 = t*(b-a)+a
        #λ2
        r1 = t*(r2-a)+a
        if f(x+r1*s) < f(x+r2*s):
            b = r2
        elif f(x+r1*s) > f(x+r2*s):
            a = r1
        #f(r1) とf(r2)の差の絶対値が1e-10以下で収束とする
        elif abs( f(x+r1*s) - f(x+r2*s))<1e-10:
            #print("Converged :",(a+b)/2," Update ", i, "times.")
            return (a + b) /2
        #print("(a,b) =",(a,b))
    return (a+b)/2

    


def quasi_newton(f, f_d, init_x):
    iter_max = 10000
    x = np.array([init_x]).T
    H = np.eye(len(x))
    count = 0
    for i in range(iter_max):
        count = i
        s = - np.dot(np.linalg.inv(H), f_d(x))
        x_ = x + s
        #print(i, x_.T[0], f(x_))
        if np.linalg.norm(s) < 1e-4:
            break
        y = f_d(x_) - f_d(x)
        H = H - np.dot(H, np.dot(s, np.dot(s.T, H))) / np.dot(s.T, np.dot(H, s)) + np.dot(y, y.T) / np.dot(s.T, y)
        x = x_
    return x_.T[0], f(x_), count

def print_result(f, f_d, init):
    print("---------------------------------------------------")
    print("Initial x : ", init, "\n")
    print("最急降下法:")
    x_g, f_g, c_g = gradient_descent(f, f_d,init, 0.025)
    print("x = ", x_g)
    #print(f_g)
    print("f(x) = ", f_g[0][0])
    print("Count: ", c_g,"\n")
    
    print("共役勾配法:")
    x_c, f_c, c_c = conjugate_gradient(f, f_d,init)
    print("x = ", x_c)
    print("f(x) = ", f_c[0][0])
    print("Count: ", c_c,"\n")
    
    print("準ニュートン法:")
    x_q, f_q, c_q = quasi_newton(f, f_d,init)
    print("x = ", x_q)
    print("f(x) = ", f_q[0][0])
    print("Count: ", c_q,"\n")


def main():
    print("********Question 1****************")
    print_result(f1, f1_d, [0,0,0,0])
    print_result(f1, f1_d, [10,10,10,10])
    print_result(f1, f1_d, [200,200,200,200])

    print("********Question 2****************" )
    print_result(f2, f2_d, [0,0,0,0])
    print_result(f2, f2_d, [10,10,10,10])
    print_result(f2, f2_d, [200,200,200,200])

    print("********Question 3****************")
    print_result(f3, f3_d, [0,0])
    print_result(f3, f3_d, [10,10])
    print_result(f3, f3_d, [200,200])

if __name__ == '__main__':
    main()
    
