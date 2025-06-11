OPENQASM 2.0;
include "qelib1.inc";


qreg q[7];

// --- Step 1: ccx q[0], q[1], q[5]
h q[5];
cx q[1], q[5];
tdg q[5];
cx q[0], q[5];
t q[5];
cx q[1], q[5];
tdg q[5];
cx q[0], q[5];
t q[1];
t q[5];
cx q[0], q[1];
h q[5];
t q[0];
tdg q[1];
cx q[0], q[1];

// --- Step 2: ccx q[2], q[3], q[6]
h q[6];
cx q[3], q[6];
tdg q[6];
cx q[2], q[6];
t q[6];
cx q[3], q[6];
tdg q[6];
cx q[2], q[6];
t q[3];
t q[6];
cx q[2], q[3];
h q[6];
t q[2];
tdg q[3];
cx q[2], q[3];

// --- Step 3: ccx q[5], q[6], q[4]
h q[4];
cx q[6], q[4];
tdg q[4];
cx q[5], q[4];
t q[4];
cx q[6], q[4];
tdg q[4];
cx q[5], q[4];
t q[6];
t q[4];
cx q[5], q[6];
h q[4];
t q[5];
tdg q[6];
cx q[5], q[6];

// --- Step 4: ccx q[2], q[3], q[6] (Uncompute)
h q[6];
cx q[3], q[6];
tdg q[6];
cx q[2], q[6];
t q[6];
cx q[3], q[6];
tdg q[6];
cx q[2], q[6];
t q[3];
t q[6];
cx q[2], q[3];
h q[6];
t q[2];
tdg q[3];
cx q[2], q[3];

// --- Step 5: ccx q[0], q[1], q[5] (Uncompute)
h q[5];
cx q[1], q[5];
tdg q[5];
cx q[0], q[5];
t q[5];
cx q[1], q[5];
tdg q[5];
cx q[0], q[5];
t q[1];
t q[5];
cx q[0], q[1];
h q[5];
t q[0];
tdg q[1];
cx q[0], q[1];
