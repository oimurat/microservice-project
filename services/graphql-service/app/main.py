import os

import resolvers
import strawberry
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

# [1] schema.graphql       ← 定義：何ができるか
#  ↓
# [2] resolvers.py         ← 実装：実際に何をするか
#  ↓
# [3] grpc_clients/        ← 各gRPCマイクロサービスの呼び出しラッパー
#  ↓
# [4] gRPC Service         ← マイクロサービス実体（order, payment など）

schema = strawberry.Schema(
    query=resolvers.Query,
    mutation=resolvers.Mutation,
    config=StrawberryConfig(auto_camel_case=False)
)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

# static ディレクトリをマウント（HTML配置先）
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# /ui エンドポイントで HTML を返す
@app.get("/ui", response_class=HTMLResponse)
async def graphql_ui():
    with open(os.path.join(static_dir, "graphql_ui.html")) as f:
        return f.read()


@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/ui")