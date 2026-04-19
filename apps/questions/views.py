from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.question_service import QuestionService


class GenerateQuestionsView(APIView):

    def post(self, request):
        try:
            document_id = request.data.get("document_id")
            num_questions = request.data.get("num_questions")
            difficulty = request.data.get("difficulty")
            topic = request.data.get("topic")

            result = QuestionService.generate_questions(
                document_id,
                num_questions,
                difficulty,
                topic
            )

            return Response({"questions": result})

        except Exception as e:
            return Response({"error": str(e)}, status=400)