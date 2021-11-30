import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import string
import secrets
import uvicorn
from urllib.parse import urlencode

# initialization
app = FastAPI()

load_dotenv()
id = os.getenv('CLIENT_ID')
uri = os.getenv('REDIRECT_URI')
AUTH_URL = 'https://accounts.spotify.com/authorize'

#init css static files instance to be served 
app.mount("/static", StaticFiles(directory="static"), name="static")
# init Jinja2 template instance
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/auth", response_class=HTMLResponse)
async def auth():
    
    # The state can be useful for correlating requests and responses. 
    # Because your redirect_uri can be guessed, using a state value can increase your assurance that an 
    # incoming connection is the result of an authentication request. 
    # If you generate a random string or encode the hash of some client state (e.g., a cookie) in this 
    # state variable, you can validate the response to additionally ensure that the request and response 
    # originated in the same browser. 
    # This provides protection against attacks such as cross-site request forgery. See RFC-6749.

    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    parameters = {
        'client_id': id,
        'response_type': 'code',
        'redirect_uri': str(uri),
        'scope': 'playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative',
        'state': state,
    }

    res = RedirectResponse(f'{AUTH_URL}/?{urlencode(parameters)}')
    return res


@app.get('/callback')
async def callback(request: Request):
    result=request.query_params
    return templates.TemplateResponse('token.html', {"request": request,"token":str(result)[5:-23]})

# main
if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=5000)
