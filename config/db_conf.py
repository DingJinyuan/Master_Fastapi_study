from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# 数据库URL
ASYNC_DATABASE_URL="mysql+aiomysql://root:Qq112233@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎 创建异步数据库连接
async_engine = create_async_engine(
ASYNC_DATABASE_URL,
echo=True, # 可选：输出SQL⽇志
pool_size=10, # 设置连接池中保持的持久连接数
max_overflow=20 # 设置连接池允许创建的额外连接数
)
# 创建异步会话⼯⼚ 用于批量生成数据库会话
AsyncSessionLocal = async_sessionmaker(
bind=async_engine,
class_=AsyncSession,
expire_on_commit=False
)
# 依赖项，⽤于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()