# MBQC-Gopt
Graph-based optimization for MBQC
### NOTE: I am currently refactoring this project. Some functionality may not be working properly.

## What is this project about?
This repo consists the software packages for my undergraduate thesis project on quantum computation. In this project, I am building an optimization engine for the measurement-based quantum computational(MBQC) model. The engine does the following optimization procedure while compiling a unitary circuit model to a MBQC model.
- It maps the algorithm expressed in unitary circuit into a MBQC model on cluster state
- It performs graph-based transformations to simulate the Clifford operations on the cluster state.
- It performs local complementation operations to search for an optimized graph state geometry.
- It conducts a measurement sequence where the memory efficiency is maximized.

## What is the motivation?
Though quantum computation in general demonstrates advantages compare to classical computation, a number of gates fall into the Clifford gate set can be efficiently simulated on classical computers. Measurement calculus is a specific kind of graph-based simulation paradigm for Clifford gates. It maps unitary gates into projective measurements on graph states and performs graph-based transformations to simulate the Clifford gates. After the simulation, it maps the residual projective measurements back onto unitary gates no unitary circuit. We will however take a different approach. The computation on graph state can be performed directly by measuring the qubits in corresponding bases. However, corrections are required if the measurements project qubits in the wrong direction. The measurement sequence and correction scheme can very much affect the memory efficiency of MBQC model. A scheduling algorithm is therefore in demand to maximize the memory efficiency of MBQC.

## Unitary circuit to MBQC
Please refer to `./graphoptim/experiments/DemoMBQC.py` for the use of `ClusterState`.

## TODO:
- [ ] Write documentation for unitary circuit.
- [ ] Refactor unitary circuit classes.
- [ ] Add support to translate between qiskit qasm code and the MBQC-circuit model.
