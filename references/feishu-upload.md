# Feishu Drive 文件上传

## 获取 Tenant Access Token

```bash
# 从环境变量读取凭据
APP_ID=$(grep FEISHU_APP_ID /config/.hermes/.env | cut -d= -f2)
APP_SECRET=$(grep FEISHU_APP_SECRET /config/.hermes/.env | cut -d= -f2)

# 获取 token
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}"
```

返回: `{"code":0,"expire":6065,"msg":"ok","tenant_access_token":"t-xxxxx"}`

## 上传图片到指定文件夹

```bash
TOKEN="t-g1045qaAZWITHBBRN7DLRKEMRCONYKTMMPDLEZNT"
FILE_PATH="/config/Desktop/cwr/images/创作手记五-配图2-无人物.png"
FILE_SIZE=$(stat -c%s "$FILE_PATH")
FILE_NAME=$(basename "$FILE_PATH")

curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/files/upload_all" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_name=$FILE_NAME" \
  -F "parent_type=explorer" \
  -F "parent_node=L7vufdU96laeQidWF3vc9C9vnXg" \
  -F "size=$FILE_SIZE" \
  -F "file=@$FILE_PATH;type=image/png"
```

成功响应:
```json
{"code":0,"data":{"file_token":"XepabtZvjoNcR4xs3w6cgDWFnFe","version":"7644028893640297658"},"msg":"Success"}
```

## 关键参数

| 参数 | 说明 |
|------|------|
| `parent_type` | 固定为 `explorer`（云文档文件夹） |
| `parent_node` | 文件夹 token（从飞书文件夹 URL 提取） |
| `file` | `@/path/to/file;type=image/png` 格式 |
| `size` | 文件字节数（`stat -c%s` 获取） |

## 常见错误

- `file too large`: 检查 size 是否与实际文件大小一致
- `permission denied`: Bot 可能没有该文件夹的上传权限
- `invalid folder token`: 确认 parent_node 正确

## lark-cli 限制

`lark-cli file upload` 命令不可用，需使用原生 curl 调用 Feishu Open API。