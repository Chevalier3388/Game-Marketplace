# marketplace/marketplace.py

import os
import sys

sys.path.append('/home/admin/PythonProject/Game_marketplace')
from fastapi import FastAPI, Request, Depends

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


import grpc

from recommendations.recommendations_pb2 import (
    GameCategory,
    RecommendationRequest,
)

from recommendations.recommendations_pb2_grpc import RecommendationsStub


app = FastAPI(title="Game Marketplace")

templates = Jinja2Templates(directory="templates")

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)

recommendations_client = RecommendationsStub(recommendations_channel)

@app.get("/", response_class=HTMLResponse)
async def render_homepage(request: Request):
    recommendations_request = RecommendationRequest(
        user_id=1, category=GameCategory.CLASSIC, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return templates.TemplateResponse(
        "homepage.html",
        {
            "request": request,
            "recommendations": recommendations_response.recommendations,
        }
    )
