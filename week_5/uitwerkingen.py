import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

# ==== OPGAVE 1 ====
def plot_number(nrVector):
    # Let op: de manier waarop de data is opgesteld vereist dat je gebruik maakt
    # van de Fortran index-volgorde – de eerste index verandert het snelst, de 
    # laatste index het langzaamst; als je dat niet doet, wordt het plaatje 
    # gespiegeld en geroteerd. Zie de documentatie op 
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html

    nrVector = nrVector.reshape(20, 20).T

    plt.matshow(nrVector, cmap=plt.cm.gray)
    plt.show()

# ==== OPGAVE 2a ====
def sigmoid(z):
    # Maak de code die de sigmoid van de input z teruggeeft. Zorg er hierbij
    # voor dat de code zowel werkt wanneer z een getal is als wanneer z een
    # vector is.
    # Maak gebruik van de methode exp() in NumPy.

    return 1 / (1 + np.exp(-z))

# ==== OPGAVE 2b ====
def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van 
    # y en m

    x = int(max(y))

    # Create an (0,x) empty array
    matrix = np.empty((0, x))

    for number in y:
        # Fill row with 0's
        row = np.zeros((1, x))
        # Set column with index y-1 to 1
        row[0][number - 1] = 1

        # Stack the row onto matrix
        matrix = np.row_stack((matrix, row))
    
    return matrix

# ==== OPGAVE 2c ==== 
# ===== deel 1: =====
def predict_number(Theta1, Theta2, X):
    # Deze methode moet een matrix teruggeven met de output van het netwerk
    # gegeven de waarden van Theta1 en Theta2. Elke regel in deze matrix 
    # is de waarschijnlijkheid dat het sample op die positie (i) het getal
    # is dat met de kolom correspondeert.

    # De matrices Theta1 en Theta2 corresponderen met het gewicht tussen de
    # input-laag en de verborgen laag, en tussen de verborgen laag en de
    # output-laag, respectievelijk. 

    # Een mogelijk stappenplan kan zijn:

    #    1. voeg enen toe aan de gegeven matrix X; dit is de input-matrix a1
    #    2. roep de sigmoid-functie van hierboven aan met a1 als actuele
    #       parameter: dit is de variabele a2
    #    3. voeg enen toe aan de matrix a2, dit is de input voor de laatste
    #       laag in het netwerk
    #    4. roep de sigmoid-functie aan op deze a2; dit is het uiteindelijke
    #       resultaat: de output van het netwerk aan de buitenste laag.

    # Voeg enen toe aan het begin van elke stap en reshape de uiteindelijke
    # vector zodat deze dezelfde dimensionaliteit heeft als y in de exercise.

    # Add the bias node to a(1)
    bias_nodes = np.ones((1, X.shape[0]))
    a1 = np.row_stack((X.T, bias_nodes))

    # Compute z(2); z(2) = ϴ(1)a(1)
    z2 = Theta1.dot(a1)

    # Compute a(2); g(z(2))
    a2 = sigmoid(z2)

    # Add the bias node to a(2)
    bias_nodes = np.ones((1, a2.shape[1]))
    a2 = np.row_stack((a2, bias_nodes))

    # Compute z(3); ϴ(2)a(2)
    z3 = Theta2.dot(a2)

    # Compute a(3) / hθ(x): g(z(3))
    a3 = sigmoid(z3)

    return a3.T

# ===== deel 2: =====
def compute_cost(Theta1, Theta2, X, y):
    # Deze methode maakt gebruik van de methode predictNumber() die je hierboven hebt
    # geïmplementeerd. Hier wordt het voorspelde getal vergeleken met de werkelijk 
    # waarde (die in de parameter y is meegegeven) en wordt de totale kost van deze
    # voorspelling (dus met de huidige waarden van Theta1 en Theta2) berekend en
    # geretourneerd.
    # Let op: de y die hier binnenkomt is de m×1-vector met waarden van 1...10. 
    # Maak gebruik van de methode get_y_matrix() die je in opgave 2a hebt gemaakt
    # om deze om te zetten naar een matrix. 

    # Get predicted and actual values
    pred = predict_number(Theta1, Theta2, X)
    actual = get_y_matrix(y, y.shape[0])
    
    # Compute total cost per prediction
    total_class_cost = (-actual * np.log(pred) - (1-actual) * np.log(1 - pred)).sum(axis=1)
    total_prediction_cost = np.sum(total_class_cost)

    # Compute average cost
    m = y.shape[0]
    J = total_prediction_cost / m

    return J

# ==== OPGAVE 3a ====
def sigmoid_gradient(z): 
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.

    return sigmoid(z) * (1 - sigmoid(z))

# ==== OPGAVE 3b ====
def nn_check_gradients(Theta1, Theta2, X, y): 
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    Delta2 = np.zeros(Theta1.shape)
    Delta3 = np.zeros(Theta2.shape)

    m = y.shape[0]
    y_vect = get_y_matrix(y, m)

    for i in range(m): 
        # Forward propagation
        x = np.array(X[i])
        a1 = np.hstack(([1], x))
        z2 = np.dot(a1, Theta1.T)
        a2 = sigmoid(z2)
        a2 = np.hstack(([1], a2))
        z3 = np.dot(a2, Theta2.T)
        a3 = sigmoid(z3)

        # Backward propagation
        d3 = a3 - y_vect[i]

        d2 = np.dot(Theta2.T, d3)
        d2 = d2 * np.hstack(([1], sigmoid_gradient(z2)))

        # Convert from 1d vectors to 2d matrices
        d3 = d3.reshape(-1, 1)
        a2 = a2.reshape(-1, 1)
        d2 = d2.reshape(-1, 1)
        a1 = a1.reshape(-1, 1)
        d2 = d2[1:, :]

        Delta2 += np.dot(d2, a1.T)
        Delta3 += np.dot(d3, a2.T)

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m

    return Delta2_grad, Delta3_grad
