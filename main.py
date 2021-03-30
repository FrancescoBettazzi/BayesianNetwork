from tabulate import tabulate
import bayesnet
import junctree


def printResults(model, variables, prob, exact_prob):
    headers = ['variable', 'prob', 'exact_prob']
    data = []
    var = iter(variables)
    exact = iter(exact_prob)
    for p in prob:
        v = next(var)
        ep = next(exact)
        data.append((v, [round(p.table[0][0] * 100, 2), round(p.table[0][1] * 100, 2)],
                     [round(ep.table[0][0] * 100, 2), round(ep.table[0][1] * 100, 2)]))

    print(model.name.upper() + ': (evidences: ' + str(model.evidences) + ')')
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()


# GET BAYESNET AND JUNC-TREE
asia = bayesnet.getBN('asia')
cancer = bayesnet.getBN('cancer')
sprinkler = bayesnet.getBN('sprinkler')

asiaJT = junctree.getJT('asia')
cancerJT = junctree.getJT('cancer')
sprinklerJT = junctree.getJT('sprinkler')

# SET EVIDENCES
variables = ['asia', 'smoke', 'dysp']
evidences = [False, True, True]

asia.setEvidence(variables, evidences)
asiaJT.setEvidence(variables, evidences)

variables = ['pollution', 'smoker']
evidences = [False, True]

cancer.setEvidence(variables, evidences)
cancerJT.setEvidence(variables, evidences)

variables = ['cloudy', 'wet_grass']
evidences = [True, True]

sprinkler.setEvidence(variables, evidences)
sprinklerJT.setEvidence(variables, evidences)

# GET PROBABILITIES
asia_variables = ['asia', 'bronc', 'dysp', 'either', 'lung', 'smoke', 'tub', 'xray']
cancer_variables = ['cancer', 'dyspnea', 'pollution', 'smoker', 'xray']
sprinkler_variables = ['cloudy', 'rain', 'sprinkler', 'wet_grass']

prob_asia = asiaJT.getProb(asia_variables)
prob_cancer = cancerJT.getProb(cancer_variables)
prob_sprinkler = sprinklerJT.getProb(sprinkler_variables)

exactProb_asia = asia.getProb(asia_variables)
exactProb_cancer = cancer.getProb(cancer_variables)
exactProb_sprinkler = sprinkler.getProb(sprinkler_variables)

# PRINT
printResults(asia, asia_variables, prob_asia, exactProb_asia)
printResults(cancer, cancer_variables, prob_cancer, exactProb_cancer)
printResults(sprinkler, sprinkler_variables, prob_sprinkler, exactProb_sprinkler)
