from dataclasses import dataclass

@dataclass
class Bollettino:
    intestatario: str
    causale: str
    eseguitoda: str
    via: str
    cap: int
    localita: str
    importocent: int
    importoinlettere: str
    contonumero: int
