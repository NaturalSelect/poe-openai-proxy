import json

class Prompt:
    role:str
    content:str

    def __init__(self,role:str,content:str) -> None:
        self.role = role
        self.content = content

    def Marshal(self) -> str:
        return json.dumps(self)

    @staticmethod
    def UnmarshalWithDict(map:dict) -> "Prompt":
        p = Prompt(map["role"],map["content"])
        return p

    @staticmethod
    def Unmarshal(v:str) -> "Prompt":
        return Prompt.UnmarshalWithDict(json.loads(v))

class OpenAIRequest:
    messages:list[Prompt]

    def __init__(self,messages:list[Prompt]) -> None:
        self.messages = messages

    def Marshal(self) -> str:
        return json.dumps(self)


    @staticmethod
    def UnmarshalWithDict(map:dict) -> "OpenAIRequest":
        prompts:list[Prompt] = list[Prompt]()
        messages:list = map["messages"]
        for promptMap in messages:
            p:Prompt = Prompt.UnmarshalWithDict(promptMap)
            prompts.append(p)
        req = OpenAIRequest(prompts)
        return req

    @staticmethod
    def Unmarshal(v:str) -> "OpenAIRequest":
        return OpenAIRequest.UnmarshalWithDict(json.loads(v))

class OpenAIChoice:
    index:int

    messages:Prompt

    finish_reason:str

    logprobs:object # Must be null

    def __init__(self,index:int=0,message:Prompt=Prompt("",""),finishReason:str="stop") -> None:
        self.index = index
        self.messages = message
        self.finish_reason = finishReason
        self.logprobs = None

    def Marshal(self) -> str:
        return json.dumps(self)


    @staticmethod
    def UnmarshalWithDict(map:dict) -> "OpenAIChoice":
        index:int = map["index"]
        messageMap:dict = map["message"]
        message:Prompt = Prompt.UnmarshalWithDict(messageMap)
        finishReason:str = map["finish_reason"]
        return OpenAIChoice(index,message,finishReason)

    @staticmethod
    def Unmarshal(v:str) -> "OpenAIChoice":
        return OpenAIChoice.UnmarshalWithDict(json.loads(v))

class OpenAIResponse:
    choices:list[OpenAIChoice]

    def __init__(self,message:Prompt) -> None:
        self.choices = list()
        self.choices.append(OpenAIChoice(message=message))
        return

    def Marshal(self) -> str:
        return json.dumps(self)

    @staticmethod
    def UnmarshalWithDict(map:dict) -> "OpenAIResponse":
        choices:list[OpenAIChoice] = list()
        for choiceMap in map["choices"]:
            choices.append(OpenAIChoice.UnmarshalWithDict(choiceMap))

        resp = OpenAIResponse(None)
        resp.choices = choices
        return resp

    @staticmethod
    def Unmarshal(v:str) -> "OpenAIResponse":
        return OpenAIResponse.Unmarshal(json.loads(v))