#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
from copy import deepcopy
import pandas as pd

class TSP_BB:
    def __init__(self, mat):
        df = pd.DataFrame(mat)
        self.length = len(df)
        self.problems = [(df, 0,[],[])]
        
        self.circle = []
        self.min_tmp = math.inf
        
    # 部分問題解く
    def part_problem(self):
        #print(self.problems)
        p = self.problems.pop()
        df = p[0]
        dist = p[1]
        go = p[2]
        # 通らない経路、debug用
        not_go = p[3]
        
        # 通る経路の数が地点の数に一致した時
        if len(go) == self.length: 
            # 一巡閉路かチェック
            circle = self.check_closed(deepcopy(go))
            print("Circle : ", circle, "Distance : ", dist)
            if circle and self.min_tmp > dist:
                self.circle = circle
                self.min_tmp = dist
                return
            else:
                return

        # df が空　or ある行全部がinfの時、終了
        if len(df) == 0 or np.isnan(df.idxmin(axis=1)).any():
            return
        
        # 下界を調べて限定
        if dist + self.get_lower_bound(deepcopy(df)) >= self.min_tmp:
            return
        
       
        # df の中の最小の値とその座標
        val_min, idx = self.min_val_idx(df)
        row, col = idx[0], idx[1]
        
        
        # その座標を通らない場合
        df_not_go = deepcopy(df)
        df_not_go.loc[row, col] = math.inf
        not_go_tmp = not_go[:]
        not_go_tmp.append((row, col))
        self.problems.append((df_not_go, dist, go, not_go_tmp))
        
        # その座標を通る場合
        go_tmp = deepcopy(go)
        go_tmp.append((row,col))
        go_df = df.drop(row)
        go_df = go_df.drop(col, axis=1)
        self.problems.append((go_df, dist+val_min, go_tmp, not_go))
        
        
    # 一巡閉路かチェック
    def check_closed(self, go):
        circle = [go[0][0]+1, go[0][1]+1]
        not_passed = list(range(self.length))
        point = go[0][1]
        not_passed.remove(point)
        while not len(circle) == self.length+1:
            for route in go:
                if route[0] == point:
                    point = route[1]
                    if not point in not_passed:
                        return False
                    not_passed.remove(point)
                    circle.append(point+1)
        return circle
        
    # df の中の最小の値とその座標返す
    def min_val_idx(self, df):
        min_ = math.inf
        mins = df.idxmin(axis=1)
        idx = []
        for i in df.index:
            if math.isnan(mins[i]): 
                continue
            if df.loc[i, mins[i]] < min_:
                min_ = df.loc[i, mins[i]]
                idx = [i, mins[i]]
        return (min_, idx)
        
    # 下界調べる
    def get_lower_bound(self, df):
        lb = 0
        for i in df.index:
            min_ = min(df.loc[i])
            lb += min_
            df.loc[i] = df.loc[i] - min_
            
        for i in df.columns:
            min_ = min(df.loc[:,i])
            lb += min_
            #mat[:,i] = mat[:,i] - min_
        return lb
    
    #　実行
    def run(self):
        while not len(self.problems)==0:
            self.part_problem()
            
        return self.circle, self.min_tmp
    
def main():
    mat = np.array([
        [math.inf, 21, 7, 13, 15],
        [11, math.inf, 19, 12, 25],
        [15, 24, math.inf, 13, 5],
        [6, 17, 9, math.inf, 23],
        [28, 6, 11, 5, math.inf]])
    tsb = TSP_BB(mat)
    circle, dist = tsb.run()
    print("\nAnswer {", "Circle : ", circle, ", Distance : ", dist, "}")
    
if __name__ == '__main__':
    main()
