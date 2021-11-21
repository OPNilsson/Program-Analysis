# -*- coding: utf-8 -*-

class Worklist(object):
    def empty():
        pass
    
    def insert(q, W):
        pass
    
    def extract(W):
        pass
    
# W = (V, P)
class LIFO(Worklist):

    def empty():
        return []
    
    def insert(q, W):
        return [q] + W
            
    def extract(W):
        return (W[0], W[1:]) 
    
class FIFO(Worklist):

    def empty():
        return []
    
    def insert(q, W):
        return W + [q]
            
    def extract(W):
        return (W[0], W[1:])
    
class ImprovedRoundRobin(Worklist):
    
    def empty():
        return []
    
    def insert(q, W):
        if q in W[0]:
            return W
        else:
            return (W[0], W[1] + [q])
            
    def extract(W):
        if W[0] is None:
            VrP = sorted(W[1])
            q = VrP[1:]
            V1 = VrP[:-1]
            return (q, (V1, []))
        else:
            q = W[0][1:]
            V1 = W[0][:-1]
            return (q, (V1, W[1]))
    