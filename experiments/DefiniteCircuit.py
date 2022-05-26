def definite_circuit(angle_matrix: np.ndarray, shot: int):
    n, m = angle_matrix.shape
    cluster = ClusterState(n)
    cluster_method_map = {
        'x': cluster.x,
        'z': cluster.z,
        's': cluster.s,
        't': cluster.t,
        'h': cluster.h
    }
    circuit = QuantumCircuit(n, n)
    circuit_method_map = {
        'x': circuit.x,
        'z': circuit.z,
        's': circuit.s,
        't': circuit.t,
        'h': circuit.h
    }
    parity = 0
    for i in range(m):
        for j in range(n):
            cluster_method_map[angle_matrix[j, i]](j)
            circuit_method_map[angle_matrix[j, i]](j)
        if parity:
            for j in range(1, n - 1, 2):
                cluster.cnot(j, j + 1)
                circuit.cnot(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                cluster.cnot(j, j + 1)
                circuit.cnot(j, j + 1)
        parity ^= 1

    # Process the MBQC result
    graph = cluster.to_graph_state()
    graph.eliminate_pauli()
    graph.draw()
    counts_mbqc = graph.run(shot)

    # Process circuit measurements
    circuit.measure(range(n), range(n))
    simulator = QasmSimulator()
    qasm_circuit = transpile(circuit, simulator)
    job = simulator.run(circuit, shot=shot)
    result = job.result()
    counts_qc = result.get_counts(qasm_circuit)

    # Draw plots
    plot_histogram([counts_mbqc, counts_qc],
                   title="MBQC result compare to theoretical results",
                   legend=["MBQC", "UC"])
    circuit.draw(output='mpl')
    plt.show()