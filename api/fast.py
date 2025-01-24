from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    """home page"""
    return {'Greeting': 'This is the API for the anaylsis'}
