# queue_simulator.py - Implementação única do simulador de filas baseado na conversão Java

from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml
import os

# ---------------- CONFIGURAÇÕES ----------------
@dataclass
class QueueConfig:
    servers: int
    capacity: int
    min_arrival: Optional[float] = None
    max_arrival: Optional[float] = None
    min_service: float = 0.0
    max_service: float = 0.0

@dataclass
class Network:
    source: str
    target: str
    probability: float

@dataclass
class Config:
    rndnumbers_per_seed: int
    seeds: int
    arrival: float
    queues: Dict[str, QueueConfig]
    network: List[Network]


# ---------------- EVENTOS ----------------
class Event:
    def __init__(self, tempo, source, target, tipo):
        self.tempo = tempo
        self.source = source
        self.target = target
        self.tipo = tipo

    def __lt__(self, other):
        return self.tempo < other.tempo


# ---------------- PAR ----------------
class Pair:
    def __init__(self, fila, prob):
        self.fila = fila
        self.prob = prob

    def __lt__(self, other):
        return self.prob > other.prob


# ---------------- FILA ----------------
class Queue:
    def __init__(self, id, c, k, inicio_a, fim_a):
        self.id = id
        self.f = 0
        self.servidores = c
        self.capacidade = k
        self.perdas = 0
        self.q = []
        self.inicio_atendimento = inicio_a
        self.fim_atendimento = fim_a
        self.estados = {}

    def inc(self): self.f += 1
    def dec(self): self.f -= 1
    def inc_perda(self): self.perdas += 1

    def add(self, target, prob):
        self.q.append(Pair(target, prob))
        self.q.sort()

    def target(self, prob, tempo, source):
        acc = 0
        for pair in self.q:
            acc += pair.prob
            if prob <= acc:
                return Event(tempo, source, pair.fila, 'p')
        return Event(tempo, source, source, 's')

    def count(self, estado, tempo):
        self.estados[estado] = self.estados.get(estado, 0) + tempo

    def set_porcentagem(self, estado, tempo_total):
        self.estados[estado] = (self.estados[estado] / tempo_total) * 100


# ---------------- SIMULADOR ----------------
class RoutingSimulator:
    def __init__(self, filas, intervalo_chegada, tempo_inicial, n, x0):
        self.tempo_total = 0
        self.agenda = []
        self.aleatorios = []
        self.filas = filas
        self.intervalo_chegada = intervalo_chegada
        self.gera_aleatorios(n, x0)
        self.agenda.append(Event(tempo_inicial, filas[0], filas[0], 'c'))

    def gera_aleatorios(self, n, x0):
        aux = x0
        for _ in range(n):
            aux = ((aux * 25.214903917) + 11) % (2 ** 44)
            self.aleatorios.append(aux / (2 ** 44))

    def rand(self, a, b):
        return ((b - a) * self.aleatorios.pop(0)) + a

    def run(self):
        while len(self.aleatorios) > 2:
            self.agenda.sort()
            e = self.agenda.pop(0)
            for f in self.filas:
                f.count(f.f, e.tempo - self.tempo_total)
            self.tempo_total = e.tempo
            if e.tipo == 'c': self.chegada(e.source, e.target)
            elif e.tipo == 'p': self.passagem(e.source, e.target)
            elif e.tipo == 's': self.saida(e.source, e.target)
        self.resultado()

    def chegada(self, source, target):
        if source.f < source.capacidade or source.capacidade == -1:
            source.inc()
            if source.f <= source.servidores:
                self.agenda.append(source.target(self.aleatorios.pop(0), self.tempo_total + self.rand(source.inicio_atendimento, source.fim_atendimento), source))
        else:
            source.inc_perda()
        self.agenda.append(Event(self.tempo_total + self.rand(*self.intervalo_chegada), source, target, 'c'))

    def saida(self, source, target):
        source.dec()
        if source.f >= source.servidores:
            self.agenda.append(source.target(self.aleatorios.pop(0), self.tempo_total + self.rand(source.inicio_atendimento, source.fim_atendimento), source))

    def passagem(self, source, target):
        self.saida(source, target)
        if target.f < target.capacidade or target.capacidade == -1:
            target.inc()
            if target.f <= target.servidores:
                self.agenda.append(target.target(self.aleatorios.pop(0), self.tempo_total + self.rand(target.inicio_atendimento, target.fim_atendimento), target))
        else:
            target.inc_perda()

    def resultado(self):
        for f in self.filas:
            for estado in list(f.estados.keys()):
                f.set_porcentagem(estado, self.tempo_total)
            print("---------------------------------------")
            print(f"Fila: {f.id}")
            print(f"Atendimento: {f.inicio_atendimento} ... {f.fim_atendimento}")
            print("---------------------------------------")
            print("Estado\t\tProbabilidade")
            for estado, tempo in f.estados.items():
                print(f"{estado}\t\t{tempo:.2f}%")
            print(f"Perdas: {f.perdas}")
        print(f"Tempo Total: {self.tempo_total}")


