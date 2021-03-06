# -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:24:49 2018

@author: msb
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.optimize
import math
import os

# Needs correction
def P_onedraw(w, start_conc, draw_size):
    
    Q4_s = start_conc[0]
    Q3_s = start_conc[1]
    Q2_s = start_conc[2]
    Q1_s = start_conc[3]
    Q0_s = start_conc[4]
    
    p4 = Q4_s*w[0] / ((Q4_s*w[0])+(Q3_s*w[1])+(Q2_s*w[2])+(Q1_s*w[3]))
    p3 = Q3_s*w[1] / ((Q4_s*w[0])+(Q3_s*w[1])+(Q2_s*w[2])+(Q1_s*w[3]))
    p2 = Q2_s*w[2] / ((Q4_s*w[0])+(Q3_s*w[1])+(Q2_s*w[2])+(Q1_s*w[3]))
    p1 = Q1_s*w[3] / ((Q4_s*w[0])+(Q3_s*w[1])+(Q2_s*w[2])+(Q1_s*w[3]))
    
    p4 = p4*draw_size
    p3 = p3*draw_size
    p2 = p2*draw_size
    p1 = p1*draw_size
    
    if Q4_s - p4 < 0:
        next_Q4 = 0
    else:
        next_Q4 = Q4_s - p4

    if Q3_s + p4 - p3 < 0:
        next_Q3 = 0
    else:
        next_Q3 = Q3_s + p4 - p3

    if Q2_s + p3 - p2 < 0:
        next_Q2 = 0
    else:
        next_Q2 = Q2_s + p3 - p2

    if Q1_s + p2 - p1 < 0:
        next_Q1 = 0
    else:
        next_Q1 = Q1_s + p2 - p1

    if Q0_s + p1 < 0:
        next_Q0 = 0
    else:
        next_Q0 = Q0_s + p1
        
    return next_Q4, next_Q3, next_Q2, next_Q1, next_Q0

