import os
for f in os.listdir("./"):
    print (f)
    r = f.replace(" ","")
    print ("f::",f)
    print ("r::",r)
    if( r != f):
        os.rename(f,r)