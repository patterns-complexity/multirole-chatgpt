# %% Imports
import tkinter as tk
import openai


from dotenv import load_dotenv
from os import environ
from json import loads

# %% Load environment variables
load_dotenv()
api_key = environ['OPENAI_API_KEY']

# %% Load initial messages
with open('initial_message.md') as f:
    manager_initial_message = f.read()
    
with open('model_initial_message.md') as f:
    model_initial_message = f.read()
    
with open('qa_initial_message.md') as f:
    qa_initial_message = f.read()
    
# %% Load functions
with open('functions.json') as f:
    functions = loads(f.read())

# %% Load API key
openai.api_key = api_key

# %% Define messages
history = []

# %% Define the function to ask QA
def ask_qa():
    ask_model("smart", "Quality Assurance", history_override=history)
    
# %% Define the function to spawn models
def spawn_models(roles: list[str], types: list[str], queries: list[str]):
    role_counter = 0
    for role in roles:
        ask_model(types[role_counter], role, queries[role_counter])
        role_counter += 1
    ask_qa()
    ask_manager(
        "system",
        "All models answered! Time to decide! \
        If you are ready to answer the user then don't run any functions and respond in a normal way. \
        Otherwise, run the function again. \
        REMEMBER TO LISTEN TO THE QA!"
    )
            
# %% Define the function dictionary
fns = {
    "spawn_models": spawn_models
}

# %% Define the communication loop
def send_request(model, message_history, model_functions = None):
    if model_functions is not None:
        return openai.ChatCompletion.create(
        model=model,
        messages=message_history,
        functions=model_functions,
    )
    else:
        return openai.ChatCompletion.create(
            model=model,
            messages=message_history,
        )

def ask_manager(name, query):
    print("Asking the manager...")

    if len(history) == 0:
        history.append({ "role": "system", "content": manager_initial_message.format(name, query) })
        
    history.append({ "role": name, "content": query })
    
    response = send_request("gpt-4", history, functions)
    
    response_message = response.choices[0].message
    
    history.append(response_message)
    
    if "function_call" in response_message:
        function_name: str = response_message["function_call"]["name"]
        function_arguments: dict[str, str] = loads(response_message["function_call"]["arguments"])
    
        print(f"The manager decided to ask those models: {', '.join(function_arguments['roles'])}")
        
        # Run function_name with function_arguments
        fns[function_name](**function_arguments)
    else:
        print("-" * 50)
        print("Answer:\n")
        print(response_message["content"])
    
def ask_model(type, role, query = None, history_override = None, is_user = False):
    if role != "Quality Assurance":
        print(f"Asking model of role {role} and {'low' if type == 'dumb' else 'high'} IQ - {query}...")
    else:
        print(f"Asking QA...")
    
    own_history = []
    
    if len(own_history) == 0:
        if role != "Quality Assurance":
            own_history.append({ "role": "system", "content": model_initial_message.format(type=type, role=role) })
        else:
            own_history.append({ "role": "system", "content": qa_initial_message })
    
    if history_override is not None:
        # Prepend the history override
        own_history = history_override + own_history
    
    if query is not None:    
        own_history.append({ "role": "user" if is_user is True else "system", "content": query })
        
    response = send_request("gpt-3.5-turbo" if type == "dumb" else "gpt-4", own_history)
    
    response_message = response.choices[0].message
    
    history.append({ "role": "system", "content": f"Model of role {role} and {'low' if type == 'dumb' else 'high'} IQ said: {response_message['content']}" })
    
    if role == "Quality Assurance":
        print("-" * 50)
        print("QA Said:\n")
        print(response_message["content"])
    
    
# %% Debug
while True:
    # Ask the user for a question
    query = str(input("Question: "))

    print("-" * 50)
    
    # Print the question asked
    print("User asked:", query)
    
    # Ask the manager
    ask_manager("user", query)
    
    print("-" * 50)

# %%