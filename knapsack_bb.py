#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   ナップサック問題を分枝限定法で解く
#   main(重さのリスト, 最大重量, 価値のリスト)
#

import numpy as np
import pandas as pd

class Brand_and_Bound:
    def __init__(self, weights, max_, target):
        r = np.array(target)/np.array(weights)
        df = pd.DataFrame({
            "r":r,
            "weights":weights,
            "target":target})
        # target/weight で並び替え
        self.df = df.sort_values(by='r')
        self.problems = [(list(self.df["weights"]), max_, list(self.df["target"]), 0, [])]
        self.constant = 0
        # 欲張り法で求めたxを初期xに
        self.df["x_initial"] = self.greedy_method(max_)
        self.x_tmp = list(self.df["x_initial"])
        x_sorted = list(self.df.sort_index()["x_initial"])
        self.value_tmp = np.dot(np.array(target), np.array(x_sorted))
    
    # 欲張り法
    def greedy_method(self, max_):
        x = []
        weights = list(self.df["weights"])
        for i in range(len(weights)):
            if weights[-i-1] <= max_:
                x.append(1)
                max_ -= weights[-i-1]
            else:
                x.append(0)
        return x[::-1]
        
    #　部分問題を解く。深さ優先探索。
    def partial_problem(self):
        problem = self.problems.pop()
        weights = problem[0][:]
        max_ = problem[1]
        target = problem[2][:]
        cons = problem[3]
        x = problem[4][:]
        x0 = x[:]
        
        # 残る x が一つならば、0 or 1を代入して最適解か検討
        if len(weights) == 1:
            if weights[0] <= max_ and target[0]+cons > self.value_tmp:
                x.append(1)
                self.x_tmp = x[::-1]
                self.value_tmp = target[0] + cons

            if 0 <= max_ and cons > self.value_tmp:
                x0.append(0)
                self.x_tmp = x0[::-1]
                self.value_tmp = cons
            return
                
        # 緩和問題を解く
        val = self.relaxation_problem(*problem[:3]) 
        if val + problem[3] <= self.value_tmp:
            return

        # x = 1,0　としたものを部分問題に追加
        w = weights.pop()
        t = target.pop()

        x.append(1)
        self.problems.append((weights, max_ - w, target, cons+t, x))
        x0.append(0)
        self.problems.append((weights, max_, target, cons, x0))
        
    # 緩和問題
    def relaxation_problem(self, weights, max_, target):
        val = 0
        l = len(weights)
        for i in range(l):
            if weights[-i-1] < max_:
                val += target[-i-1]
                max_ -= weights[-i-1]
            else:
                val += target[-i-1] * (max_ / weights[-i-1])
                return val
        return val
        
    def run(self):
        while len(self.problems) != 0:
            self.partial_problem()
            
        self.df["x"] = self.x_tmp
        x = list(self.df.sort_index()["x"])
        return x, self.value_tmp
    
def main():
    bb = Brand_and_Bound([2,3,5,6],9,[4,5,12,14])
    return bb.run()
    
if __name__ == '__main__':
    print(main())

