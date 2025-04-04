from fastapi import FastAPI
from routes import user


def create_application():
    application = FastAPI()
    application.include_router(user.user_router)
    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "Hi, I am Otienoh CJ. Awesome - My setup is done & working."}
