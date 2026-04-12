# apps/ai/views.py

import os
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


class AskAIView(APIView):
    def post(self, request):
        question = request.data.get("question")

        # ✅ Validate input
        if not question:
            return Response(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        client = get_openai_client()

        # ✅ Check API key
        if client is None:
            return Response(
                {"error": "OpenAI API key not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        prompt = f"""
You are an AI assistant for Irfan's portfolio.

Answer based on:
- He is a developer
- Works with Django, Next.js, AI
- Builds real-world systems

Question: {question}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content

        except Exception:
            return Response(
                {"error": "AI service temporarily unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response({"answer": answer})