class Prompt:
    def __init__(self, values: dict):
        self._person = values["person"]
        self._place = values["place"]
        self._basic_instructions = values["basic_instructions"]
        self._task = values["task"]

    @property
    def person(self):
        return self._person

    @property
    def place(self):
        return self._place

    @property
    def basic_instructions(self):
        return self._basic_instructions

    @property
    def task(self):
        return self._task

    def get_instructions(self):
        instructions = f"""

        **Basic instructions**

        {self.basic_instructions}

        **Your task**

        {self.task}

        **Info about the person in front of you**

        {self.person}

        **Additional information**

        {self.place}

        """

        return instructions
