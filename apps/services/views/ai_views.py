from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from transformers import pipeline

chatbot = None

if settings.USE_AI_MODELS:
    chatbot = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")


class GenerateTextView(APIView):
    def post(self, request):
        try:
            if not settings.USE_AI_MODELS:
                return Response({"generated_text": "dummy response"}, status=status.HTTP_200_OK)

            option = request.data.get("option")
            input_text = request.data.get("text")

            if not option:
                return Response({"error": "No option provided"}, status=status.HTTP_400_BAD_REQUEST)

            if not input_text:
                return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

            prompt_templates = {
                "improve": "Improve this text: {}",
                "fix": "Fix the grammar of this text: {}",
                "shorter": "Make this text shorter: {}",
                "longer": "Make this text longer: {}",
                "continue": "Continue writing from this text: {}",
            }

            prompt_template = prompt_templates.get(option)

            if not prompt_template:
                return Response({"error": "Invalid option provided"}, status=status.HTTP_400_BAD_REQUEST)

            prompt = prompt_template.format(input_text)

            messages = [
                {"role": "system", "content": "You are an AI assistant that helps in writing text."},
                {"role": "user", "content": prompt},
            ]

            response = chatbot(messages)

            generated_text = response[0]["generated_text"]

            return Response({"generated_text": generated_text}, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"error": "Something went wrong. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
