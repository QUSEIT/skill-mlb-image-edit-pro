#!/usr/bin/env python3
"""
MuleRun Nano Banana Pro Image Edit - Working Reference Script
基于 Gemini Nano-Banana Pro 的高保真图生图编辑实现

采用异步任务模式：
1. POST /nano-banana-pro/edit → 创建任务，返回 task_id
2. GET /nano-banana-pro/edit/{task_id} → 轮询直到 completed/failed

支持最多 10 张参考图，支持 URL 和本地文件。
本地文件自动转为 data:image/xxx;base64,{data} 格式。

⚠️ 注意：此模型目前处于 Beta 公测阶段，可能不稳定。

环境变量：
- MLB_API_KEY（获取地址：https://mulerun.com 控制台）
"""
import os
import sys
import json
import time
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# ENV SETUP
# ============================================================================
ENV_PATH = "/config/.hermes/.env"
load_dotenv(ENV_PATH, override=False)

API_KEY = os.environ.get("MLB_API_KEY", "")
BASE_URL = "https://api.mulerun.com/vendors/google/v1/nano-banana-pro"

if not API_KEY:
    raise ValueError(
        f"MLB API Key not found. "
        f"Please ensure MLB_API_KEY is set in {ENV_PATH}"
    )


# ============================================================================
# Pro Image Edit - 高保真图片编辑（异步任务模式）
# ============================================================================
def image_edit_pro(
    prompt: str,
    images: list,
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    output_dir: str = "/config/Desktop",
    download: bool = True,
    poll_interval: int = 3,
    max_wait: int = 120,
) -> dict:
    """
    Nano Banana Pro 高保真图片编辑 API（异步任务模式）

    Args:
        prompt: 编辑指令
        images: 参考图片列表（URL 或本地路径，1-10 张）
        aspect_ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
                      注意：不支持 1:4, 1:8, 4:1, 8:1
        resolution: 1K / 2K（必须大写 K，不支持 4K，默认 2K）
        output_dir: 下载目录
        download: 是否下载到本地
        poll_interval: 轮询间隔（秒）
        max_wait: 最大等待时间（秒）

    Returns:
        {"task_id", "status", "image_urls", "description", "local_paths"}
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 处理参考图：URL 直接用，本地文件转 Base64 data URI
    processed_images = []
    for img in images:
        if img.startswith(("http://", "https://")):
            processed_images.append(img)
        elif os.path.isfile(img):
            with open(img, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            # 根据文件扩展名判断 MIME 类型
            ext = Path(img).suffix.lower()
            mime = "image/png" if ext == ".png" else \
                   "image/jpeg" if ext in (".jpg", ".jpeg") else \
                   "image/webp" if ext == ".webp" else \
                   "image/bmp" if ext == ".bmp" else "image/png"
            processed_images.append(f"data:{mime};base64,{b64}")
        else:
            raise ValueError(f"Invalid image path or URL: {img}")

    if len(processed_images) > 10:
        raise ValueError(f"Too many reference images: {len(processed_images)} (max 10 for Pro)")

    # Step 1: Submit task
    payload = {
        "prompt": prompt,
        "images": processed_images,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    print(f"[Pro Edit] Submitting task: {len(processed_images)} ref image(s), ratio={aspect_ratio}, resolution={resolution}")
    print(f"[Pro Edit] Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    response = requests.post(
        f"{BASE_URL}/edit",
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code not in (200, 202):
        raise RuntimeError(f"Task submission failed: HTTP {response.status_code} - {response.text}")

    result = response.json()
    task_info = result.get("task_info", {})
    task_id = task_info.get("id")
    status = task_info.get("status")

    if not task_id:
        raise RuntimeError(f"No task_id returned: {result}")

    print(f"[Pro Edit] Task created: {task_id}, status={status}")

    # Step 2: Poll for result
    image_urls = []
    description = ""
    final_status = status

    start_time = time.time()
    while final_status in ("pending", "processing"):
        if time.time() - start_time > max_wait:
            raise TimeoutError(f"Task {task_id} timed out after {max_wait}s")

        time.sleep(poll_interval)

        poll_resp = requests.get(
            f"{BASE_URL}/edit/{task_id}",
            headers=headers,
            timeout=30
        )
        poll_result = poll_resp.json()

        task_info = poll_result.get("task_info", {})
        final_status = task_info.get("status")

        print(f"[Pro Edit] Polling... status={final_status}")

        if final_status == "completed":
            image_urls = poll_result.get("images", [])
            description = poll_result.get("description", "")
            print(f"[Pro Edit] Completed! {len(image_urls)} image(s)")
            break
        elif final_status == "failed":
            error = task_info.get("error", {})
            raise RuntimeError(
                f"Task failed: [{error.get('code')}] {error.get('title')} - {error.get('detail')}"
            )

    # Step 3: Download
    local_paths = []
    if image_urls and download:
        local_paths = _download_images(image_urls, output_dir, prefix="mlb_pro_edit")

    return {
        "task_id": task_id,
        "status": final_status,
        "image_urls": image_urls,
        "description": description,
        "local_paths": local_paths,
    }


# ============================================================================
# Get Task Status
# ============================================================================
def get_task(task_id: str) -> dict:
    """
    查询指定 Pro 编辑任务的状态和结果

    Returns:
        {"task_id", "status", "image_urls", "description", "error"}
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(
        f"{BASE_URL}/edit/{task_id}",
        headers=headers,
        timeout=30
    )

    result = response.json()
    task_info = result.get("task_info", {})

    return {
        "task_id": task_info.get("id"),
        "status": task_info.get("status"),
        "image_urls": result.get("images", []),
        "description": result.get("description", ""),
        "error": task_info.get("error"),
    }


