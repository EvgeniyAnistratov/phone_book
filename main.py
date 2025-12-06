from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def main():
    return "Phone book"
