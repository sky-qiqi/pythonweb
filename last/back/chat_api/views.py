# chat_api/views.py
import json
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse # 导入 StreamingHttpResponse

# !!! 安全警告 !!!
# 将 API Key 存储在环境变量或Django设置文件中，而不是直接写在代码中。
# 这里为了演示，直接写在settings中，但在生产环境请务必使用环境变量！
# 请确保你的settings.py中有 VOLCANO_ENGINE_API_KEY 和 VOLCANO_ENGINE_API_URL
# 例如:
# VOLCANO_ENGINE_API_KEY = os.environ.get('VOLCANO_ENGINE_API_KEY', '你的实际API Key')
# VOLCANO_ENGINE_API_URL = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
# VOLCANO_ENGINE_MODEL = 'doubao-1-5-thinking-pro-250415'

class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        api_messages = request.data.get('messages')
        if not api_messages:
            return Response({'error': 'Messages field is required and should follow the multi-modal structure.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Volcano Engine (Doubao) API uses key in Authorization header
            payload = {
                'model': settings.VOLCANO_ENGINE_MODEL,
                'messages': api_messages, # Doubao uses 'messages' instead of 'contents'
                'stream': True,
            }

            headers = {
                'Authorization': f'Bearer {settings.VOLCANO_ENGINE_API_KEY}',
                'Content-Type': 'application/json'
            }

            api_url = settings.VOLCANO_ENGINE_API_URL

            response = requests.post(api_url, json=payload, headers=headers, stream=True)
            response.raise_for_status()

            def event_stream():
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        try:
                            for line in chunk.decode('utf-8').splitlines():
                                if line.startswith('data:'):
                                    json_str = line[len('data:'):].strip()
                                    if json_str == '[DONE]':
                                        yield f"data: [DONE]\n\n" # 转发结束标记
                                        return # 结束生成器
                                    try:
                                        event_data = json.loads(json_str)
                                        if 'choices' in event_data and len(event_data['choices']) > 0:
                                            delta = event_data['choices'][0].get('delta')
                                            if delta and 'content' in delta:
                                                new_token = delta['content']
                                                # 发送给前端的数据格式：JSON字符串，包含 content
                                                yield f"data: {json.dumps({'content': new_token})}\n\n"
                                    except json.JSONDecodeError:
                                        pass
                                elif line.strip(): # 忽略空行，但处理非数据行
                                    # 如果有非SSE格式的行，可以在这里处理或忽略
                                    pass
                        except UnicodeDecodeError:
                            pass

            return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

        except requests.exceptions.RequestException as e:
            print(f"调用豆包 API失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                except json.JSONDecodeError:
                    error_detail = e.response.text
                return Response({'error': 'Failed to call external AI API.', 'detail': error_detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'Failed to call external AI API.', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"后端处理AI请求时发生未知错误: {e}")
            return Response({'error': 'An unexpected error occurred on the backend.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)