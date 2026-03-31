

from fastapi import APIRouter,Depends,Query,HTTPException
from pyexpat.errors import messages
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news_cache,news
from schemas.users import UserAuthResponse, UserInfoResponse
from utils.response import success_response

# 创建 APIRouter 实例
# prefix 路由前缀（API 接口规范文档）
# tags 分组 标签
router =APIRouter(prefix='/api/news',tags=['news'])


#模块化路由
@router.get('/categories')
async  def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    #获取数据库里面的新闻分类数据-》先定义模型类-》封装查询数据方法
    categories=await news_cache.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"success",
        "data":categories,
    }
@router.get('/list')
async def get_news_list(
        #声明的参数不是路径参数时， 路径操作函数会把该参数自动解释为**查询参数**
        #查询参数 - 类型注解 Query alias 设置参数别名
        catergory_id: int=Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, le=100, alias="pageSize"),
        db:AsyncSession = Depends(get_db)
):
    offset=(page-1)*page_size
    #处理分页规则-》新闻列表-》计算总量-》计算是否还有更多
    news_list=await news_cache.get_news_list(db,catergory_id,offset,page_size)
    total_count=await  news_cache.get_news_count(db,catergory_id)
    #(跳过的+当前列表数量) < 总数量
    has_more=(offset+len(news_list)) < total_count
    return {
        "code":200,
        "message":"success",
        "data":{
            "list": news_list,
            "total":total_count,
            "hasMore":has_more
        },
    }
@router.get('/detail')
async def get_news_detail(news_id: int=Query(...,alias="id"),db:AsyncSession = Depends(get_db)):
    #获取新闻详情+浏览量+1+相关新闻
    news_detail=await news.get_news_detail(db,news_id)
    if not news_detail:
            raise  HTTPException(status_code=404,detail="新闻不存在")
    views_res=await news.increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="更新浏览量失败")
    related_news=await news.get_related_news(db,news_detail.id,news_detail.category_id)
    return {
        "code":200,
        "message":"success",
              "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
      }
    }
