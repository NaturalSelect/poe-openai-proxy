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
    def objectHook(map:dict):
        p = Prompt(map["Role"],map["Content"])
        return p

    @staticmethod
    def UnmarshalWithDict(map:dict):
        return Prompt.objectHook(map)

    @staticmethod
    def Unmarshal(v:str):
        return json.loads(v,object_hook=Prompt.objectHook)

class OpenAIRequest:
    messages:list[Prompt]

    def __init__(self,messages:list[Prompt]) -> None:
        self.messages = messages

    def Marshal(self) -> str:
        return json.dumps(self)

    @staticmethod
    def objectHook(map:dict):
        prompts:list[Prompt] = list()
        messages:list = map["Messages"]
        for promptMap in messages:
            p = Prompt.UnmarshalWithDict(promptMap)
            prompts.append(p)
        req = OpenAIRequest(messages)
        return req

    @staticmethod
    def UnmarshalWithDict(map:dict):
        return OpenAIRequest.objectHook(map)

    @staticmethod
    def Unmarshal(v:str):
        return json.loads(v,object_hook=OpenAIRequest.objectHook)

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
    def objectHook(map:dict):
        index:int = map["index"]
        messageMap:dict = map["message"]
        message:Prompt = Prompt.UnmarshalWithDict(messageMap)
        finishReason:str = map["finish_reason"]
        return OpenAIChoice(index,message,finishReason)

    @staticmethod
    def UnmarshalWithDict(map:dict):
        return OpenAIChoice.objectHook(map)

    @staticmethod
    def Unmarshal(v:str):
        return json.loads(v,object_hook=OpenAIChoice.objectHook)

class OpenAIResponse:
    choices:list[OpenAIChoice]

    def __init__(self,message:Prompt) -> None:
        self.choices = list()
        self.choices.append(OpenAIChoice(message=message))
        return

    def Marshal(self) -> str:
        return json.dumps(self)

    @staticmethod
    def objectHook(map:dict):
        choices:list[OpenAIChoice] = list()
        for choiceMap in map["choices"]:
            choices.append(OpenAIChoice.UnmarshalWithDict(choiceMap))

        resp = OpenAIResponse(None)
        resp.choices = choices
        return resp

    @staticmethod
    def UnmarshalWithDict(map:dict):
        return OpenAIResponse.objectHook(map)

    @staticmethod
    def Unmarshal(v:str):
        return json.loads(v,object_hook=OpenAIResponse.objectHook)