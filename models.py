# This file contains blueprints for person, prescription, drug, task and stock. Collected in one place for simplicity

# Person

class Person:
    def __init__(self, name: str, personal_nr: str) -> None:
        self._name = name
        self._personal_nr = personal_nr

    @property
    def name(self) -> str:
        """The name property"""

        return self._name

    @property
    def personal_nr(self) -> str:
        """The personal nr property"""

        return self._personal_nr

    def __repr__(self):
        return f"""
        Name: {self.name}
        Personal nr: {self.personal_nr}
        """


# Prescription

class Prescription:
    def __init__(self, drug: str, usage: str, withdrawals: int, ):
        self._drug = drug
        self._usage = usage
        self._withdrawals = withdrawals

    @property
    def drug(self) -> str:
        """The drug property"""

        return self._drug

    @property
    def usage(self) -> str:
        """The usage property"""

        return self._usage

    @property
    def withdrawals(self) -> int:
        """The nr of withdrawals property"""

        return self._withdrawals

    def __repr__(self):
        return f"""
        Drug: {self.drug}
        Usage: {self.usage}
        Withdrawals: {self.withdrawals}
        """


# Drug

class Drug:
    def __init__(self, name: str, dosage: int, brand: str) -> None:
        self._name = name
        self._dosage = dosage
        self._brand = brand

    @property
    def name(self) -> str:
        """The name property"""

        return self._name

    @property
    def dosage(self) -> str:
        """The dosage property"""

        return f"{self._dosage} mg"

    @property
    def brand(self) -> str:
        """The brand property"""

        return self._brand

    def __repr__(self):
        return f"""
        Name: {self.name}
        Dosage: {self.dosage}
        Brand: {self.brand}
        """


# Task

class Task:
    def __init__(self, name: str):
        self._name = name
        self._steps = []

    @property
    def name(self):
        return self._name

    @property
    def steps(self):
        return self._steps

    def add_step(self, step: str):
        self.steps.append(step)

    def __repr__(self):
        return f"""
        Name of task: {self.name}
        Steps to complete the task: {self.steps}
        """


class Stock:
    def __init__(self):
        self._stock = {}

    @property
    def stock(self):
        return self._stock

    def add(self, key: str, value: list):
        self._stock[key] = value

    def __repr__(self):
        return f"{self.stock}"
