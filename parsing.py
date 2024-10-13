from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field, model_validator
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


class query(BaseModel):
    "create sql query for given column name, email and column value."
    name: str = Field(description='column name')
    value: int = Field(description='column value')
    email: str = Field(description='email of person',examples=['m@example.com'])
    @model_validator(mode='before')
    @classmethod
    def validate_each_value(cls, values: dict):
        print(f'email {values['email'][-4:] != ".com"}')
        if not values['name']:
            raise ValueError("name not exist!")
        if values['email'][-4:] != '.com':
            raise ValueError("pleasee provide correct email formate!")
        return values
    
model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0,api_key=api_key)

parser = PydanticOutputParser(pydantic_object=query)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# And a query intended to prompt a language model to populate the data structure.
prompt_and_model = prompt | model
output = prompt_and_model.invoke({"query": "please if you can get salary of ishaq when his age was 30 and email ishaq@gmail.edu.pk."})
ish = parser.invoke(output)
print(ish)

'''Custom vlidation of data:
In the above code there are two validation that are explexitly mentioned and applied.
@model_validator(mode='before') -> This is validation applied to all the attribut of this class before the pydantic validation.
@classmethod is method use to do the custom validation of each variale like i have checked if eamil last four letter contain ".com".
This is how you can improve the reliability of user function tool arguments and data type consistancy with both custom validation and built in validation.
'''

'''
There are some LLM provider which uses builtin parsing method and respon in json formate.
(llm.with_structure_output(method = 'json'))
'''