import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.mlab as mlab
from numpy.core.fromnumeric import transpose

def draw_graph(data):
    # OPGAVE 1
    # Maak een scatter-plot van de data die als parameter aan deze functie wordt meegegeven. Deze data
    # is een twee-dimensionale matrix met in de eerste kolom de grootte van de steden, in de tweede
    # kolom de winst van de vervoerder. Zet de eerste kolom op de x-as en de tweede kolom op de y-as.
    # Je kunt hier gebruik maken van de mogelijkheid die Python biedt om direct een waarde toe te kennen
    # aan meerdere variabelen, zoals in het onderstaande voorbeeld:

    #     l = [ 3, 4 ]
    #     x,y = l      ->  x = 3, y = 4

    # Om deze constructie in dit specifieke geval te kunnen gebruiken, moet de data-matrix wel eerst
    # roteren (waarom?).
    # Maak gebruik van pytplot.scatter om dit voor elkaar te krijgen.

    x, y = zip(*data)

    plt.scatter(x, y)
    plt.xlabel('Populatie (10k personen)')
    plt.ylabel('Winst (10k$)')
    
    plt.show()

def compute_cost(X, y, theta):
    # OPGAVE 2
    # Deze methode berekent de kosten van de huidige waarden van theta, dat wil zeggen de mate waarin de
    # voorspelling (gegeven de specifieke waarde van theta) correspondeert met de werkelijke waarde (die
    # is gegeven in y).

    # Elk datapunt in X wordt hierin vermenigvuldigd met theta (welke dimensies hebben X en dus theta?)
    # en het resultaat daarvan wordt vergeleken met de werkelijke waarde (dus met y). Het verschil tussen
    # deze twee waarden wordt gekwadrateerd en het totaal van al deze kwadraten wordt gedeeld door het
    # aantal data-punten om het gemiddelde te krijgen. Dit gemiddelde moet je retourneren (de variabele
    # J: een getal, kortom).

    # Een stappenplan zou het volgende kunnen zijn:

    #    1. bepaal het aantal datapunten
    #    2. bepaal de voorspelling (dus elk punt van X maal de huidige waarden van theta)
    #    3. bereken het verschil tussen deze voorspelling en de werkelijke waarde
    #    4. kwadrateer dit verschil
    #    5. tal al deze kwadraten bij elkaar op en deel dit door twee keer het aantal datapunten

    # Make sure theta has the right shape
    theta = theta.reshape((2, 1))

    # Get n of data points
    m = y.shape[0]

    # Calculate hypotheses
    h = X.dot(theta)

    # Calculate difference with actual value squared
    delta = (y - h) ** 2

    # Calculate cost
    J = sum(delta) / (2 * m)

    return J

def gradient_descent(X, y, theta, alpha, num_iters):
    #OPGAVE 3a
    # In deze opgave wordt elke parameter van theta num_iter keer geüpdate om de optimale waarden
    # voor deze parameters te vinden. Per iteratie moet je alle parameters van theta update.

    # Elke parameter van theta wordt verminderd met de som van de fout van alle datapunten
    # vermenigvuldigd met het datapunt zelf (zie Blackboard voor de formule die hierbij hoort).
    # Deze som zelf wordt nog vermenigvuldigd met de 'learning rate' alpha.

    # Een mogelijk stappenplan zou zijn:
    #
    # Voor elke iteratie van 1 tot num_iters:
    #   1. bepaal de voorspelling voor het datapunt, gegeven de huidige waarde van theta
    #   2. bepaal het verschil tussen deze voorspelling en de werkelijke waarde
    #   3. vermenigvuldig dit verschil met de i-de waarde van X
    #   4. update de i-de parameter van theta, namelijk door deze te verminderen met
    #      alpha keer het gemiddelde van de som van de vermenigvuldiging uit 3

    costs = []

    # Make sure theta has the right shape
    theta = theta.reshape((2, 1))
    m = X.shape[0]

    for _ in range(num_iters):
        # Calculate hypotheses
        h = X.dot(theta)

        # Calculate difference with actual value
        A = h - y

        # Multiply by X
        value = A * X

        # Calculate updated theta
        theta = (theta.T - (alpha * (value.sum(axis=0) / m))).T

        # Calculate cost for new theta and store in costs list
        costs.append(compute_cost(X, y, theta)[0])

    return theta.T, costs

def draw_costs(costs): 
    # OPGAVE 3b
    
    # Plot x and y axis in linegraph
    plt.plot(range(len(costs)), costs)

    # Set labels
    plt.xlabel('Iteraties')
    plt.ylabel('J(θ)')
    
    # Show plot
    plt.show()

def contour_plot(X, y):
    #OPGAVE 4
    # Deze methode tekent een contour plot voor verschillende waarden van theta_0 en theta_1.
    # De infrastructuur en algemene opzet is al gegeven; het enige wat je hoeft te doen is 
    # de matrix J_vals vullen met waarden die je berekent aan de hand van de methode computeCost,
    # die je hierboven hebt gemaakt.
    # Je moet hiervoor door de waarden van t1 en t2 itereren, en deze waarden in een ndarray
    # zetten. Deze ndarray kun je vervolgens meesturen aan de functie computeCost. Bedenk of je nog een
    # transformatie moet toepassen of niet. Let op: je moet computeCost zelf *niet* aanpassen.

    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    plt.get_cmap('jet')

    t1 = np.linspace(-10, 10, 10)
    t2 = np.linspace(-1, 4, 10)
    T1, T2 = np.meshgrid(t1, t2)

    J_vals = np.zeros((len(t2), len(t2)))

    # Compute costs for every theta in J_val matrix
    for i, theta0 in enumerate(t1):
        for j, theta1 in enumerate(t2):
            J_vals[i][j] = compute_cost(X, y, np.array([[theta0], [theta1]]))

    # Plot surface
    ax.plot_surface(T1, T2, J_vals, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Set labels
    ax.set_xlabel(r'$\theta_0$', linespacing=3.2)
    ax.set_ylabel(r'$\theta_1$', linespacing=3.1)
    ax.set_zlabel(r'$J(\theta_0, \theta_1)$', linespacing=3.4)

    ax.dist = 10

    plt.show()
