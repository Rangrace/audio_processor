from openai import OpenAI


class Assistant:
    def __init__(self, values: dict, client: OpenAI):
        self.name = values["name"]
        self.prompt = values["prompt"]
        self.tools = values["tools"]
        self.model = values["model"]
        self.temperature = values["temperature"]
        self.client = client

    def create_assistant(self):
        assistant = self.client.beta.assistants.create(name=self.name, instructions=self.prompt, tools=self.tools,
                                                       model=self.model, temperature=self.temperature)

        return assistant
