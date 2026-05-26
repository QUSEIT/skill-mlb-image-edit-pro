# MuleRun Nano Banana Pro Image Edit API Reference

## 环境变量

```bash
export MLB_API_KEY="your_api_key_here"
```

## API Endpoint

```
POST https://api.mulerun.com/vendors/google/v1/nano-banana-pro/edit
Authorization: Bearer {MLB_API_KEY}
Content-Type: application/json
```

```
GET https://api.mulerun.com/vendors/google/v1/nano-banana-pro/edit/{task_id}
Authorization: Bearer {MLB_API_KEY}
```

---

## Pro 图片编辑函数

```python
import os
import base64
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = "/config/.hermes/.env"
load_dotenv(ENV_PATH, override=False)

MLB_API_KEY = os.environ.get("MLB_API_KEY", "")
MLB_BASE_URL = "https://api.mulerun.com/vendors/google/v1/nano-banana-pro"


def mlb_image_edit_pro(
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
    MuleRun Nano Banana Pro 高保真图片编辑 API（异步任务模式）

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
        {"task_id": str, "status": str, "image_urls": list, "description": str, "local_paths": list}
    """
    if not MLB_API_KEY:
        raise ValueError("请设置环境变量 MLB_API_KEY")

    headers = {
        "Authorization": f"Bearer {MLB_API_KEY}",
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
        f"{MLB_BASE_URL}/edit",
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
            f"{MLB_BASE_URL}/edit/{task_id}",
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
```

---

## 查询任务状态

```python
def mlb_get_pro_edit_task(task_id: str) -> dict:
    """
    查询指定 Pro 编辑任务的状态和结果

    Returns:
        {"task_id": str, "status": str, "image_urls": list, "description": str, "error": dict}
    """
    if not MLB_API_KEY:
        raise ValueError("请设置环境变量 MLB_API_KEY")

    headers = {"Authorization": f"Bearer {MLB_API_KEY}"}

    response = requests.get(
        f"{MLB_BASE_URL}/edit/{task_id}",
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
```

---

## 辅助函数

```python
def _download_images(image_urls: list, output_dir: str, prefix: str = "mlb_pro_edit") -> list:
    """下载图片到本地目录"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, url in enumerate(image_urls):
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if resp.status_code == 200:
                ext = "png" if "image/png" in resp.headers.get("Content-Type", "") else "jpg"
                filepath = output_path / f"{prefix}_{i+1}.{ext}"
                filepath.write_bytes(resp.content)
                saved.append(str(filepath))
                print(f"[Download] Saved: {filepath}")
            else:
                print(f"[Download] Failed ({resp.status_code}): {url[:80]}")
        except Exception as e:
            print(f"[Download] Error: {e}")
    return saved
```

---

## 响应格式

### 提交任务 (POST /nano-banana-pro/edit)

```json
{
  "task_info": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "pending",
    "created_at": "2025-09-21T00:00:00.000Z",
    "updated_at": "2025-09-21T00:00:00.000Z"
  }
}
```

### 查询结果 (GET /nano-banana-pro/edit/{task_id})

**完成状态**:
```json
{
  "task_info": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed",
    "created_at": "2025-09-21T00:00:00.000Z",
    "updated_at": "2025-09-21T00:00:00.000Z"
  },
  "images": [
    "https://example.com/image.png"
  ],
  "description": "A beautiful sunset over the mountains"
}
```

---

## Pro 版 vs 标准版对比速查

| 特性 | 标准版 (nano-banana-2) | Pro 版 (nano-banana-pro) |
|------|----------------------|-------------------------|
| 端点 | `/nano-banana-2/edit` | `/nano-banana-pro/edit` |
| 状态 | 稳定 | Beta 公测 |
| 参考图上限 | 14 | 10 |
| 分辨率 | 1K/2K/**4K** | 1K/2K（无 4K） |
| 默认分辨率 | 1K | **2K** |
| 宽高比 | 14 种 | 10 种（无 1:4,1:8,4:1,8:1） |
| web_search | ✅ | ❌ |
| 保真度 | 标准 | **更高** |
