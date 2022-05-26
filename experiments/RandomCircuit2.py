def random_circuit2(m, n, density, shot):
    k = int(n * density)
    cluster = ClusterState(n)
    circuit = QuantumCircuit(n, n)
    parity = 0
    for i in range(m):
        t_id = random.sample(range(n), k)
        for j in range(n):
            if j in t_id:
                cluster.t(j)
                circuit.t(j)
            else:
                cluster.h(j)
                circuit.h(j)
        if parity:
            for j in range(1, n - 1, 2):
                cluster.cnot(j, j + 1)
                circuit.cnot(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                cluster.cnot(j, j + 1)
                circuit.cnot(j, j + 1)
        parity ^= 1
    graph = cluster.to_graph_state()
    graph.draw_cluster()
    graph.eliminate_pauli()
    graph.draw()
    _, size = graph.schedule()
    plt.title(f"qubits required {size}")
    plt.show()