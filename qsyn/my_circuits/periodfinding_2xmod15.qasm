OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];    // q[0-3]: counting, q[4-7]: work
creg c[4];    // classical bits for counting qubits

// --- Step 1: Hadamards on counting register
h q[0];
h q[1];
h q[2];
h q[3];

// --- Step 2: Initialize work register to |1⟩
x q[4];  // |0001⟩ = 1

// --- Step 3: Controlled modular exponentiation
// Simulate f(x) = 2^x mod 15, encoded manually for small x
// (In real Shor, you'd use modular exponentiation circuits)
// For simplicity, assume fixed action

// Skip actual exponentiation (placeholder logic)


// --- Step 4: Inverse QFT on counting qubits
// iQFT(q[0-3])
swap q[0], q[3];
swap q[1], q[2];

h q[0];
cp(-pi/2) q[1], q[0];
cp(-pi/4) q[2], q[0];
cp(-pi/8) q[3], q[0];

h q[1];
cp(-pi/2) q[2], q[1];
cp(-pi/4) q[3], q[1];

h q[2];
cp(-pi/2) q[3], q[2];

h q[3];

// --- Step 5: Measure counting qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
