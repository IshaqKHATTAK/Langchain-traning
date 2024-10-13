from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from custom_prompts import simple_assistant
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def joint_prompt(llm, system_message):
    prmpt = ChatPromptTemplate.from_messages(
        [
            ('system',"{system_message}"),
            MessagesPlaceholder(variable_name="user_input"),
        ]
    )
    prmpt = prmpt.partial(system_message = system_message)
    return prmpt | llm


llm = ChatOpenAI(model='gpt-4o-mini', api_key=api_key)
formate = simple_assistant.format(
    time_voc = 2,
    budget = '5 lac',
    countary = 'pakistan',
)
chained = joint_prompt(llm=llm,system_message=formate)
ans = chained.invoke({'user_input':[{'role':'user','content':'hi how can you help me'}],'time_voc':2, 'budget':'5 lac','countary':'pakistan'})
print(f'answer = {ans}')