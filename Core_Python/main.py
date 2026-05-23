from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = "You are a helpful maths assistant. You can answer questions about maths If user asks something other then maths just say sorry"

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content":SYSTEM_PROMPT},
        {"role": "user" ,  "content":"What is 2*2?"}
    ]
)

print(response.choices[0].message.content)

#Zero Shot prompting:Directly giving instructions to the model
#eg: SYSTEM_PROMPT = "You are a helpful maths assistant. You can answer questions about maths If user asks something other then maths just say sorry"

#few shot prompting:Giving examples to the model
#eg: SYSTEM_PROMPT = """
#Q. what is 2+2?
#A. 4
#""" 
#few shot increases the accuracy more than zero shot

#Chain of Thought Prompting:Asking the model to think step by step. Think before you answer in model

#eg: SYSTEM_PROMPT = """

