import os
import requests # 导入 requests 库
import traceback # 添加 traceback 用于打印详细错误信息
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 重要提示：在生产环境中，切勿将API密钥硬编码在此处。
# 推荐使用环境变量或其他安全方式存储。
# os.environ['GOOGLE_API_KEY'] = 'YOUR_API_KEY'
API_KEY = 'sk-UUlLWbSNQcZxQOWFwiI3o6B0T0gpCVgl9EmAGZHoWjEi7bcT' # Kimi API 密钥

# Removed global model and chat initialization
# Initialization will now happen inside the chat_endpoint function

@app.route('/')
def index():
    # 提供 index.html 文件
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def script():
    # 提供 script.js 文件
    return send_from_directory('.', 'script.js')

@app.route('/page1.html')
def page1():
    # 提供 page1.html 文件
    return send_from_directory('.', 'page1.html')

@app.route('/page2.html')
def page2():
    # 提供 page2.html 文件
    return send_from_directory('.', 'page2.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint(): # <-- Revert to synchronous route
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        print(f"Sending message to Kimi: {user_message}")
        # 调用 Kimi API
        kimi_api_endpoint = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {
            "model": "moonshot-v1-8k", # 或者选择其他 Kimi 模型
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.3 # 可以根据需要调整
        }

        response = requests.post(kimi_api_endpoint, headers=headers, json=payload)
        response.raise_for_status() # 如果请求失败（状态码不是 2xx），则抛出 HTTPError

        response_data = response.json()
        # 检查 Kimi API 返回的数据结构，提取回复内容
        if response_data and 'choices' in response_data and len(response_data['choices']) > 0:
            ai_reply = response_data['choices'][0]['message']['content']
        else:
            ai_reply = "抱歉，未能从 Kimi 获取有效回复。"
            print(f"Unexpected Kimi API response format: {response_data}")

        print(f"Received reply from Kimi: {ai_reply}")
        return jsonify({'reply': ai_reply})

    except requests.exceptions.RequestException as e:
        # 捕获 requests 库相关的错误 (例如网络问题、超时)
        print(f"Error communicating with Kimi API (RequestException): {e}")
        traceback.print_exc()
        return jsonify({'reply': f'抱歉，与 Kimi API 通信时发生网络错误: {e}'}), 500
    except Exception as e:
        # 捕获其他通用错误 (例如 JSON 解析错误、Kimi API 返回的特定错误码处理等)
        print(f"General Error communicating with Kimi API: {e}")
        traceback.print_exc()
        # 尝试打印 Kimi 返回的具体错误信息（如果可用）
        try:
            error_details = response.json()
            print(f"Kimi API Error Details: {error_details}")
            error_message = error_details.get('error', {}).get('message', str(e))
            return jsonify({'reply': f'抱歉，与 Kimi API 通信时发生错误: {error_message}'}), 500
        except:
             return jsonify({'reply': f'抱歉，与 Kimi API 通信时发生一般错误: {e}'}), 500
    except BaseException as e:
        # 捕获所有其他可能的异常，包括系统级错误
        print(f"Caught BaseException: {e}")
        traceback.print_exc() # 打印详细堆栈跟踪
        return jsonify({'reply': f'抱歉，发生了一个意外的基础错误: {e}'}), 500

if __name__ == '__main__':
    # 使用 0.0.0.0 使其在本地网络中可访问
    app.run(host='0.0.0.0', port=5000, debug=True) # Re-enable debug mode