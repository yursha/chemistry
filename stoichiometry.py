import re
import csv


periodic_table = {}
with open('periodic_table.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        periodic_table[row['Symbol']] = row


reaction = input("Please enter reaction: ")
pattern = re.compile('[^a-zA-Z0-9+=()]+')
reaction = pattern.sub('', reaction)

pair = reaction.split("=")
reactants = pair[0].split('+')
products = pair[1].split('+')


def parse_integer(string, index):
    result = 0
    while index < len(string) and string[index].isdigit():
        result = result * 10 + int(string[index])
        index += 1
    return 1 if result == 0 else result, index


def parse_element(string, index):
    result = ''
    while index < len(string) and string[index].isalpha():
        if string[index].isupper() and result:
            break
        result += string[index]
        index += 1
    print('parsed element %s from %s' % (result, string))
    return result, index


def calculate_per_mole_weight(substance):
    weight = 0
    coefficient, index = parse_integer(substance, 0)
    #print('coefficient is ', coefficient, ' and index is ', index)
    while index < len(substance):
        if substance[index] == '(':
            index += 1
            last_index = substance.find(')', index)
            functional_group_weight, _ = calculate_per_mole_weight(substance[index:last_index])
            index = last_index + 1
            subscript, index = parse_integer(substance, index)
            weight += functional_group_weight * subscript
        else:
            element, index = parse_element(substance, index)
            subscript, index = parse_integer(substance, index)
            print(element)
            weight += float(periodic_table[element]['AtomicMass']) * subscript
    return weight, coefficient


reactant_given_weights = []
reactant_per_mole_weights = []
reactant_coefficients = []
reactant_moles = []
reactant_mole_rxn = []

for reactant in reactants:
    given_weight = input("Please enter weight for %s: " % reactant)
    reactant_given_weights.append(given_weight)
    per_mole_weight, c = calculate_per_mole_weight(reactant)
    reactant_per_mole_weights.append(per_mole_weight)
    reactant_coefficients.append(c)
    moles = float(given_weight) / per_mole_weight
    reactant_moles.append(moles)
    mol_rxn = moles / c
    reactant_mole_rxn.append(mol_rxn)
    print("Reactant: %s, coefficient: %d, molecular weight (1 mole): %f, moles given: %f, molrxn: %f" % (
        reactant, c, per_mole_weight, moles, mol_rxn
    ))

limiting_reagent = reactant_mole_rxn.index(min(reactant_mole_rxn))
print('liming reagent is %s' % reactants[limiting_reagent])
mol_rxn_base = min(reactant_mole_rxn)

for product in products:
    per_mole_weight, c = calculate_per_mole_weight(product)
    moles = c * mol_rxn_base
    weight = moles * per_mole_weight
    print("Product: %s, coefficient: %d, molecular weight (1 mole): %f, moles: %f, weight: %f" % (
        product, c, per_mole_weight, moles, weight
    ))

#print('reaction', reaction)
#print('reactants', reactants)
#print('products', products)


