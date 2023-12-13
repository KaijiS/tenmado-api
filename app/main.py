from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from routers import samplerouter, weatherforecastrouter
from utils import logger

app = FastAPI(
    title="tenmado-api",
    description="tenmadoプロジェクトのAPIの処理を担う",
    version="1.1",
    # デフォルトの応答クラスを指定: ORJSONResponseｰ>パフォーマンス高い
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tenmado-front-dev-6jbikhj2nq-an.a.run.app",
        "https://tenmado-front-6jbikhj2nq-an.a.run.app",
        "https://tenmado.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.setup_logger()

# ルーティングをinclude
app.include_router(samplerouter.router)
app.include_router(weatherforecastrouter.router, prefix="/weatherforecast")
