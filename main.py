from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, users, favorite, history
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
#注册异常处理器
register_exception_handlers(app)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #云讯的原 开发允许所有，生产环境只允许指定域名
    allow_credentials=True, #允许携带cookie
    allow_methods=["*"], #允许所有方法
    allow_headers=["*"], #允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)