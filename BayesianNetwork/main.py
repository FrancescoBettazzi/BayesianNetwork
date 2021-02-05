import bnlearn

'''
Given a Bayesian Network, put the evidence and, through message passing, get the probability
of a random variable conditioned by evidence p(V|e).
'''

# Asia model, p(L|A=1,S=0,D=1)
model1 = dict(bnlearn.import_DAG('asia.bif'))
# G1 = bnlearn.plot(model)
q1 = bnlearn.inference.fit(model1, variables=['lung'], evidence={'asia': 1, 'smoke': 0, 'dysp': 1})

# Sprinkler model, p(S|W=1)
model2 = dict(bnlearn.import_DAG('sprinkler'))
# G2 = bnlearn.plot(model2)
q2 = bnlearn.inference.fit(model2, variables=['Sprinkler'], evidence={'Wet_Grass': 1})

# Cancer model, p(C|S=0,P=1)
model3 = dict(bnlearn.import_DAG('cancer.bif'))
# G3 = bnlearn.plot(model3)
q3 = bnlearn.inference.fit(model3, variables=['Cancer'], evidence={'Smoker': 0, 'Pollution': 1})
