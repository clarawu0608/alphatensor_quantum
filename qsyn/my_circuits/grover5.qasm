OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

// --- Step 1: Initialization (Hadamards on all qubits)
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];

// --- Step 2: Oracle (marking a specific state)
// Let's say the "target" state is |10101⟩ (q4 q3 q2 q1 q0)
// In little-endian, that's q[0]=1, q[1]=0, q[2]=1, q[3]=0, q[4]=1

// Flip bits to turn |10101⟩ into |11111⟩
x q[1];
x q[3];

// Multi-controlled Z (emulated with H + multi-ccx + H)
h q[4];
ccx q[0], q[1], q[2];     // ancilla not available, so simulate pairwise
ccx q[2], q[3], q[4];
h q[4];

// Undo the flips
x q[1];
x q[3];

// --- Step 3: Diffusion operator (inversion about the mean)
// H, X on all qubits
h q[0]; x q[0];
h q[1]; x q[1];
h q[2]; x q[2];
h q[3]; x q[3];
h q[4]; x q[4];

// Multi-controlled Z again (reflect about |00000⟩)
h q[4];
ccx q[0], q[1], q[2];
ccx q[2], q[3], q[4];
h q[4];

// X, H on all qubits to undo
x q[0]; h q[0];
x q[1]; h q[1];
x q[2]; h q[2];
x q[3]; h q[3];
x q[4]; h q[4];

// --- Step 4: Measurement
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
