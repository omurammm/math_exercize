#!/usr/bin/python
# -*- coding: utf-8 -*-

from sympy import *


#関数1
def f1(x):
    return 1/x+exp(x)

#関数２
def f2(x):
    return sin(5*x)+(x-5)**2

#黄金分割法
def golden_section(f, a, b, n):
    print("(a0, b0) =",(a, b))
    #　τ
    t = (-1+5**(1/2))/2
    for i in range(n):
        #λ1
        r2 = t*(b-a)+a
        #λ2
        r1 = t*(r2-a)+a
        if f(r1) < f(r2):
            b = r2
        elif f(r1) > f(r2):
            a = r1
        #f(r1) とf(r2)の差の絶対値が1e-10以下で収束とする
        elif abs( f(r1) - f(r2))<1e-10:
            print("Converged :",(a,b)," Update ", i, "times.")
            return (a, b)
        print("(a,b) =",(a,b))
    return(a,b)

#二分割法
def bisection(f, a, b, n):
    print("(a0, b0) =",(a, b))
    x = Symbol('x')
    #f'(x)
    f_ = diff(f(x),x)
    for i in range(n):
        #ラムダ
        r = (a+b)/2  
        if f_.subs(x,r) > 0:
            b = r
        elif f_.subs(x,r) < 0:
            a = r
        #f' にラムダ代入した値が1e-10以下で収束とする
        elif abs(f_.subs(x,r))<1e-10:
            print("Converged :",(a,b)," Update ", i, "times.")
            return (a, b)
        print("(a,b) =",(a,b))
    return(a,b)

#ニュートン法
def newton(f, x0, n):
    print("x0 = ", x0)
    x = Symbol('x')
    #f'
    f_ = diff(f(x),x)
    #f''
    f_2 = diff(f_.subs(x,x), x)
    for i in range(n):
        update = float(f_.subs(x, x0)/f_2.subs(x,x0))
        #更新幅1e-10以下で収束とする
        if abs(update)<1e-10:
            print("Converged :", x0, " Update ", i, "times.")
            return x0
        x0 = x0 - update
        print("x : ",x0)
    return (x0)


#実行

#関数1
print("f(x) = 1/x+exp(x)")
print("\nGolden Section")
golden_section(f1,0.001,10,100)
print("\nBisection")
bisection(f1,0.001,10,100)
print("\nNewton")
newton(f1,0.001,1000)

#関数2
print("f(x) = sin(5*x)+(x-5)**2")
print("\nGolden Section")
golden_section(f2,2,6,100)
print("\nBisection")
bisection(f2,2,6,100)
print("\nNewton")
newton(f2,4,1000)
newton(f2,5,1000)
newton(f2,4.5,1000)
