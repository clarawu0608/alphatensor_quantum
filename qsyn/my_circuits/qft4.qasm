OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

// --- Step 1: QFT circuit

// Qubit 0
h q[0];
cp(pi/2) q[1], q[0];
cp(pi/4) q[2], q[0];
cp(pi/8) q[3], q[0];

// Qubit 1
h q[1];
cp(pi/2) q[2], q[1];
cp(pi/4) q[3], q[1];

// Qubit 2
h q[2];
cp(pi/2) q[3], q[2];

// Qubit 3
h q[3];！

// --- Step 2: Swap to reverse qubit order
swap q[0], q[3];
swap q[1], q[2];

// --- Step 3: Optional measurement
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
