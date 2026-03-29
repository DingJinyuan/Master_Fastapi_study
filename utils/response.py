from fastapi.responses import JSONResponse
#导入 数据格式化工具（把对象 → 普通 JSON）
from fastapi.encoders import jsonable_encoder

def success_response(message:str="success",data=None):
    ## 构造固定格式的返回数据
    content={
        "code":200,
        "message":message,
        "data":data
    }
    # 目标：把任何的 FastAPI、Pydantic、ORM 对象 都要正常响应 → code、message、data
    # 把 content 转成 JSON，再返回给前端
    return JSONResponse(content=jsonable_encoder(content))