# ============================================================================
# Internal Utils
# ============================================================================
def _download_images(urls: list, output_dir: str, prefix: str = "mlb_pro_edit") -> list:
    """
    下载图片到本地

    关键：添加 User-Agent 避免 403
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    saved = []
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if resp.status_code == 200:
                ext = "png" if "image/png" in resp.headers.get("Content-Type", "") else "jpg"
                path = Path(output_dir) / f"{prefix}_{i+1}.{ext}"
                path.write_bytes(resp.content)
                saved.append(str(path))
                print(f"[Download] Saved: {path}")
            else:
                print(f"[Download] Failed ({resp.status_code}): {url[:80]}")
        except Exception as e:
            print(f"[Download] Error: {e}")
    return saved


# ============================================================================
# CLI Entry
# ============================================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MuleRun Nano Banana Pro Image Edit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Edit
    edit = sub.add_parser("edit", help="Pro 图片编辑")
    edit.add_argument("--prompt", "-p", required=True, help="编辑指令")
    edit.add_argument("--images", "-i", nargs="+", required=True,
                      help="参考图片（URL 或本地路径，可多个，最多10张）")
    edit.add_argument("--ratio", "-r", default="1:1",
                      choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5",
                               "5:4", "9:16", "16:9", "21:9"],
                      help="宽高比（Pro不支持1:4,1:8,4:1,8:1）")
    edit.add_argument("--resolution", default="2K", choices=["1K", "2K"],
                      help="分辨率（必须大写K，不支持4K，默认2K）")
    edit.add_argument("--output", "-o", default="/config/Desktop", help="输出目录")
    edit.add_argument("--no-download", action="store_true", help="仅返回 URL 不下载")
    edit.add_argument("--poll-interval", type=int, default=3, help="轮询间隔（秒）")
    edit.add_argument("--max-wait", type=int, default=120, help="最大等待时间（秒）")

    # Status
    status = sub.add_parser("status", help="查询任务状态")
    status.add_argument("task_id", help="任务ID")

    args = parser.parse_args()

    if args.cmd == "edit":
        result = image_edit_pro(
            prompt=args.prompt,
            images=args.images,
            aspect_ratio=args.ratio,
            resolution=args.resolution,
            output_dir=args.output,
            download=not args.no_download,
            poll_interval=args.poll_interval,
            max_wait=args.max_wait,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.cmd == "status":
        result = get_task(args.task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
