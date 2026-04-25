from dotenv import load_dotenv
from pypdf import PdfReader
import gradio as gr
from openai import OpenAI
from pydantic import BaseModel
from groq import Groq

load_dotenv(override=True)
reader = []
text = ""
summary = ""
name= "Harpreet Singh Walia"
openAI = OpenAI()
groq_client = Groq()

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


reader = PdfReader("me/Profile.pdf")
for page in reader.pages:
    text += page.extract_text()

with open("me/summary.txt","r") as f:
    summary = f.read()

#System Prompt
system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{text}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."


#Evaluator Prompt

evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {name} and is representing {name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {name} in the form of their summary and LinkedIn details. Here's the information:"

evaluator_system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{text}\n\n"
evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."


def callfirstLLM(message, history):
    messages = [{"role": "system", "content": system_prompt}]+history+[{"role": "user", "content": message}]
    response = openAI.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content

def evaluator_user_prompt(message, history, reply):
    return f"Evaluate the following response from the agent:\n\nUser: {message}\n\nAgent: {reply}\n\nWas the response acceptable? (yes/no)\n\nIf no, please provide feedback on how to improve the response. Here is conversation history {history} for context."

def evaluate(message, history, reply)->Evaluation:
    messages = [{"role": "system", "content": evaluator_system_prompt}]+[{"role": "user", "content": evaluator_user_prompt(message, history, reply)}]
    response = openAI.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=Evaluation
    )
    print(response.choices[0].message.parsed)
    return response.choices[0].message.parsed

def rerun(message, history, feedback):
    #call open ai client and get the response
    updated_system_prompt= system_prompt + f"\n\n## Your answer was rejected so use this Feedback for Improvement:\n{feedback}\n\n Please use this feedback to improve your response and answer the user's question again."
    messages = [{"role": "system", "content": updated_system_prompt}]+history+[{"role": "user", "content": message}]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    return response.choices[0].message.content

def chat(message, history):
    #call open ai client and get the response
    response = callfirstLLM(message, history)

    #send the response to evaluater and get verified
    evaluation = evaluate(message, history, response)
    
    print(evaluation.feedback)
    
    #if / else to validate response 
    if evaluation.is_acceptable:
         return response
    else:
        return rerun(message, history, evaluation.feedback)
    

gr.ChatInterface(chat,type="messages").launch()