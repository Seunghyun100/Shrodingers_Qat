import pygame
import matplotlib.pyplot as plt
from math import pi, sqrt
from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import os

sim = Aer.get_backend('aer_simulator')

def load_bloch_sphere(eat_gate: list):
    # gate kind: 'M', 'X', 'Y', 'Z', 'H', 'S', 'T', 'S_dagger', 'T_dagger'

    qc = QuantumCircuit(1,1)    
    for gate in eat_gate:

        if gate == "X":
            qc.x(0)
        if gate == "Y":
            qc.y(0)
        if gate == "Z":
            qc.z(0)
        if gate == "H":
            qc.h(0)
        if gate == "S":
            qc.s(0)
        if gate == "T":
            qc.t(0)
        if gate == "S_dagger":
            qc.sdg(0)
        if gate == "T_dagger":
            qc.tdg(0)

    qc.draw()
    qc.save_statevector()
    qobj = assemble(qc)
    result = sim.run(qobj).result()
    state = result.get_statevector()
    bloch_sphere = render(state)

    return bloch_sphere

    # plot_bloch_multivector(state)
    # plt.show()

def render(state):

    if not os.path.exists("./temp"):
        # print("no exist!")
        os.mkdir("./temp")

    try:
        bloch_sphere = pygame.image.load(f"./temp/{state}.png")
    except:
        plot_bloch_multivector(state)
        plt.savefig(f"./temp/{state}.png")
        plt.cla()
        bloch_sphere = pygame.image.load(f"./temp/{state}.png")
        os.remove(f"./temp/{state}.png")
    
    return bloch_sphere

# load_bloch_sphere(list("HT"))