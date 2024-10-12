import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing_extensions import Annotated
from langchain_openai import ChatOpenAI
from typing import Optional

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
class Multiple(BaseModel):
    "Multiply two numbers"
    a: int = Field(description='first integer',examples=[1,3,44],strict=True)
    b: int = Field(description='Second intiger')
    c: int = Field(description='third integer')

class Add(BaseModel):
    "add two numbers"
    a:Annotated[int,'first integer'] = 10
    b:Annotated[int,'second integer']
    c:Annotated[Optional[int],...,'second integer']
    
class multiply(BaseModel):
    """Multiply two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

    
tool = [Add,Multiple]

llm = ChatOpenAI(model='gpt-4o-mini',api_key = api_key)
tool_and_llm = llm.bind_tools(tool)
print('#####',tool_and_llm)
res = tool_and_llm.invoke('will you help me multily the number five and three')
print('api_key == ',res)

