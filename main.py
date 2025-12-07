from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Base URL matches the API documentation
Base_url = "https://quranapi.pages.dev/api" 
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/quran/{sorah}")
def get_sorah(request: Request, sorah: int):
    url = f"{Base_url}/{sorah}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # --- NEW CODE START ---
        # We combine the two separate lists (arabic1 and english) into one list of pairs
        # We use Python's zip() function for this.
        arabic_text = data.get('arabic1', [])
        english_text = data.get('english', [])
        
        # Create a new list 'verses' that contains both texts for each number
        verses = []
        for i, (ar, en) in enumerate(zip(arabic_text, english_text)):
            verses.append({
                "id": i + 1,
                "arabic": ar,
                "english": en
            })
            
        # Add this new list back to data so the HTML can use it
        data['formatted_verses'] = verses
        # --- NEW CODE END ---

        print(data) # Check your terminal to see the structure!
        return templates.TemplateResponse("quran.html", {"request": request, "data": data})
    else:
        return {"error": f"Sorah {sorah} not found. Status: {response.status_code}"}


@app.get("/quran/{sorah}/{aya}")
def get_aya(request: Request, sorah: int, aya: int):
    # FIXED: Removed "/quran" from the URL path
    # New URL structure: https://quranapi.pages.dev/api/1/1.json
    url = f"{Base_url}/{sorah}/{aya}.json" 
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return templates.TemplateResponse("aya.html", {"request": request, "data": data})
    else:
        return {"error": f"Aya {sorah}:{aya} not found. Status: {response.status_code}"}