def P_draw(H1, frac = None, s_plt = False, s_dat = False, p = False):
    """
    This function will plot the SRO scale structural evolution of silicate 
    glasses by accounting for the enthalpic and entropic contributons to 
    modifier-former interactions.
    
 =============================================================================
    model(H1, H2 = None, frac = None, s_plt = False, s_dat = False)
 =============================================================================
    
    where H1 is the necessary enthalpic contribution in a bunary glass. 
    Examples are provided: "module.HNaSi", "module.HKSi", "module.HLiSi".
    
    H2 may be set to enthalpy values for a second modifier, where frac defines
    the fraction of the first to second modifier (0-1). 
    
    s_plt and s_dat may be set to "True" to save the plot and data as png and
    csv files
    

    Example:

    >>> model(HNaSi, H2 = HLiSi, frac = 0.6, s_plt = True, s_dat = True)
    """
    draw_nr = list(range(300))
    draw_ar = np.array(draw_nr)
    
            
    M2O = []
            
    for i in draw_ar:
        next_mod = draw_ar[i] / (100 + draw_ar[i]) * 100
        M2O.append(next_mod)
        
    M2O.append(75) 
    M2Onp = np.array(M2O)

    Tg = np.array(0.00016808*M2Onp**4 - 0.023995*M2Onp**3 + 1.18355*M2Onp**2 - 23.1234*M2Onp + 359.112)   
   
    w_Q3 = []
    w_Q2 = []
    w_Q1 = []
    
    if frac is None:

        H = [0, H1[0], H1[1]]

        for i in draw_ar:
            next_w_Q3 = math.exp(-H[0]/(Tg[i]*0.00831))
            w_Q3.append(next_w_Q3)

            next_w_Q2 = math.exp(-H[1]/(Tg[i]*0.00831))
            w_Q2.append(next_w_Q2)

            next_w_Q1 = math.exp(-H[2]/(Tg[i]*0.00831))
            w_Q1.append(next_w_Q1)
            
        Q3 = [100, ]
        Q2 = [0, ]
        Q1 = [0, ]
        Q0 = [0, ]
    
        for i in draw_ar:
    
            p3 = Q3[-1]*w_Q3[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
            p2 = Q2[-1]*w_Q2[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
            p1 = Q1[-1]*w_Q1[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
    
    
            if Q3[-1] - p3 < 0:
                next_Q3 = 0
            else:
                next_Q3 = Q3[-1] - p3
    
            if Q2[-1] + p3 - p2 < 0:
                next_Q2 = 0
            else:
                next_Q2 = Q2[-1] + p3 - p2
    
            if Q1[-1] + p2 - p1 < 0:
                next_Q1 = 0
            else:
                next_Q1 = Q1[-1] + p2 - p1
    
            if Q0[-1] + p1 < 0:
                next_Q0 = 0
            else:
                next_Q0 = Q0[-1] + p1
    
            Q3.append(next_Q3)
            Q2.append(next_Q2)
            Q1.append(next_Q1)
            Q0.append(next_Q0)

    elif type(H1) is tuple:
        w_Na_Q3 = []
        w_Na_Q2 = []
        w_Na_Q1 = []
        
        w_K_Q3 = []
        w_K_Q2 = []
        w_K_Q1 = []
        
        for i in draw_ar:


            next_w_Na_Q3 = ((math.exp(-H1[1][0]/(Tg[i]*0.00831))))
            w_Na_Q3.append(next_w_Na_Q3)
            
            next_w_Na_Q2 = ((math.exp(-H1[1][1]/(Tg[i]*0.00831))))
            w_Na_Q2.append(next_w_Na_Q2)
            
            next_w_Na_Q1 = ((math.exp(-H1[1][2]/(Tg[i]*0.00831))))
            w_Na_Q1.append(next_w_Na_Q1)
            
            next_w_K_Q3 = ((math.exp(-H1[0][0]/(Tg[i]*0.00831))))
            w_K_Q3.append(next_w_K_Q3)
            
            next_w_K_Q2 = ((math.exp(-H1[0][1]/(Tg[i]*0.00831))))
            w_K_Q2.append(next_w_K_Q2)
            
            next_w_K_Q1 = ((math.exp(-H1[0][2]/(Tg[i]*0.00831))))
            w_K_Q1.append(next_w_K_Q1)

            
        Q3 = [100, ]
        Q2 = [0, ]
        Q1 = [0, ]
        Q0 = [0, ]
    
        for i in draw_ar:
    
            p3 = ((Q3[-1]*w_K_Q3[i] / ((Q3[-1]*w_K_Q3[i])+(Q2[-1]*w_K_Q2[i])+(Q1[-1]*w_K_Q1[i])))*frac[0]) + ((Q3[-1]*w_Na_Q3[i] / ((Q3[-1]*w_Na_Q3[i])+(Q2[-1]*w_Na_Q2[i])+(Q1[-1]*w_Na_Q1[i])))*frac[1])
            p2 = ((Q2[-1]*w_K_Q2[i] / ((Q3[-1]*w_K_Q3[i])+(Q2[-1]*w_K_Q2[i])+(Q1[-1]*w_K_Q1[i])))*frac[0]) + ((Q2[-1]*w_Na_Q2[i] / ((Q3[-1]*w_Na_Q3[i])+(Q2[-1]*w_Na_Q2[i])+(Q1[-1]*w_Na_Q1[i])))*frac[1])
            p1 = ((Q1[-1]*w_K_Q1[i] / ((Q3[-1]*w_K_Q3[i])+(Q2[-1]*w_K_Q2[i])+(Q1[-1]*w_K_Q1[i])))*frac[0]) + ((Q1[-1]*w_Na_Q1[i] / ((Q3[-1]*w_Na_Q3[i])+(Q2[-1]*w_Na_Q2[i])+(Q1[-1]*w_Na_Q1[i])))*frac[1])
    
    
            if Q3[-1] - p3 < 0:
                next_Q3 = 0
            else:
                next_Q3 = Q3[-1] - p3

            if Q2[-1] + p3 - p2 < 0:
                next_Q2 = 0
            else:
                next_Q2 = Q2[-1] + p3 - p2
    
            if Q1[-1] + p2 - p1 < 0:
                next_Q1 = 0
            else:
                next_Q1 = Q1[-1] + p2 - p1

            if Q0[-1] + p1 < 0:
                next_Q0 = 0
            else:
                next_Q0 = Q0[-1] + p1
    
            Q3.append(next_Q3)
            Q2.append(next_Q2)
            Q1.append(next_Q1)
            Q0.append(next_Q0)

    else:
        return print("Wrong H format")
    if s_plt is False and p is True:
        plt.plot(M2O, Q3, 'r-', M2O, Q2, 'k-', M2O, Q1, 'b-', M2O, Q0, 'g-',)
        plt.axis([0, 75, 0, 100])
        plt.legend(["$Q^3$","$Q^2$","$Q^1$","$Q^0$"])
        plt.xlabel("Modifier mol %")
        plt.ylabel(f"Qn species concentration")
        plt.title('Qn distribution')
        plt.show()

    if s_plt is True:
        if not os.path.exists("P2O5_Structure"):
            os.mkdir("P2O5_Structure")
        plt.plot(M2O, Q3, 'r-', M2O, Q2, 'k-', M2O, Q1, 'b-', M2O, Q0, 'g-',)
        plt.axis([0, 75, 0, 100])
        plt.legend(["$Q^3$","$Q^2$","$Q^1$","$Q^0$"])
        plt.xlabel("Modifier mol %")
        plt.ylabel(f"Qn species concentration")
        plt.title('Qn distribution')
        plt.savefig(os.path.join('P2O5_Structure', 'Qn_distribution.png'))
        plt.show()
        
    if s_dat is True:
        if not os.path.exists("P2O5_Structure"):
            os.mkdir("P2O5_Structure")        
        m_data = np.column_stack([M2O, Q3, Q2, Q1, Q0])
        np.savetxt(os.path.join('P2O5_Structure', "Model_data.csv"), m_data)
        
    elif s_plt is False and s_dat is False and p is False:
        return M2O, Q3, Q2, Q1, Q0

def P_SSE(H1,  data, frac = None, s_plt = False, s_dat = False, p = False):
    """
    This function will plot the SRO scale structural evolution of silicate 
    glasses by accounting for the enthalpic and entropic contributons to 
    modifier-former interactions.
    
 =============================================================================
    model(H1, H2 = None, frac = None, s_plt = False, s_dat = False)
 =============================================================================
    
    where H1 is the necessary enthalpic contribution in a bunary glass. 
    Examples are provided: "module.HNaSi", "module.HKSi", "module.HLiSi".
    
    H2 may be set to enthalpy values for a second modifier, where frac defines
    the fraction of the first to second modifier (0-1). 
    
    s_plt and s_dat may be set to "True" to save the plot and data as png and
    csv files
    

    Example:

    >>> model(HNaSi, H2 = HLiSi, frac = 0.6, s_plt = True, s_dat = True)
    """
    
    mod_data = data[0]
    Q3_data = data[1]
    Q2_data = data[2]
    Q1_data = data[3]
    Q0_data = data[4]
    
    M2O, Q3, Q2, Q1, Q0 = P_draw(H1, frac)
            

    if s_plt is False and p is True:
        plt.plot(M2O, Q3, 'r-', M2O, Q2, 'k-', M2O, Q1, 'b-', M2O, Q0, 'g-',)
        plt.plot(mod_data, Q3_data, 'rd', mod_data, 
                 Q2_data, 'kd', mod_data, Q1_data, 'bd', mod_data, Q0_data, 'gd',)
        plt.axis([0, 75, 0, 100])
        plt.legend(["$Q^3$","$Q^2$","$Q^1$","$Q^0$"])
        plt.xlabel("Modifier mol %")
        plt.ylabel(f"Qn species concentration")
        plt.title('Qn distribution')
        plt.show()

    if s_plt is True:
        if not os.path.exists("P2O5_Structure"):
            os.mkdir("P2O5_Structure")
        plt.plot(M2O, Q3, 'r-', M2O, Q2, 'k-', M2O, Q1, 'b-', M2O, Q0, 'g-',)
        plt.plot(mod_data, Q3_data, 'rd', mod_data, 
                 Q2_data, 'kd', mod_data, Q1_data, 'bd', mod_data, Q0_data, 'gd',)
        plt.axis([0, 75, 0, 100])
        plt.legend(["$Q^3$","$Q^2$","$Q^1$","$Q^0$"])
        plt.xlabel("Modifier mol %")
        plt.ylabel(f"Qn species concentration")
        plt.title('Qn distribution')
        plt.savefig(os.path.join('P2O5_Structure', 'Qn_distribution.png'))
        plt.show()
        
    if s_dat is True:
        if not os.path.exists("P2O5_Structure"):
            os.mkdir("P2O5_Structure")        
        m_data = np.column_stack([M2O, Q3, Q2, Q1, Q0])
        np.savetxt(os.path.join('P2O5_Structure', "Model_data.csv"), m_data)
        
    if p is False:
        mod_m = []
        Q3_m = []
        Q2_m = []
        Q1_m = []
        Q0_m = []
    
        
        for i in mod_data:
            next_mod_m = min(M2O, key=lambda x:abs(x-i))
            mod_m.append(next_mod_m)
        
        for i in mod_m:
            ind = M2O.index(i)
            next_Q3_m = Q3[ind]
            Q3_m.append(next_Q3_m)
        
            next_Q2_m = Q2[ind]
            Q2_m.append(next_Q2_m)
        
            next_Q1_m = Q1[ind]
            Q1_m.append(next_Q1_m)

            next_Q0_m = Q0[ind]
            Q0_m.append(next_Q0_m)
            
        
        Q3_m = np.array(Q3_m)
        Q2_m = np.array(Q2_m)
        Q1_m = np.array(Q1_m)
        Q0_m = np.array(Q0_m)
     
        
        SSE = sum(((Q3_data - Q3_m)**2)+((Q2_data - Q2_m)**2)+
                  ((Q1_data - Q1_m)**2)+((Q0_data - Q0_m)**2))
        
        return SSE
    
def P_engine(fil, data, it = 10):
    dat = data
    w0 = [20, 30]

    minimizer_kwargs = {"method": "COBYLA", "args": (dat,)}
    res = scipy.optimize.basinhopping(P_SSE, w0, niter=it, T=2.0, stepsize=1, 
                                       minimizer_kwargs=minimizer_kwargs, take_step=None, 
                                       accept_test=None, callback=None, interval=50, 
                                       disp=True, niter_success=None, seed=None)
    
    return res.x












# fil = 'ZnO_phosphate'

# mod_data = []
# Q3_data = []
# Q2_data = []
# Q1_data = []
# Q0_data = []

# with open(f"{fil}.csv", newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
#     for row in spamreader:
#         mod_data.append(row[0])
#         Q3_data.append(row[1])
#         Q2_data.append(row[2])
#         Q1_data.append(row[3])
#         Q0_data.append(row[4])
        
# mod_data = [float(i) for i in mod_data]
# Q3_data = [float(i) for i in Q3_data]
# Q2_data = [float(i) for i in Q2_data]
# Q1_data = [float(i) for i in Q1_data]
# Q0_data = [float(i) for i in Q0_data]

# Q3_data = np.array(Q3_data)
# Q2_data = np.array(Q2_data)
# Q1_data = np.array(Q1_data)
# Q0_data = np.array(Q0_data)

# draw_nr = list(range(300))
# draw_ar = np.array(draw_nr)
        
# M2O = []
        
# for i in draw_ar:
#     next_mod = draw_ar[i] / (100 + draw_ar[i]) * 100
#     M2O.append(next_mod)
    
# M2O.append(75) 
# M2Onp = np.array(M2O)

# #This estimate of the Tg must be changed for each type of phosphate system. 
# #This one is only true for the ZnO-P2O5 system

# Tg = np.array(0.00016808*M2Onp**4 - 0.023995*M2Onp**3 + 1.18355*M2Onp**2 - 23.1234*M2Onp + 359.112)    

# def P_draw(H1):
     
#     draw_nr = list(range(300))
#     draw_ar = np.array(draw_nr)
    
#     M2O = []
        
#     for i in draw_ar:
#         next_mod = draw_ar[i] / (100 + draw_ar[i]) * 100
#         M2O.append(next_mod)
        
#     M2O.append(75) 
        
#     H = np.array([0, H1[0], H1[1]])
#                 #M1 = np.array((draw_ar/(100+draw_ar))*100)
                
# #                w1 = [1, 0.01, 0.001]
    
#     w_Q3 = []
#     w_Q2 = []
#     w_Q1 = []
    
#     for i in draw_ar:
#         next_w_Q3 = math.exp(-H[0]/(Tg[i]*8.31))
#         if next_w_Q3 < 1e-20:
#             return 100000
#         else:
#             w_Q3.append(next_w_Q3)
        
#     for i in draw_ar:
#         next_w_Q2 = math.exp(-H[1]/(Tg[i]*8.31))
#         if next_w_Q2 < 1e-20:
#             return 100000
#         else: 
#             w_Q2.append(next_w_Q2)
        
#     for i in draw_ar:
#         next_w_Q1 = math.exp(-H[2]/(Tg[i]*8.31))
#         if next_w_Q1 < 1e-20:
#             return 100000
#         else:
#             w_Q1.append(next_w_Q1)

        
#     Q3 = [100, ]
#     Q2 = [0, ]
#     Q1 = [0, ]
#     Q0 = [0, ]
#     # The function that makes each iteration at a time


#     for i in draw_ar:
#         try:
#             p3 = Q3[-1]*w_Q3[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#             p2 = Q2[-1]*w_Q2[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#             p1 = Q1[-1]*w_Q1[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#         except ZeroDivisionError:
#             print(f"wQ3: {Q3[-1]}, {w_Q3[i]}, wQ2: {Q2[-1]}, {w_Q2[i]}, wQ1: {Q1[-1]}, {w_Q1[i]}")
        
#         if Q3[-1] - p3 < 0:
#             next_Q3 = 0
#         else:
#             next_Q3 = Q3[-1] - p3
#         if Q2[-1] + p3 - p2 < 0:
#             next_Q2 = 0
#         else:
#             next_Q2 = Q2[-1] + p3 - p2
#         if Q1[-1] + p2 - p1 < 0:
#             next_Q1 = 0
#         else:
#             next_Q1 = Q1[-1] + p2 - p1
#         if Q0[-1] + p1 < 0:
#             next_Q0 = 0
#         else:
#             next_Q0 = Q0[-1] + p1
            
#         Q3.append(next_Q3)
#         Q2.append(next_Q2)
#         Q1.append(next_Q1)
#         Q0.append(next_Q0)
    
#     #Vi laver lister, som indeholer data fra modellen, som svarer til de punkter, 
#     #hvor vi har experimentiel data
#     mod_m = []
#     Q3_m = []
#     Q2_m = []
#     Q1_m = []
#     Q0_m = []
    
#     for i in mod_data:
#         next_mod_m = min(M2O, key=lambda x:abs(x-i))
#         mod_m.append(next_mod_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q3_m = Q3[ind]
#         Q3_m.append(next_Q3_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q2_m = Q2[ind]
#         Q2_m.append(next_Q2_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q1_m = Q1[ind]
#         Q1_m.append(next_Q1_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q0_m = Q0[ind]
#         Q0_m.append(next_Q0_m)
    
#     Q3 = np.array(Q3)
#     Q3_m = np.array(Q3_m)
    
#     Q2_m = np.array(Q2_m)
    
#     Q1_m = np.array(Q1_m)
    
#     Q0_m = np.array(Q0_m)
    
    
    
#     SSE = sum(((Q3_data - Q3_m)**2) + ((Q2_data - Q2_m)**2) + ((Q1_data - Q1_m)**2) + ((Q0_data - Q0_m)**2))
    
#     return SSE
# H1 = [55, 85]
# #res = scipy.optimize.minimize(model, w0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})

# class MyBounds(object):
#     def __init__(self, xmax=[200000., 200000.], xmin=[0., 0.] ):
#         self.xmax = np.array(xmax)
#         self.xmin = np.array(xmin)
#     def __call__(self, **kwargs):
#         x = kwargs["x_new"]
#         tmax = bool(np.all(x <= self.xmax))
#         tmin = bool(np.all(x >= self.xmin))
#         return tmax and tmin

# mybounds = MyBounds()

# res = scipy.optimize.basinhopping(model, H1, niter=10, T=1.0, stepsize=10, minimizer_kwargs=None, take_step=None, accept_test=mybounds, callback=None, interval=50, disp=True, niter_success=None, seed=None)

# sterr = np.sqrt(np.diag(res.lowest_optimization_result.hess_inv))

# #Now, to plot it :

# def model(H1):
    
#     H = np.array([0, H1[0], H1[1]])
#                 #M1 = np.array((draw_ar/(100+draw_ar))*100)
                
# #                w1 = [1, 0.01, 0.001]
    
#     w_Q3 = []
#     w_Q2 = []
#     w_Q1 = []
    
#     for i in draw_ar:
#         next_w_Q3 = math.exp(-H[0]/(Tg[i]*8.31))
#         if next_w_Q3 < 1e-20:
#             return 100000
#         else:
#             w_Q3.append(next_w_Q3)
        
#     for i in draw_ar:
#         next_w_Q2 = math.exp(-H[1]/(Tg[i]*8.31))
#         if next_w_Q2 < 1e-20:
#             return 100000
#         else: 
#             w_Q2.append(next_w_Q2)
        
#     for i in draw_ar:
#         next_w_Q1 = math.exp(-H[2]/(Tg[i]*8.31))
#         if next_w_Q1 < 1e-20:
#             return 100000
#         else:
#             w_Q1.append(next_w_Q1)

        
#     Q3 = [100, ]
#     Q2 = [0, ]
#     Q1 = [0, ]
#     Q0 = [0, ]
#     # The function that makes each iteration at a time


#     for i in draw_ar:
#         try:
#             p3 = Q3[-1]*w_Q3[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#             p2 = Q2[-1]*w_Q2[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#             p1 = Q1[-1]*w_Q1[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#         except ZeroDivisionError:
#             print(f"wQ3: {Q3[-1]}, {w_Q3[i]}, wQ2: {Q2[-1]}, {w_Q2[i]}, wQ1: {Q1[-1]}, {w_Q1[i]}")
        
#         if Q3[-1] - p3 < 0:
#             next_Q3 = 0
#         else:
#             next_Q3 = Q3[-1] - p3
#         if Q2[-1] + p3 - p2 < 0:
#             next_Q2 = 0
#         else:
#             next_Q2 = Q2[-1] + p3 - p2
#         if Q1[-1] + p2 - p1 < 0:
#             next_Q1 = 0
#         else:
#             next_Q1 = Q1[-1] + p2 - p1
#         if Q0[-1] + p1 < 0:
#             next_Q0 = 0
#         else:
#             next_Q0 = Q0[-1] + p1
            
#         Q3.append(next_Q3)
#         Q2.append(next_Q2)
#         Q1.append(next_Q1)
#         Q0.append(next_Q0)
    
#     #Vi laver lister, som indeholer data fra modellen, som svarer til de punkter, 
#     #hvor vi har experimentiel data
#     mod_m = []
#     Q3_m = []
#     Q2_m = []
#     Q1_m = []
#     Q0_m = []
    
#     for i in mod_data:
#         next_mod_m = min(M2O, key=lambda x:abs(x-i))
#         mod_m.append(next_mod_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q3_m = Q3[ind]
#         Q3_m.append(next_Q3_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q2_m = Q2[ind]
#         Q2_m.append(next_Q2_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q1_m = Q1[ind]
#         Q1_m.append(next_Q1_m)
    
#     for i in mod_m:
#         ind = M2O.index(i)
#         next_Q0_m = Q0[ind]
#         Q0_m.append(next_Q0_m)
    
#     Q3 = np.array(Q3)
#     Q3_m = np.array(Q3_m)
    
#     Q2_m = np.array(Q2_m)
    
#     Q1_m = np.array(Q1_m)
    
#     Q0_m = np.array(Q0_m)
    
    
    
#     SSE = sum(((Q3_data - Q3_m)**2) + ((Q2_data - Q2_m)**2) + ((Q1_data - Q1_m)**2) + ((Q0_data - Q0_m)**2))



# H = np.array([0, res.x[0], res.x[1]])


# w_Q3 = []
# w_Q2 = []
# w_Q1 = []

# for i in draw_ar:
#     next_w_Q3 = math.exp(-H[0]/(Tg[i]*8.31))
#     w_Q3.append(next_w_Q3)
    
# for i in draw_ar:
#     next_w_Q2 = math.exp(-H[1]/(Tg[i]*8.31))
#     w_Q2.append(next_w_Q2)
    
# for i in draw_ar:
#     next_w_Q1 = math.exp(-H[2]/(Tg[i]*8.31))
#     w_Q1.append(next_w_Q1)


# Q3 = [100, ]
# Q2 = [0, ]
# Q1 = [0, ]
# Q0 = [0, ]
# # The function that makes each iteration at a time

    
# for i in draw_ar:
#     p3 = Q3[-1]*w_Q3[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#     p2 = Q2[-1]*w_Q2[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))
#     p1 = Q1[-1]*w_Q1[i] / ((Q3[-1]*w_Q3[i])+(Q2[-1]*w_Q2[i])+(Q1[-1]*w_Q1[i]))

#     if Q3[-1] - p3 < 0:
#         next_Q3 = 0
#     else:
#         next_Q3 = Q3[-1] - p3
#     if Q2[-1] + p3 - p2 < 0:
#         next_Q2 = 0
#     else:
#         next_Q2 = Q2[-1] + p3 - p2
#     if Q1[-1] + p2 - p1 < 0:
#         next_Q1 = 0
#     else:
#         next_Q1 = Q1[-1] + p2 - p1
#     if Q0[-1] + p1 < 0:
#         next_Q0 = 0
#     else:
#         next_Q0 = Q0[-1] + p1
            
#     Q3.append(next_Q3)
#     Q2.append(next_Q2)
#     Q1.append(next_Q1)
#     Q0.append(next_Q0)

# mod_m = []
# Q3_m = []
# Q2_m = []
# Q1_m = []
# Q0_m = []
    
# for i in mod_data:
#     next_mod_m = min(M2O, key=lambda x:abs(x-i))
#     mod_m.append(next_mod_m)

# for i in mod_m:
#     ind = M2O.index(i)
#     next_Q3_m = Q3[ind]
#     Q3_m.append(next_Q3_m)

# for i in mod_m:
#     ind = M2O.index(i)
#     next_Q2_m = Q2[ind]
#     Q2_m.append(next_Q2_m)

# for i in mod_m:
#     ind = M2O.index(i)
#     next_Q1_m = Q1[ind]
#     Q1_m.append(next_Q1_m)

# for i in mod_m:
#     ind = M2O.index(i)
#     next_Q0_m = Q0[ind]
#     Q0_m.append(next_Q0_m)

# Q3 = np.array(Q3)
# Q3_data = np.array(Q3_data)
# Q3_m = np.array(Q3_m)

# Q2_data = np.array(Q2_data)
# Q2_m = np.array(Q2_m)

# Q1_data = np.array(Q1_data)
# Q1_m = np.array(Q1_m)

# Q0_data = np.array(Q0_data)
# Q0_m = np.array(Q0_m)

# SSE = sum(((Q3_data - Q3_m)**2) + ((Q2_data - Q2_m)**2) + ((Q1_data - Q1_m)**2) + ((Q0_data - Q0_m)**2))

# if not os.path.exists(f"{fil}_H_model"):
#         os.mkdir(f"{fil}_H_model")

# plt.plot(M2O, Q3, 'r-', M2O, Q2, 'b-', M2O, Q1, 'g-', M2O, Q0, 'y-',)
# plt.plot(mod_data, Q3_data, 'rd', mod_data, Q2_data, 'bd', mod_data, Q1_data, 'gd', mod_data, Q0_data, 'yd',)
# plt.axis([0, 75, 0, 100])
# plt.xlabel("Modifier mol %")
# plt.ylabel(f"Qn species concentration")
# plt.title('Qn distribution')
# plt.savefig(os.path.join(f'{fil}_H_model', f'{fil}.png'))
# plt.show()

# m_data = np.column_stack([M2O, Q3, Q2, Q1, Q0])
# np.savetxt(os.path.join(f'{fil}_H_model', f"Model data {fil}.csv"), m_data)

# print(f"Parameters: {H}")
# print(f"SSE: {SSE}")
# print(f"Standard errors for the parameters: {sterr}")

