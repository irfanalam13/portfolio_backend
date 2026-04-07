import os
from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

class AskAIView(APIView):
    def post(self, request):
        question = request.data.get("question")

        client = get_openai_client()

        # ✅ Safety check
        if client is None:
            return Response({
                "error": "OpenAI API key not configured"
            }, status=500)

        prompt = f"""
        You are an AI assistant for Irfan's portfolio.

        Answer based on:
        - He is a developer
        - Works with Django, Next.js, AI
        - Builds real-world systems

        Question: {question}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return Response({
            "answer": response.choices[0].message.content
        })