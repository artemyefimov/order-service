import uvicorn

from order_service.presentation.app_factory import create_app
from order_service.settings import Settings

settings = Settings()
app = create_app(settings)
uvicorn.run(app, host="0.0.0.0", port=8000)
