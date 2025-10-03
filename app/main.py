from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from text_blind_watermark import TextBlindWatermark

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/embed", response_class=HTMLResponse)
def 嵌入(request: Request, text: str = Form(...), wm: str = Form(...), pwd: str = Form(...)):
    try:
        twm = TextBlindWatermark(pwd=pwd.encode())
        result = twm.add_wm_rnd(text=text, wm=wm.encode())
        return templates.TemplateResponse("index.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

@app.post("/extract", response_class=HTMLResponse)
def extract(request: Request, text: str = Form(...), pwd: str = Form(...)):
    try:
        twm = TextBlindWatermark(pwd=pwd.encode())
        wm = twm.extract(text)。decode()
        return templates.TemplateResponse("index.html", {"request": request, "extracted": wm})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})
