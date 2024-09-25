import os

def logger(model:str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            with open(os.environ["LLM_CALL_LOG_DIR"], "a") as file:
                file.write(f"Model: {model} \n Input Prompt: {args}{kwargs}\n Model Response: {response}\n\n")
            return response
        return wrapper
    return decorator