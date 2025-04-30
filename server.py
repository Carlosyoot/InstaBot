from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import instabot  

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    try:
        result = instabot.login(data.username, data.password)
        return {"message": "Login feito com sucesso", **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/mensagens")
async def get_mensagens():
    try:
        mensagens = instabot.ProcessarBusca()
        return JSONResponse(
            content=mensagens,
            status_code=200
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar mensagens: {str(e)}"
        )

