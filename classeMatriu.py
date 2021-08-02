import random


class Matriu():
    def __init__(self,files,columnes,dades=[],numero=None,calcular_determinant=True):#dades introduides per columnes
        self.numero=numero
        self.files=files
        self.columnes=columnes
        self.dades = [0] * files
        self.det()
        for i in range(files):
        	self.dades[i] = [0] * columnes
        if(len(dades)!=0):
            for i in range(len(dades)):
                self.dades[i%self.files][int(i/self.files)]=dades[i]     

#    def __iter__(self):
#        print("adeu")
#        return self

#    def __next__(self):
#        if(self.files>1):
#            print("hola")
#            self.files-=1
#            return self.dades[self.files]
#        else:
#            raise StopIteration


    @staticmethod
    def aleatori(files,columnes, min=0,max=9):
        mat=Matriu(files,columnes)
        for idx in range(mat.files):   
            for c in range(mat.columnes):
                mat.dades[idx][c]=random.randint(min,max)
        return mat
    @staticmethod
    def identitat(c):
        id=Matriu(c,c)
        for diag in range(id.files):
            id.dades[diag][diag]=1
        return id
    def copia(self,f_ad=0,c_ad=0):  #files i columnes adicionals per si se vol copiar a una matriu més gran
        resultat=Matriu(self.files+f_ad,self.columnes+c_ad)
        for fil in range(self.files):
            for col in range(self.columnes):
                resultat.dades[fil][col]=self.dades[fil][col]
        return resultat       
    def sub_matriu(self,fil,col):#agafa una submatriu de fil files i col columnes
        sub=self.copia()
        for idx in range(fil):
            for idx2 in range(col):
                sub.dades[idx][idx2]=self.dades[idx][idx2]                                
    def __str__(self):
        text=''
        for fil in range(self.files):
            for col in range(self.columnes):
                text+= str(self.dades[fil][col])+' '
            text+= '\n'
        return text    
    def __add__(self,B):
        sumades=self.copia()
        if(sumades.files==B.files and  sumades.columnes==B.columnes):
            for fil in range(len(self.dades)):
                for col in range(len(self.dades[0])):
                    
                    sumades.dades[fil][col]+=B.dades[fil][col]
            return sumades
        else:
            return False
    def __sub__(self,B):
        restades=self.copia()
        if(restades.files==B.files and  restades.columnes==B.columnes):
            for fil in range(len(self.dades)):
                for col in range(len(self.dades[0])):
                    restades.dades[fil][col]-=B.dades[fil][col]
            return restades
        else:
            return False
    def __mul__(self,mat2):
        
        if(type(mat2)==int or type(mat2)==float):
            resultat=Matriu(self.files,self.columnes)
            for c in range(self.files):
                for d in range(self.columnes):
                    resultat.dades[c][d]=mat2*self.dades[c][d]
        elif(self.columnes==mat2.files):
            resultat=Matriu(self.files,mat2.columnes)
            for c in range(resultat.files):
                for idx in range(resultat.columnes):
                    m=0
                    for d in range(self.columnes):
                        m+=self.dades[c][d]*mat2.dades[d][idx]
                    resultat.dades[c][idx]=m            
        return resultat
    def __pow__(self,pot):
        A=Matriu.identitat(self.files)
        B=self.copia()
        if(type(pot)==int):
            if(pot==0):
                return Matriu.identitat(A.files)
            if(pot<0):
                B=self.inversa()
                pot*=-1
            for _ in range(pot-1):
                A=A*B
            return A
    def t(self):
        trans=Matriu(self.columnes,self.files)
        for fil in range(trans.files):
            for col in range(trans.columnes):
                trans.dades[fil][col]=self.dades[col][fil]
        return trans
    def det(self):
        if self.det != None:
            return self.det
        det=1
        cop=self.copia()
        for x in range(self.files-1):
            f=x
            while (cop.dades[f][x]==0):
                f=f+1
                if(f>self.files):
                    det=0
            if(f!=x):
                cop.canvi_f(f,x)
                det*=-1
            for c in range(x+1,self.files):
                cop.__operar_fila(c,x,1,-cop.dades[c][x]/cop.dades[x][x])
                
        for idx in range(self.files):
            det*=cop.dades[idx][idx]
        self.det=det
        return det
    def inversa(self):
        cop=self.copia()
        if(self.files==self.columnes and self.det()!=0):
            inv=Matriu.identitat(self.files)
            for c in range(self.columnes):
                fila_nz=cop.dades[c][c] #Fila no zeros
                contador=0
                while(fila_nz==0):
                    contador+=1
                    fila_nz=cop.dades[c+contador][c]
                cop.canvi_f(c,c+contador)
                inv.canvi_f(c,c+contador)
                
                inv.__multiplicar_fila(c,1/cop.dades[c][c])
                cop.__multiplicar_fila(c,1/cop.dades[c][c])
                for f in range(self.files):
                    if(f!=c):
                        inv.__operar_fila(f,c,1,-cop.dades[f][c])
                        cop.__operar_fila(f,c,1,-cop.dades[f][c])
                        
            return inv
                    
        else:
            print("La matriu no és quadrada")
    def afegir_fila(self,fil):
        nova=self.copia(f_ad=1)
        for c in range (self.columnes):
            nova.dades[self.files][c]=fil[c]
        return nova
    def llevar_fila(self):
        if(self.files>1):
            nova=Matriu(self.files-1,self.columnes)
            for a in range (self.files-1):
                for b in range (self.columnes):
                    nova.dades[a][b]=self.dades[a][b]
            return nova
        else:
            print("no es poden llevar més files")
    def afegir_columna(self,col):
        nova=self.copia(c_ad=1)
        for c in range (self.files):
            nova.dades[c][self.columnes]=col[c]
        return nova        
    def llevar_columna(self):
        if(self.columnes>1):
            nova=Matriu(self.files,self.columnes-1)
            for a in range (self.files):
                for b in range (self.columnes-1):
                    nova.dades[a][b]=self.dades[a][b]
            return nova
        else:
            print("no es poden llevar més columnes")
    def canvi_f(self,a,b):
        for c in range(self.columnes):
            self.dades[a][c],self.dades[b][c]=self.dades[b][c],self.dades[a][c]
    def canvi_c(self,a,b):
        for c in range(self.files):
            self.dades[c][a],self.dades[c][b]=self.dades[c][b],self.dades[c][a]     
    def num_ceros(self):
        z=0
        for a in range(self.files):
            for b in range(self.columnes):
                if(self.dades[a][b]==0):
                    z+=1
        return z
    def inte(self): #torna els nombre a enters
        for a in range(self.files):
            for b in range(self.columnes):
                self.dades[a][b]=int(self.dades[a][b])
    def arrod(self,d): #arrodoneix la matriu a d decimals
        for a in range(self.files):
            for b in range(self.columnes):
                self.dades[a][b]=round(self.dades[a][b],d)
    def abs(self):#torna tots els nombres positius
        for a in range(self.files):
            for b in range(self.columnes):
                self.dades[a][b]=abs(self.dades[a][b])
    def cercar(self,valor):
        trobades=Matriu(0,2)
        for c in range (self.files):
            for d in range(self.columnes):
                if(self.dades[c][d]==valor):
                    trobades=trobades.afegir_fila([c,d])
        return trobades
    def LaTex(self):
        text=""
        for c in range(self.files):
            for d in range(self.columnes-1):
                text+=str(self.dades[c][d])+" & "
            text+=str(self.dades[c][self.columnes-1])+chr(92)+chr(92)+"\n"
        text="$$\n\left(\n"+chr(92)+"begin{matrix}\n"+text+chr(92)+"end{matrix}\n"+chr(92)+"right)\n$$"
        return text
    
    def LaTex_sistema(self,x,b):
        variables=["x","y","z","t"]
        text=""
        if(self.det==0):
            text+="SI\n"
        else:
            text+="SD\n"
        for c in range(self.files):
            for d in range(self.columnes-1):
                if(self.dades[c][d]>0):
                    text+="+" + str(self.dades[c][d])+variables[d]+" & "
                elif(self.dades[c][d]<0):
                    text+=str(self.dades[c][d])+variables[d]+" & "
            text+=str(self.dades[c][self.columnes-1])+variables[self.columnes-1] +" & = & "+str(b.dades[c][0])+chr(92)+chr(92)+"\n"
        text="$$\n\left\lbrace\n"+chr(92)+"begin{matrix}\n"+text+chr(92)+"end{matrix}\n"+chr(92)+"right.\n$$\n" 
        text+="Solució: $x=" + str(x.dades[0][0]) + "$, $y="+ str(x.dades[1][0]) + "$, $z=" + str(x.dades[2][0])+"$"
        return text
    @staticmethod
    def llegir(docu):
        mat=Matriu(1,1)
        f=open(docu,"r")
        carac=f.read(1)
        cela=""
        fi=0
        co=0
        cela=""
        while(carac!="\n" and carac != ""):
            co=0
            while(carac!="\n" and carac !=""):
                while(carac!="," and carac!="\n" and carac!=""):
                    cela=cela + carac
                    carac=f.read(1)    
                if(co+1>mat.columnes):
                    mat=mat.afegir_columna([cela])
                else:
                    
                    mat.dades[fi][co]=cela
                cela=""
                if (carac!="\n"):
                    carac=f.read(1)
                co+=1
            carac=f.read(1)
            if(carac!="\n" and carac !=""):
                mat=mat.afegir_fila([carac]+[0]*(mat.columnes-1))
            fi+=1
        f.close()
        return mat        
    def escriure(self,docu):
        f=open(docu,"w")
        for c in range(self.files):
            for d in range(self.columnes):
                f.write(str(self.dades[c][d])+",")
            f.write("\n")        
        f.close()        
    def __operar_fila(self,f1,f2,c1,c2):
        for c in range(self.columnes):
            self.dades[f1][c]=c1*self.dades[f1][c]+c2*self.dades[f2][c]    
    def __multiplicar_fila(self,fila,escalar):
        for c in range(self.columnes):
            self.dades[fila][c]=self.dades[fila][c]*escalar



if __name__=="__main__":
    A=Matriu(4,4,[1,2,3,4,0,0,0,0,0,0,0,0,0,0,0,0])
    
    
    
