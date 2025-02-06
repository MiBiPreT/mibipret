#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 12:43:45 2024

@author: alraune
"""

import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


lum77 = np.array([0.52,0.09,0.114,0.027,0.12,0.11,0.019])
lum77_names = ['PAHs (3-ring)','PAHs (2-ring)','non-volatile aromates','volatile aromates','N-heterocyclic\n carbenes','oxidized\n compounds','rest']
print(np.sum(lum77))

plt.figure(figsize=[4.2,3])
plt.pie(lum77,labels = lum77_names,startangle=180,explode=[0,0.1,0,0,0,0,0])
# plt.title('Source composition')
plt.tight_layout()
plt.savefig('Fig_source.png',dpi = 300)
