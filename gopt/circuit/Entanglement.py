from ..core import BlochSphere


class Entanglement:
    """
    Record edges corresponding to entanglements
    """
    def __init__(self, size) -> None:
        self.entanglement_edges: set[((int, int), (int, int))] = set()
        self.corrections: list[dict[(int, int), BlochSphere]] = [
            dict() for _ in range(size)]
        self.dependencies: dict[(int, int), set[(int, int)]] = dict()
