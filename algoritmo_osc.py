import numpy as np
from scipy.integrate import odeint 


#Rearranjando a função dada no exercício temos:
    
    # x''(t) + E*(x**2 - 1)*x'(t) + x(t) = 0  
    
    #substituindo x' por v: (mudança de variáveis!)
    
    # x'(t) = v(t)
    # v'(t) = -E*(x**2 - 1)*v(t) - x(t) 
    
    # y será o vetor [x,v]
    

def osc(y, t, E):
    x, v = y
    dydt = [v, -E*((x**2) - 1)*v - x]
    return dydt


def oscilador_de_van_der_Pol(E, s0, v0, t_min, t_max, n_pontos):
    
    
    y0 = [s0, v0] #vetor cond. inicial
    
    t = np.linspace(t_min, t_max, n_pontos) #tempo de 0 à 8 pi
    
    #chamando a função odeint para gerar a solução: 
        
        
    sol = odeint(osc, y0, t, args = (E,)) 

    #obs: 
    
    #caso houvessem constantes multiplicando os termos da edo exemplo:
    # x''(t) + b*x'(t) + c*x = 0
    
    # a função odeint chamada ficaria:
    #sol = odeint(osc, y0, t, args=(b,c)) 
    
    s = sol[:, 0]  
    v = sol[:, 1]
    
    return s, v, t
