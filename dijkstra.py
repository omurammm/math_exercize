#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def dijkstra(weights):
    num_nodes = len(weights)
    # 重みの合計の暫定値と確定値
    sum_tmp = [math.inf for _ in range(num_nodes)]
    sum_fixed = [0 for _ in range(num_nodes)]

    # 仮のルートと確定のルート
    route_tmp = [[] for _ in range(num_nodes)]
    route_fixed = [[] for _ in range(num_nodes)]
    
    # 経路のスタートは1
    route_tmp[0] = [1]
    route_fixed[0] = [1]
    
    min_idx = 0
    
    # ゴールの重みの合計の確定値が出るまで繰り返す
    while not sum_fixed[-1]:
        for i in range(num_nodes):
            # 経路が存在し、重みの合計の暫定の値より小さければ更新
            if weights[min_idx][i] != 0 and sum_fixed[min_idx] + weights[min_idx][i] < sum_tmp[i]:
                sum_tmp[i] = sum_fixed[min_idx] + weights[min_idx][i] 
                route_tmp[i] = route_fixed[min_idx] + [i+1] 
        # 暫定の重みの合計が最小のノードの重みの合計、ルートを確定にする。
        min_idx = sum_tmp.index(min(sum_tmp))
        sum_fixed[min_idx] = sum_tmp[min_idx]
        route_fixed[min_idx] = route_tmp[min_idx]
        
        # 確定にしたノードの重みの合計の暫定値を inf に戻す
        sum_tmp[min_idx] = math.inf
    return route_fixed[-1], sum_fixed[-1]
        
        
def main():
    weight_matrix = [[0,50,80,0,0],[0,0,20,15,0],[0,0,0,10,15],[0,0,0,0,30],[0,0,0,0,0]]
    route, weight_sum = dijkstra(weight_matrix)
    print("Route : ", route)
    print("Sum Weights : ", weight_sum)
    
if __name__ == '__main__':
    main()

