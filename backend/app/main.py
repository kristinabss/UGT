from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .core.config import settings
from .api.technologies import router as technologies_router
from .api.products import router as products_router
from .api.dashboard import router as dashboard_router

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Прототип системы определения уровня готовности технологий (УГТ)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(technologies_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Корневой endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Система определения уровня готовности технологий",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Проверка работоспособности системы."""
    return {"status": "healthy"}
