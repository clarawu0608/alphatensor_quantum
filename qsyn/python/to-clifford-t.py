from qiskit import QuantumCircuit
from qiskit import transpile

from qiskit.synthesis import generate_basic_approximations
from qiskit.transpiler.passes import SolovayKitaev
import qiskit.qasm2

circuit_name = "qft4"

def qasm_to_clifford_and_t(qc, basic_approx_depth=3):
    qc = transpile(qc,basis_gates=["cx","u3"])
    basis = ["x", "y", "z", "s", "sdg", "t", "tdg", "z", "h"]
    approx = generate_basic_approximations(basis, depth=basic_approx_depth)
    skd = SolovayKitaev(recursion_degree=1, basic_approximations=approx)
    new_qc = skd(qc)
    new_qc.draw()

    return new_qc


# Load circuit from QASM 2.0 file
circuit = QuantumCircuit.from_qasm_file(f"./qsyn/my_circuits/{circuit_name}.qasm")

# Display or use the circuit
print(circuit)
circuit.draw()



# basic_approx_depth - size of basic circuits pool - as the RAM size I will to give
# recursion_degree=1 -> best aprox from pool
# bigger recursion_degree -> use only basic aproximations
# recursion_degree - choose by resolution wanted

new_qc = qasm_to_clifford_and_t(circuit)
print(new_qc)
new_qc.draw()
qiskit.qasm2.dump(new_qc, f"./qsyn/my_circuits/{circuit_name}_clifford_t.qasm")