from fastapi import FastAPI, Request, WebSocket, Body, Depends, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from decouple import config
import re
import bcrypt

from auth.jwt_handles import signJWT, decodeJWT
from auth.jwt_bearer import jwtBearer


from function import *
from classes import *


salt = str(config("salt"))
bearer = jwtBearer(auto_Error=True)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

response = ResponseMessage()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse, dependencies=[Depends(bearer)])
def home(request: Request):
    print(request.body)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/user/signup")
def user_signup(user: UserSchema = Body(default=None)):
    alphanumeric_regex = "^[a-zA-Z0-9]+$"
    if(bool(re.match(alphanumeric_regex, user.user_name)) and user.password.find(' ') == -1):
        if(check_user_already_used(user.user_name) == False):
            salt = bcrypt.gensalt()
            passhash = bcrypt.hashpw(user.password.encode('utf-8'), salt)
            add_user_to_database(user.user_name, user.email, passhash.decode("utf-8"), salt.decode('utf-8'))
            return signJWT(user.user_name)
        else:
            return{"detail": "email already used"}
    else:
        return response.succes  

        
@app.post("/user/login")
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        salt = get_salt(user.user_name)[0][0]
        if check_user_total(user.user_name, user.password, salt):
            return signJWT(user.user_name)
        else:
           return {"error":"invalid login details!"} 
    else:
        return {"error":"invalid login details!"}
    

@app.post("/api", dependencies=[Depends(bearer)])
def API_function(input):
    userID = decodeJWT(input).get("userID")
    return userID