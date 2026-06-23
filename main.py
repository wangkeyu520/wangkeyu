from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import logging
import time
from functools import wraps
from typing import Callable, Dict, Any
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sunny Tea House AI评价生成器",
    description="AI辅助生成符合特定社交平台风格的评价",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "sk-cb38a6aa4cbc466aa37100f289f45eb6"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60

client_request_counts: Dict[str, list] = defaultdict(list)

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    
                    if attempt < max_retries - 1:
                        logger.info(f"等待 {current_delay} 秒后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
            
            logger.error(f"请求重试 {max_retries} 次后仍失败: {str(last_exception)}")
            raise last_exception
        
        return wrapper
    
    return decorator

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    logger.info(
        f"收到请求: {request.method} {request.url} "
        f"IP: {request.client.host} "
        f"Headers: {dict(request.headers)}"
    )
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"请求完成: {request.method} {request.url} "
            f"状态码: {response.status_code} "
            f"耗时: {process_time:.2f}s"
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        
        logger.error(
            f"请求异常: {request.method} {request.url} "
            f"错误: {str(e)} "
            f"耗时: {process_time:.2f}s",
            exc_info=True
        )
        
        raise

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    client_request_counts[client_ip] = [
        t for t in client_request_counts[client_ip]
        if current_time - t < RATE_LIMIT_WINDOW
    ]
    
    if len(client_request_counts[client_ip]) >= RATE_LIMIT:
        logger.warning(f"IP {client_ip} 请求频率过高，已达到限流阈值")
        raise HTTPException(
            status_code=429,
            detail=f"请求过于频繁，请等待 {RATE_LIMIT_WINDOW} 秒后再试"
        )
    
    client_request_counts[client_ip].append(current_time)
    
    return await call_next(request)

@retry_on_failure(max_retries=3, delay=1.0, backoff_factor=2.0)
def call_ai_api(model_name: str, messages: list):
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    logger.info(f"调用AI API: {model_name}, 消息数: {len(messages)}")
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    logger.info(f"AI API响应成功，状态码: {response.status_code}")
    
    return response.json()

class StoreInfo(BaseModel):
    name: str
    location: str
    rating: float = 4.8

class GenerateReviewRequest(BaseModel):
    feeling_tags: list[str]
    platform: str
    store_info: StoreInfo

class GenerateReviewResponse(BaseModel):
    success: bool
    review: dict

GOOGLE_PROMPT_TEMPLATE = """你是一个在{store_name}（位于{location}）消费过的顾客。

请根据以下感受标签生成一条Google风格的英文评价：
- 感受标签：{tags}

要求：
1. 使用英文，简洁实用
2. 3-5句话，不超过100词
3. 提到店铺名称和地点
4. 包含正面评价和推荐
5. 自然真诚，不要过于夸张

示例风格：
"Great service at Sunny Tea House in San Jose! The drinks were excellent and ready quickly. Will definitely come back!"

请直接返回评价内容，不要添加任何其他文字。"""

XIAOHONGSHU_PROMPT_TEMPLATE = """你是一个在{store_name}（位于{location}）消费过的年轻女生。

请根据以下感受标签生成一条小红书风格的中文评价：
- 感受标签：{tags}

要求：
1. 使用中文，种草风格
2. 语气活泼，使用表情符号
3. 包含话题标签（如#奶茶推荐 #探店）
4. 提到店铺名称和地点
5. 不超过200字

示例风格：
"姐妹们！Sunny Tea House真的绝了🥤
服务超级好，店员小姐姐很热情～
饮品颜值超高，拍照发朋友圈绝绝子！
地址在San Jose，快来打卡吧！

#奶茶推荐 #探店 #SunnyTea"

请直接返回评价内容，不要添加任何其他文字。"""

@app.post("/api/generate-review", tags=["评价生成"])
async def generate_review(request: GenerateReviewRequest):
    try:
        logger.info(
            f"收到评价生成请求: 平台={request.platform}, "
            f"标签={request.feeling_tags}, "
            f"店铺={request.store_info.name}"
        )
        
        tags_str = ", ".join(request.feeling_tags)
        
        if request.platform == "google":
            prompt = GOOGLE_PROMPT_TEMPLATE.format(
                store_name=request.store_info.name,
                location=request.store_info.location,
                tags=tags_str
            )
            model_name = "qwen-plus"
        elif request.platform == "xiaohongshu":
            prompt = XIAOHONGSHU_PROMPT_TEMPLATE.format(
                store_name=request.store_info.name,
                location=request.store_info.location,
                tags=tags_str
            )
            model_name = "qwen-plus"
        else:
            logger.error(f"不支持的平台类型: {request.platform}")
            raise HTTPException(status_code=400, detail="不支持的平台类型")
        
        logger.info(f"调用大模型: {model_name}")
        
        messages = [
            {
                "role": "system",
                "content": "你是一名专业的评价助手，擅长生成符合各种社交平台风格的评价内容。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response_data = call_ai_api(model_name, messages)
        
        if "choices" not in response_data or len(response_data["choices"]) == 0:
            logger.error(f"AI API返回格式错误: {response_data}")
            raise HTTPException(status_code=500, detail="AI返回格式错误")
        
        result_text = response_data["choices"][0]["message"]["content"].strip()
        
        logger.info(f"大模型返回成功，内容长度: {len(result_text)}")
        
        return {
            "success": True,
            "review": {
                "content": result_text,
                "platform": request.platform,
                "tags": request.feeling_tags,
                "store_name": request.store_info.name,
                "location": request.store_info.location
            }
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"网络连接失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail="网络连接失败，请稍后重试")
    
    except KeyError as e:
        logger.error(f"API返回格式错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="API返回格式错误")
    
    except Exception as e:
        logger.error(f"未知错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成评价失败: {str(e)}")

@app.get("/api/health", tags=["健康检查"])
async def health():
    logger.info("健康检查请求")
    return {"status": "ok", "message": "服务正常运行"}

@app.get("/", tags=["首页"])
async def root():
    return {"message": "Sunny Tea House AI评价生成器 API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

handler = app
