from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from utils import logger
from routers import samplerouter
from routers import weatherforecastrouter


app = FastAPI(
    title="tenmado-api",
    description="tenmadoプロジェクトのAPIの処理を担う",
    version="1.0",
    # デフォルトの応答クラスを指定: ORJSONResponseｰ>パフォーマンス高い
    default_response_class=ORJSONResponse,
)

logger.setup_logger()

# ルーティングをinclude
app.include_router(samplerouter.router)
app.include_router(weatherforecastrouter.router, prefix="/weatherforecast")
