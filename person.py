class PharmacyCustomer:
    def __init__(self, name: str, personal_nr: int, drug_prescriptions: dict) -> None:
        self._name = name
        self._personal_nr = personal_nr
        self._drug_prescriptions = drug_prescriptions

    @property
    def name(self) -> str:
        """The name property"""

        return self._name

    @property
    def personal_nr(self) -> int:
        """The personal nr property"""

        return self._personal_nr

    @property
    def drug_prescriptions(self) -> dict:
        """The drug prescriptions property"""

        return self._drug_prescriptions

