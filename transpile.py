from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import SabreLayout, SabreSwap
from qiskit.transpiler.preset_passmanagers import level_0_pass_manager, level_1_pass_manager,\
    level_2_pass_manager, level_3_pass_manager
from qiskit.transpiler.passmanager_config import PassManagerConfig

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
reversed_coupling = []
for pair in coupling:
    reversed_coupling.append([pair[1], pair[0]])
coupling_map = CouplingMap(couplinglist=coupling + reversed_coupling)

# parse qasm file into a circuit
circuit = QuantumCircuit(20)
with open('sabre.qasm') as file:
    # omit the header
    file.readline()
    file.readline()
    line = file.readline()
    num_qubits = int(line.split(' ')[1].split(']')[0].split('[')[1])
    # parse the rest
    line = file.readline()
    while line != '':
        # add to circuit
        arg_list = line.split(' ')
        if arg_list[0] == '':
            arg_list = arg_list[1:]
        if len(arg_list) == 3:
            # two qubits gate
            qubit1 = int(arg_list[1].split(']')[0].split('[')[1])
            qubit2 = int(arg_list[2].split(']')[0].split('[')[1])
            circuit.cx(qubit1, qubit2)
        elif len(arg_list) == 2:
            # single qubit gate
            qubit1 = int(arg_list[1].split(']')[0].split('[')[1])
            circuit.h(qubit1)
        else:
            assert False
        # read another line
        line = file.readline()

# run sabre layout and sabre swap
level_0_manager = level_0_pass_manager(PassManagerConfig(coupling_map=coupling_map, layout_method="sabre",
                                                         routing_method="sabre"))
level_1_manager = level_1_pass_manager(PassManagerConfig(coupling_map=coupling_map, layout_method="sabre",
                                                         routing_method="sabre"))
level_2_manager = level_2_pass_manager(PassManagerConfig(coupling_map=coupling_map, layout_method="sabre",
                                                         routing_method="sabre"))
level_3_manager = level_3_pass_manager(PassManagerConfig(coupling_map=coupling_map, layout_method="sabre",
                                                         routing_method="sabre"))
result_circuit_0 = level_0_manager.run(circuit)
result_circuit_1 = level_1_manager.run(circuit)
result_circuit_2 = level_2_manager.run(circuit)
result_circuit_3 = level_3_manager.run(circuit)

# original gate count
ori_circuit_op_list = dict(circuit.count_ops())
ori_gate_count = 0
for key in ori_circuit_op_list:
    if key == "swap":
        ori_gate_count += 3 * ori_circuit_op_list[key]
    else:
        ori_gate_count += ori_circuit_op_list[key]
print(f"Original circuit gate dict: {ori_circuit_op_list}")
print(f"Original circuit gate count: {ori_gate_count}")

# level 0 gate count
level0_circuit_op_list = dict(result_circuit_0.count_ops())
level0_gate_count = 0
for key in level0_circuit_op_list:
    if key == "swap":
        level0_gate_count += 3 * level0_circuit_op_list[key]
    else:
        level0_gate_count += level0_circuit_op_list[key]
print(f"Level 0 circuit gate dict: {level0_circuit_op_list}")
print(f"Level 0 circuit gate count: {level0_gate_count}")

# level 1 gate count
level1_circuit_op_list = dict(result_circuit_1.count_ops())
level1_gate_count = 0
for key in level1_circuit_op_list:
    if key == "swap":
        level1_gate_count += 3 * level1_circuit_op_list[key]
    else:
        level1_gate_count += level1_circuit_op_list[key]
print(f"Level 1 circuit gate dict: {level1_circuit_op_list}")
print(f"Level 1 circuit gate count: {level1_gate_count}")

# level 2 gate count
level2_circuit_op_list = dict(result_circuit_2.count_ops())
level2_gate_count = 0
for key in level2_circuit_op_list:
    if key == "swap":
        level2_gate_count += 3 * level2_circuit_op_list[key]
    else:
        level2_gate_count += level2_circuit_op_list[key]
print(f"Level 2 circuit gate dict: {level2_circuit_op_list}")
print(f"Level 2 circuit gate count: {level2_gate_count}")

# level 3 gate count
level3_circuit_op_list = dict(result_circuit_3.count_ops())
level3_gate_count = 0
for key in level3_circuit_op_list:
    if key == "swap":
        level3_gate_count += 3 * level3_circuit_op_list[key]
    else:
        level3_gate_count += level3_circuit_op_list[key]
print(f"Level 3 circuit gate dict: {level3_circuit_op_list}")
print(f"Level 3 circuit gate count: {level3_gate_count}")
