import numpy as np

class Stress():
    '''class definition for a stress tensor object
    Dependencies: numpy as np'''
    def __init__(self, sx, sy=0, sz=0, sxy=0, syz=0, sxz=0):
        '''initialises the stress tensor'''
        #getting a numpy array of the stress components
        self.S = np.array([sx, sxy, sxz, sxy, sy, syz, sxz, syz, sz]).\
        reshape(3,3) #getting a 3x3 tensor
        
    def __repr__(self):
        '''returns representation of the stress tensor'''
        return "Stress(" + "{:.2f}".format(self.S[0][0]) + "," + \
        "{:.2f}".format(self.S[1][1]) + "," + \
        "{:.2f}".format(self.S[2][2]) + "," + "{:.2f}".format(self.S[0][1]) + "," + \
        "{:.2f}".format(self.S[1][2]) + "," + "{:.2f}".format(self.S[0][2]) + ")"
        
    def __str__(self):
        '''prints the stress tensor'''
        return "\nStress Tensor: \n" + str(self.S)
    
    def __add__(self, other):
        '''adds the stress components and returns a stress tensor'''
        return Stress(self.S[0][0] + other.S[0][0], self.S[1][1] + other.S[1][1], \
                      self.S[2][2] + other.S[2][2], self.S[0][1] + other.S[0][1], \
                      self.s[1][2] + other.S[1][2], self.S[0][2] + other.S[0][2])
        
    def __sub__(self, other):
        '''subtracts components of stress and returns a stress tensor'''
        return Stress(self.S[0][0] - other.S[0][0], self.S[1][1] - other.S[1][1], \
                      self.S[2][2] - other.S[2][2], self.S[0][1] - other.S[0][1], \
                      self.S[1][2] - other.S[1][2], self.S[0][2] - other.S[0][2])
    
    def scale(self, k):
        '''returns scaled stresses'''
        return Stress(k*self.S[0][0], k*self.S[1][1], k*self.S[2][2],\
                      k*self.S[0][1], k*self.S[1][2], k*self.S[0][2])
    
    def vonmises(self):
        '''returns the Von Mises stress for a stress tensor'''
        dir_terms = (self.S[0][0] - self.S[1][1])**2 + (self.S[1][1] - \
                    self.S[2][2])**2 + (self.S[2][2] - self.S[0][0])**2
        shear_terms = self.S[0][1]**2 + self.S[1][2]**2 + self.S[0][2]**2
        return np.sqrt(dir_terms + 6*shear_terms)/np.sqrt(2)
    
    def srange(self, other):
        '''returns the equivalent stress range using the stress components'''
        return (self - other).vonmises()
    
    def invariant(self):
        '''returns a tuple containing three stress invariants'''
        #Refer Roark's 7ed, Section 2.3, Page 25
        #I1 = self.sx + self.sy + self.sz
        #I3 = self.sx*self.sy*self.sz + 2*self.sxy*self.syz*self.sxz - \
        #self.sx*self.syz**2 - self.sy*self.sxz**2 - self.sz*self.sxy**2
        I1 = np.trace(self.S)
        I2 = self.S[0][0]*self.S[1][1] + self.S[1][1]*self.S[2][2] + self.S[2][2]*self.S[0][0] - \
        self.S[0][1]**2 - self.S[1][2]**2 - self.S[0][2]**2
        I3 = np.linalg.det(self.S)
        return (I1,I2,I3)
    
    def principal(self):
        '''returns a tuple of Principal stresses - min, mid, max
        S^3 - I1.S^2 + I2.S - I3 = 0'''
        prinStress = sorted(np.roots([1] + list(self.invariant())), reverse = True)
        return Stress(prinStress[0], prinStress[1], prinStress[2])