# ---------------- FUNÇÕES AUXILIARES ----------------
def create_queue(id, queue_config):
    return Queue(id, queue_config.servers, queue_config.capacity, queue_config.min_service, queue_config.max_service)

def add_network(queues, source_id, target_id, prob):
    source = next((q for q in queues if q.id == source_id), None)
    target = next((q for q in queues if q.id == target_id), None)
    if source and target:
        source.add(target, prob)

def calcular_populacao(queue):
    return sum((pi / 100.0) * i for i, pi in queue.estados.items())

def calcular_vazao(queue):
    mu = 2.0 / (queue.inicio_atendimento + queue.fim_atendimento)
    c = queue.servidores
    return sum(((pi / 100.0) * (i * mu if i <= c else c * mu)) for i, pi in queue.estados.items())

def calcular_utilizacao(queue):
    c = queue.servidores
    return sum((pi / 100.0) * (min(i, c) / c) for i, pi in queue.estados.items())

def calcular_tempo_resposta(populacao, vazao):
    return 0 if vazao == 0 else populacao / vazao


# ---------------- MAIN ----------------
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "inputsT2Proposta2.yaml")
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)

            # Conversão explícita dos dados para as dataclasses
            queues = {k: QueueConfig(**v) for k, v in data["queues"].items()}
            network = [Network(**n) for n in data["network"]]
            config = Config(
                rndnumbers_per_seed=data["rndnumbers_per_seed"],
                seeds=data["seeds"],
                arrival=data["arrival"],
                queues=queues,
                network=network
            )

    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        exit(1)

    filas = [
        create_queue("F1", config.queues["F1"]),
        create_queue("F2", config.queues["F2"]),
        create_queue("F3", config.queues["F3"])
    ]

    for net in config.network:
        add_network(filas, net.source, net.target, net.probability)

    primeira_chegada = [config.queues["F1"].min_arrival, config.queues["F1"].max_arrival]
    sim = RoutingSimulator(filas, primeira_chegada, config.arrival, config.rndnumbers_per_seed, config.seeds)
    sim.run()

    resultados = []
    descricao_filas = [
        "G/G/1, chegadas entre 2..4, atendimento entre 1..2",
        "G/G/2/5, atendimento entre 4..8",
        "G/G/2/10, atendimento entre 5..15"
    ]

    for idx, (q, desc) in enumerate(zip(filas, descricao_filas), start=1):
        pop = calcular_populacao(q)
        vazao = calcular_vazao(q)
        util = calcular_utilizacao(q)
        t_resp = calcular_tempo_resposta(pop, vazao)

        resultados.append(f"\n"
                          f"{idx}. Resultado da Fila {idx}: {desc}\n"
                          f"   - População média:       {pop:.4f}\n"
                          f"   - Vazão:                 {vazao:.4f}\n"
                          f"   - Utilização:            {util:.4f}\n"
                          f"   - Tempo de resposta:     {t_resp:.4f}\n"
                          f"   - Perdas:                {q.perdas}\n"
                          f"   - Estados (%):           { {k: round(v, 2) for k, v in q.estados.items()} }\n")

    print("\n".join(resultados))
    print(f"4. Tempo total de simulação: {sim.tempo_total:.2f}")