import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import json

from scraper import extract_all_reactions
from ml_analyzer import analyze_profile_sync
from notifier import send_email_report

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PRODUCTS = {
    "1": {"id": "1", "name": "AI Reaction Analyzer", "price": "$49", "author": "NexusAI Team", "desc": "Scrape and score reactions in real-time.", "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=400&q=80"},
    "2": {"id": "2", "name": "Viral Post Predictor", "price": "$29", "author": "GrowthHackers", "desc": "Predict the virality of your post before publishing.", "img": "https://images.unsplash.com/photo-1678280434720-e22648fb4f97?auto=format&fit=crop&w=400&q=80"},
    "3": {"id": "3", "name": "Cold DM Auto-Generator", "price": "$99", "author": "SalesBotInc", "desc": "Generate hundreds of custom DMs based on profiles.", "img": "https://images.unsplash.com/photo-1679083216051-aa510a1a2c0e?auto=format&fit=crop&w=400&q=80"},
    "4": {"id": "4", "name": "Competitor Insight", "price": "$149", "author": "SpyGlass", "desc": "Analyze competitor strategies secretly.", "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=400&q=80"}
}

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"You are an expert LinkedIn growth strategist for 10x Automations. Keep answers under 3 sentences and professional but futuristic. User says: {req.message}"
        response = await asyncio.to_thread(model.generate_content, prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"System Error: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/features", response_class=HTMLResponse)
async def read_features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@app.get("/pricing", response_class=HTMLResponse)
async def read_pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.get("/meeting", response_class=HTMLResponse)
async def read_meeting(request: Request):
    return templates.TemplateResponse("meeting.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/marketplace", response_class=HTMLResponse)
async def read_marketplace(request: Request):
    return templates.TemplateResponse("marketplace.html", {"request": request, "products": PRODUCTS.values()})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def read_product(request: Request, product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse("product.html", {"request": request, "product": product})

@app.get("/vendor", response_class=HTMLResponse)
async def read_vendor(request: Request):
    return templates.TemplateResponse("vendor.html", {"request": request})

@app.get("/library", response_class=HTMLResponse)
async def read_library(request: Request):
    return templates.TemplateResponse("library.html", {"request": request})

@app.websocket("/ws/analyze")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        payload = json.loads(data)
        post_url = payload.get("post_url")
        li_at_cookie = payload.get("li_at_cookie")
        target_email = payload.get("target_email")
        
        if not post_url or not li_at_cookie:
            await websocket.send_json({"type": "error", "message": "Missing credentials or URL"})
            await websocket.close()
            return
            
        await websocket.send_json({"type": "status", "message": "Initializing Scraper Engine..."})
        
        queue = asyncio.Queue()
        scraper_task = asyncio.create_task(extract_all_reactions(post_url, li_at_cookie, queue))
        
        all_profiles = []
        
        while True:
            profile = await queue.get()
            if profile is None:
                break
                
            await websocket.send_json({"type": "status", "message": "Analyzing " + profile['name'] + "..."})
            
            ai_data = await asyncio.to_thread(analyze_profile_sync, profile)
            enriched_profile = {**profile, **ai_data}
            all_profiles.append(enriched_profile)
            
            await websocket.send_json({"type": "profile", "data": enriched_profile})
            
        await websocket.send_json({"type": "status", "message": "Scraping Complete. Sending report..."})
        
        if all_profiles and target_email:
            report = "LinkedIn Reaction Analysis Report\n\n"
            for p in sorted(all_profiles, key=lambda x: x.get('score', 0), reverse=True):
                report += f"Name: {p['name']}\nHeadline: {p['headline']}\nURL: {p['url']}\nScore: {p.get('score')}\nCategory: {p.get('category')}\nOutreach: {p.get('outreach')}\n\n"
            await asyncio.to_thread(send_email_report, report, target_email)
            
        await websocket.send_json({"type": "complete", "message": "Process finished successfully."})
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
