import numpy
from base import STL
from matplotlib import pyplot
from mpl_toolkits import mplot3d


class Slicer:
    def __init__(self, stl: STL):
        self.stl = stl

    def slice(self, S):
        self.slice_lines=[]
        for i in range(self.stl.no_of_facets):
            X_1=numpy.array([self.stl.vectors[i][0][0],self.stl.vectors[i][0][1],self.stl.vectors[i][0][2]])
            X_2=numpy.array([self.stl.vectors[i][1][0],self.stl.vectors[i][1][1],self.stl.vectors[i][1][2]])
            X_3=numpy.array([self.stl.vectors[i][2][0],self.stl.vectors[i][2][1],self.stl.vectors[i][2][2]])

            [x1,y1,z1]=X_1
            [x2,y2,z2]=X_2
            [x3,y3,z3]=X_3

            vert_tup=[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)]

            if(z1==z2 and z2==z3):
                continue

            L1=(z1/S) #To determine the closest slicing plane below or on the point
            L2=(z2/S)
            L3=(z3/S)

            L=numpy.floor([L1,L2,L3])
        
            on_layer_flag=0
            odd=0
            
            #determine the edge parallel to slicing plane
            if (z1==z2):
                on_layer_flag+=1
                odd=3
                
            if (z2==z3):
                on_layer_flag+=1
                odd=1
            if (z1==z3):
                on_layer_flag+=1
                odd=2
            
            L_max=numpy.floor(max(L1,L2,L3))
            L_min=numpy.floor(max(L1,L2,L3))

            
            # If one edge is parallel to the slicing plane
            if(on_layer_flag==1): 
                zs=[1,2,3]
                zs.remove(odd)

                #If parallel edge on slicing plane
                if(vert_tup[zs[0]-1][2]%S==0):
                    line_vertices=[vert_tup[zs[0]-1],vert_tup[zs[1]-1]] #the parallel edge
                    self.slice_lines.append(line_vertices)
                    
                    line_vertices=[]

                    #if more slicing planes intersect the triangle
                    if((L[odd-1]>L[zs[0]-1]+1 or L[odd-1]<L[zs[0]-1]-1)):
                        [xa,ya,za]=[vert_tup[odd-1][0],vert_tup[odd-1][1],vert_tup[odd-1][2]]
                        [xb,yb,zb]=[vert_tup[zs[0]-1][0],vert_tup[zs[0]-1][1],vert_tup[zs[0]-1][2]]
                        [xc,yc,zc]=[vert_tup[zs[1]-1][0],vert_tup[zs[1]-1][1],vert_tup[zs[1]-1][2]]
                        
                        
                        z_p1=L[odd-1]*S
                        if(za<zb): z_p1=z_p1+S
                        
                        while abs(z_p1-zb)>0:
                            if za==z_p1:
                                z_p1=z_p1+(S*(zb-z_p1))/abs(zb-z_p1)
                                continue
                            
                            x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                            y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb
                            
                            x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                            y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc
                            
                            line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                            
                            self.slice_lines.append(line_vertices)
                            if zb>z_p1:
                                z_p1=z_p1+S
                            else:
                                z_p1=z_p1-S
                            
                #If parallel edge not on slicing plane         
                elif ((L[odd-1]>L[zs[0]-1] or L[odd-1]<L[zs[0]-1])):
                    [xa,ya,za]=[vert_tup[odd-1][0],vert_tup[odd-1][1],vert_tup[odd-1][2]]
                    [xb,yb,zb]=[vert_tup[zs[0]-1][0],vert_tup[zs[0]-1][1],vert_tup[zs[0]-1][2]]
                    [xc,yc,zc]=[vert_tup[zs[1]-1][0],vert_tup[zs[1]-1][1],vert_tup[zs[1]-1][2]]
                    z_p1=(L[odd-1])*S
                    if(za<zb): z_p1=z_p1+S
                                
                    while (z_p1-zb)/(za-zb)>=0:
                        if za==z_p1:
                            z_p1=z_p1+(S*(zb-z_p1))/abs(zb-z_p1)
                            continue
                        
                        x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                        y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb
                        
                        x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                        y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc
                        
                        line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                        
                        self.slice_lines.append(line_vertices)
                        if zb>z_p1:
                            z_p1=z_p1+S
                        else:
                            z_p1=z_p1-S

            #The remaining triangles            
            else:
                vert_tup.sort(key=lambda x:x[2])
                [xa,ya,za]=[vert_tup[0][0],vert_tup[0][1],vert_tup[0][2]]
                [xb,yb,zb]=[vert_tup[1][0],vert_tup[1][1],vert_tup[1][2]]
                [xc,yc,zc]=[vert_tup[2][0],vert_tup[2][1],vert_tup[2][2]]

            
                L1=numpy.floor(za/S)
                L2=numpy.floor(zb/S)
                L3=numpy.floor(zc/S)

                if (L1<L3):
                    z_p1=L3*S

                    #start from highest vertex and move down
                    while(z_p1>=zb):
                        if(z_p1==zc):
                            z_p1=z_p1-S
                            continue
                        
                        x_p1=(xc-xb)*(z_p1-zb)/(zc-zb)+xb
                        y_p1=(yc-yb)*(z_p1-zb)/(zc-zb)+yb

                        x_p2=(xc-xa)*(z_p1-za)/(zc-za)+xa
                        y_p2=(yc-ya)*(z_p1-za)/(zc-za)+ya

                        line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                        self.slice_lines.append(line_vertices)
                        z_p1=z_p1-S


                    while(z_p1>za):
                        
                        x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                        y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb

                        x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                        y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc

                        line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                        self.slice_lines.append(line_vertices)
                        z_p1=z_p1-S
    
    def display(self):
        figure=pyplot.figure()
        print(len(self.slice_lines))
        ax=figure.add_subplot(111,projection='3d')
        for v in range(len(self.slice_lines)):
            ax.plot([self.slice_lines[v][0][0],self.slice_lines[v][1][0]],[self.slice_lines[v][0][1],self.slice_lines[v][1][1]],[self.slice_lines[v][0][2],self.slice_lines[v][1][2]])

        ax.auto_scale_xyz(
            
            self.stl.x.flatten(),
            self.stl.y.flatten(),
            self.stl.z.flatten()
        )

        pyplot.axis('on')
        pyplot.show()