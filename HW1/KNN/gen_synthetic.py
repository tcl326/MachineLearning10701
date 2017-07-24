import numpy as np


def gen_synthetic(n,p,sigma):

    #Generate X0
    X=np.random.normal(size=(n,p))
    print "X0 generated"

    # print X[1:100]

    w=np.random.uniform(size=(p,1))-0.5
    print "w generated"

    Y0 = np.dot(X,w)
    Y0 = Y0+np.random.normal(loc=0,scale=sigma,size=(n,1))

    # print Y0[1:100]

    Y = np.ones((n,1))
    Y[Y0<0]=-1
    Y[Y0>=0]=1

    # print Y[1:100]

    return X,Y
