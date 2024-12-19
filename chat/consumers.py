import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
from django.conf import settings
from .prompt_engineering import prompt

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # OpenAI API 호출
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
                # {"role": "user", "content": "2024년 글로벌 및 한국 경제 전망을 바탕으로 수익성 높은 사업 기회는 무엇인가요?"},
                # {"role": "system", "content": "2024년 경제 전망을 분석한 결과, 다음과 같은 수익성 높은 사업 기회가 있습니다 : AI 및 첨단 기술 산업: 글로벌 IT 시장의 회복세와 AI에 대한 수요 확대로 인해 관련 기술 개발 및 서비스 제공 사업이 유망합니다. 특히 반도체 산업의 성장이 두드러질 것으로 예상됩니다. 글로벌 수출 중심 비즈니스: 2024년 세계 경제 성장률이 3.0%로 전망되며, 한국의 수출은 5.0% 성장할 것으로 예측됩니다. 국제 시장을 겨냥한 제품 개발 및 수출 관련 서비스 사업이 유망합니다. 디지털 플랫폼 및 온라인 서비스: 소비자들의 온라인 활동 증가에 따라 e-커머스, 디지털 콘텐츠, 온라인 교육 등의 사업 기회가 확대될 것으로 예상됩니다. 친환경 및 지속가능성 관련 사업: 글로벌 트렌드에 맞춘 친환경 제품 개발, 재생 에너지 사업, 탄소 배출 저감 기술 등이 주목받을 것입니다. 헬스케어 및 바이오 산업: 고령화 사회 진입에 따른 의료 서비스, 건강 관리 앱, 바이오 기술 등의 수요가 증가할 것으로 전망됩니다. 한국 경제는 2024년 2.4%~2.7% 성장이 전망되므로, 이를 고려한 사업 전략 수립이 중요합니다23. 다만, 내수 회복은 제한적일 것으로 예상되며, 민간 부채 리스크에 대한 원활한 대처 여부가 성장흐름을 가를 변수가 될 것입니다. 이러한 분야에서 혁신적인 비즈니스 모델을 개발하고 글로벌 시장을 공략하는 전략을 수립한다면 높은 수익을 창출할 수 있을 것입니다. 특히 인공지능(AI)에 대한 수요 확대에 따른 반도체 수출 증가가 전체 수출실적 개선의 주요 요인이 될 것으로 보입니다."}
            ]
        )



        ai_response = response.choices[0].message.content

        # 응답 전송
        await self.send(text_data=json.dumps({
            'message': ai_response,
            'is_bot': True
        }))
