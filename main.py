from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import BasicSwap, LookaheadSwap, StochasticSwap

# identical to IBM Q20 Tokyo
coupling = [
    # rows
    [0, 1], [1, 2], [2, 3], [3, 4],
    [5, 6], [6, 7], [7, 8], [8, 9],
    [10, 11], [11, 12], [12, 13], [13, 14],
    [15, 16], [16, 17], [17, 18], [18, 19],
    # cols
    [0, 5], [5, 10], [10, 15],
    [1, 6], [6, 11], [11, 16],
    [2, 7], [7, 12], [12, 17],
    [3, 8], [8, 13], [13, 18],
    [4, 9], [9, 14], [14, 19],
    # crossings
    [1, 7], [2, 6],
    [3, 9], [4, 8],
    [5, 11], [6, 10],
    [8, 12], [7, 13],
    [11, 17], [12, 16],
    [13, 19], [14, 18]
]

circuit = QuantumCircuit(7)
circuit.h(3)
circuit.cx(0, 6)
circuit.cx(6, 0)
circuit.cx(0, 1)
circuit.cx(3, 1)
circuit.cx(3, 0)

coupling_map = CouplingMap(couplinglist=coupling)

bs = BasicSwap(coupling_map=coupling_map)
pass_manager = PassManager(bs)
basic_circ = pass_manager.run(circuit)

ls = LookaheadSwap(coupling_map=coupling_map)
pass_manager = PassManager(ls)
lookahead_circ = pass_manager.run(circuit)

ss = StochasticSwap(coupling_map=coupling_map)
pass_manager = PassManager(ss)
stochastic_circ = pass_manager.run(circuit)
