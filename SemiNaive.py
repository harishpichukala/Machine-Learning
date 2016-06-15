import math
import numpy as np
from heapq import nlargest
import sys
import itertools
class SemiNaive:

    def __init__(self,face_sample_size,number_cut_off,sgSize):
        #self.face_sample_size = face_sample_size
        #self.number_cut_off = number_cut_off
        #self.groupsize = sgSize
		self.Facesize=face_sample_size
        self.numcutoff=number_cut_off
        self.groupsize=sgSize
    def kth_largest(self,lst,k):
        indexes=range(len(lst))
        return nlargest(k,indexes,key=lambda i: lst[i])[k-1]
        
    def subgroup1(self,m):
        d=[]
        pos=[]
        for i in range(len(m)):
            for j in range(len(m[0])):
                if i==j:
                    d.append(m[i][j])
                    pos.append(i)
        return pos
        
    def largest_matrix(self,m,sz):
        lg=[]
        pos=[]
        c=len(m[0])
        r=len(m)
        for j in range(r):
            lg.append(self.kth_largest(m[j],sz))
        return lg
    def get_cpair(self,face,i,j):
        characters=''.join(str(l) for l in self.features_values)
        length=2
        l1=[]
        for p in itertools.product(characters,repeat=length):
            l=[]
            for x in p:
                l.append(int(x))
            l1.append(l)
        
        self.l1=l1
        pt = l1
        
        #print l1
        
        tp=[]
        for k in range(len(face)):
            tp.append((face[k][i],face[k][j]))
        
        
        #print tp
        
        s=list(set(tp))
        tup_count={}
        j1=0
        for i in s:
            tup_count[j1]=tp.count(i)
            j1=j1+1
        print "pt is "
        print pt
		print len(pt)
        for h in s:
            for i in range(len(pt)):
                for j in range(len(pt[0])):
                    if pt[i][j] is h:
                        pt[i][j]=tup_count[s.index(h)]
                    
        for i in range(len(pt)):
            for j in range(len(pt[0])):
                if type(pt[i][j]) is not int:
                    pt[i][j]=0
        return pt
    
    def probabilityxiw1(self,p,q):
        try:
            out=coefficient_tb_class_faces[p][q]/2.
        except:
            return 0
        return out

    def probabilityxiw2(self,p,q):
        try:
            out=coefficient_tb_class_nonfaces[p][q]/2.
        except:
            return 0
        return out

    def probabilityxixjw1(self,i,j,m,n):
        try:
            res=coefficient_pair_tb_faces[i][j][m][n]/2.
        except:
            return 0
        return res

    def probabilityxixjw2(self,i,j,m,n):
        try:
            res=coefficient_pair_tb_nonfaces[i][j][m][n]/2.
        except:
            return 0
        return res

    def probabilityxixj(self,i,j,m,n):
        try:
            res=coefficient_pair_tb_faces[i][j][m][n]+coefficient_pair_tb_nonfaces[i][j][m][n]
            res1 = (res/4.)
        except:
            return 0
        return res1
        
        
    def coefficient_pair_function(self,size,face):
        copair_table = [[] for t in range(size)]
        
        
        for i in range(len(self.faces)):
            cpair=[]
            for i in range(len(self.features_values)):
                t=[]
                for j in range(len(self.features_values)):
                    t.append(0)
                cpair.append(t)
            for j in range(size):
                
                cpair=self.get_cpair(face,i,j)
                
                copair_table[i].append(cpair)
        return copair_table
        
    
    def Subgroup(self,i):
        sub=[]
        for sz in range(len(i[0])-1):
            if sz==0:
                sub.append(self.subgroup1(i))
            else:
                sub.append(self.largest_matrix(i,sz))
        return sub
        
    def train(self,faces,nonfaces,model):
        self.faces = faces
        self.nonfaces = nonfaces
        self.model = model
        
        features_values=[]
        features_values=set(features_values)
        for i in self.faces:
            features_values=features_values.union(i)
        for i in self.nonfaces:
            features_values=features_values.union(i)
        
        self.features_values=list(features_values)
        #print("the feature values are")
        #print features_values
        e=(np.finfo(np.float).eps)*7.9
        global coefficient_pair_tb_faces
        global coefficient_pair_tb_nonfaces
        global coefficient_tb_class_faces
        global coefficient_tb_class_nonfaces 
        coefficient_tb_class_faces = [[] for t in range(len(faces[0]))]
        coefficient_tb_class_nonfaces =  [[] for t in range(len(nonfaces[0]))]
        M=[[] for t in range(len(faces[0]))]
        size_faces = 0
        size_faces = len(faces[0])
        size_non_faces = len(nonfaces[0])
        feature_count=len(self.features_values)
        for i in range(size_faces):
             for k in self.features_values:
                count=0
                for j in range(len(self.faces)):
                    #count=0
                    
                    if self.faces[j][i] is k:
                        count=count+1
                coefficient_tb_class_faces[i].append(count)  
             #coefficient_tb_class_faces[i].append(oc)
            
        for i in range(size_non_faces):
            for k in self.features_values:
                count=0
                for j in range(len(self.nonfaces)):
                    #count=0
                    
                    if self.nonfaces[j][i] is k:
                        count=count+1
                coefficient_tb_class_nonfaces[i].append(count)  
            
        print("coefficient count are:\n")
        print(coefficient_tb_class_faces)
        print(coefficient_tb_class_nonfaces)
       
        coefficient_pair_tb_faces = self.coefficient_pair_function(size_faces,self.faces)
       
        
        coefficient_pair_tb_nonfaces = self.coefficient_pair_function(size_non_faces,self.nonfaces)
        
        for i in range(len(coefficient_pair_tb_faces)):
       
            for j in range(len(coefficient_pair_tb_faces)):
                s=0
                p_1=0
                p_2=0
                p_3=0
                p_4=0
                p_5=0
                for m in range(2):
                    for n in range(2):
                        p_1 =p_1 +self.probabilityxixj(i,j,m,n)
                        #print p_1
                    
                        try:
                            val=(self.probabilityxixjw1(i,j,m,n))/(self.probabilityxixjw2(i,j,m,n))
                        except ZeroDivisionError:
                            val=0
                        
                        p_2=p_2+math.log(max(val,e))
                        
                    
                        try:
                            val=((self.probabilityxiw1(i,m))*(self.probabilityxiw1(j,n)))/((self.probabilityxiw2(i,m))*(self.probabilityxiw2(j,n)))
                        except ZeroDivisionError:
                            val=0
                        p_3=p_3+math.log(max(val,e))
                    
                        p_4 =p_4+abs(p_2-p_3)
                    
                        p_5=p_5+p_1*p_4
                        s = s+p_5
                    
                        p_1=0
                        p_2=0
                        p_3=0
                        p_4=0
                        p_5=0
                    
                
                M[i].append(s)
                
     
        G=self.Subgroup(M)
        self.G=G[0:self.groupsize]
        print "sub groups"
        print self.G
        self.P1=self.ProbabilityTable(G,self.faces)
        self.P2=self.ProbabilityTable(G,self.nonfaces)
        print self.P1
        print self.P2
		model.setSubgroupSize(self.groupsize)
        model.setDataSize(self.Facesize)#length of faces.shape[0]
        model.setNumClass1(len(faces[0]))#no.of samples faces
        model.setNumClass2(len(nonfaces[0]))#no. of samples nfaces
        model.setSubgroups(p)#s
        print "mdel.get from subgroup"
        print model.getSubgroups()
        model.setTableClass1(self.P1)
        model.setTableClass2(self.P2)
        model.setGoodness("None")
        model.write()
	def loadModel(self, model):
        kcp = model.read()
        self.groupsize = model.subgroupSize
        self.Facesize = model.dataSize
        self.lenFaces = model.numClass1
        self.lenNonfaces = model.numClass2
        self.group = model.subgroups
        self.probfaces = model.tableClass1
        self.probnonfaces = model.tableClass2
        self.goodness = model.goodness

    def ProbabilityTable(self,sg,pattern):
        v=len(self.features_values)  # no of features values
        self.v=v
        P=[[0 for t in range(len(sg[0]))] for t in range(pow(v,self.groupsize))]
        for i in range(len(sg[0])):
            elements=[]
            for j in range(len(pattern)):
                t=[]
                for k in range(self.groupsize):
                    l=sg[k][i]
                    e=pattern[j][l]
                    t.append(e)
                elements.append(tuple(t))
            
            for a in elements:
                ind=self.l1.index(list(a))
                P[i][ind]=elements.count(a)
        return P
        
    def log_likelihood(self,pm):
        pattern=[]
        for i in range(len(pm)):
            pattern.append(pm)
        pm=pattern
        elements=[]
        elements_1=[]
        elements_2=[]
        for i in range(len(self.G[0])):
            t=[]
            for j in range(self.groupsize):
                l=self.G[j][i]
                e=pm[i][l]
                t.append(e)
            if t in self.l1:
                z=self.l1.index(t)
                elements_1.append(self.P1[i][z])
                elements_2.append(self.P2[i][z])
        
        norm1=[]
        norm2=[]
        for a in elements_1:
                norm1.append(float(a)/2)
        elements.append(norm1)
        for a in elements_2:
                norm2.append(float(a)/2)
        elements.append(norm2)
        #print elements
        epsilon=np.finfo(np.float).eps
        
        lo=[]
        for t in range(len(self.faces[0])):
            if t%3==0:
                if elements[0][t]!=0:
                    d=(elements[0][t]/(elements[1][t]+epsilon))
                else:
                    d=0
        
            if t%3==1:
        
                if elements[1][t]!=0:
                    d=((elements[0][t]+epsilon)/elements[1][t])
                else:
                    d=0
            
            
            if t%3==2:
                if elements[0][t]!=0 and elements[1][t]!=0:
                    d=(elements[0][t]/elements[1][t])
                else:
                    d=0
            lo.append(d)
        return self.logvalue(lo)
        
    def test(self,v):
        norm_values=[]
        for i in v:
            if self.log_likelihood(i)>0:
                print i
                print ":"+"belong to faces"
            if self.log_likelihood(i)<0:
                print i
                print ":"+"belong non-faces"
    
    def logvalue(self,k):
        lkh=0
        for i in k:
            if i!=0:
                lkh+=np.log(i)
        return lkh
    
def face_detection(sfaces,snonfaces,testdata):
    faces=sfaces
    #print("faces is \n")
    #print(faces)
    #print(type(faces))
    nonfaces=snonfaces
    #testfaces=getFacesTest()
    #faces = [[1,1,0,1,2,2,2,0,1],[1,0,1,1,1,2,0,0,2]]
    #nonfaces = [[1,1,1,0,2,1,2,1,1],[2,0,1,1,1,1,2,0,1]]
    #faces=[[1,1,0,1],[1,0,1,1]]
    #nonfaces=[[1,1,1,0],[0,1,0,1]]
    model=0
    c = SemiNaive(0,0,2)
    c.training(faces, nonfaces, model)
    #c.testing([[1,1,1,1,1,1,1,1,1],[2,1,1,0,0,0,1,2,1]])
    c.testing(testdata)
    
#if __name__ == "__main__" :
#    sys.setrecursionlimit(1500)
#    face_detection()
