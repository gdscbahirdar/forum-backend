import pandas as pd
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.entities.models.student_models import Student
from apps.entities.models.teacher_models import Teacher
from apps.forum.models import Answer, Question
from apps.forum.models.qa_meta_models import Tag
from apps.resources.models.resource_models import Resource

User = get_user_model()


class AnalyticsViewSet(viewsets.ViewSet):
    def get_student_count(self, request):
        faculty = request.query_params.get("faculty")
        department = request.query_params.get("department")
        year_in_school = request.query_params.get("year")

        students = Student.objects.all()
        if faculty:
            students = students.filter(faculty__name=faculty)
        if department:
            students = students.filter(department__name=department)
        if year_in_school:
            students = students.filter(year_in_school=year_in_school)

        return students.count()

    def get_teacher_count(self, request):
        faculty = request.query_params.get("faculty")
        department = request.query_params.get("department")

        teachers = Teacher.objects.all()
        if faculty:
            teachers = teachers.filter(faculty__name=faculty)
        if department:
            teachers = teachers.filter(departments__name=department)

        return teachers.count()

    @action(detail=False, methods=["get"], url_path="entity_count")
    def get_student_teacher_count(self, request):
        student_count = self.get_student_count(request)
        teacher_count = self.get_teacher_count(request)

        return {"student_count": student_count, "teacher_count": teacher_count}

    @action(detail=False, methods=["get"])
    def stats(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        data = {
            "total_students": Student.objects.count(),
            "total_teachers": Teacher.objects.count(),
            "total_questions": Question.objects.count(),
            "total_answers": Answer.objects.count(),
            "total_resources": Resource.objects.count(),
            "top_users": self.get_top_users(),
            "top_questions": self.get_top_questions(),
            "top_tags": self.get_top_tags(),
            "most_active_faculties": self.get_most_active_faculties(),
            "questions_per_day": self.get_questions_per_day(start_date, end_date),
            "entity": self.get_student_teacher_count(request),
        }
        return Response(data)

    def get_top_users(self):
        users = User.objects.all().order_by("-reputation")[:5]
        return [{"username": user.username, "reputation": user.reputation} for user in users]

    def get_top_questions(self):
        questions = Question.objects.all().order_by("-post__score")[:5]
        return [{"title": question.title, "score": question.post.score} for question in questions]

    def get_top_tags(self, limit=10):
        tags = Tag.objects.annotate(question_count=Count("questions")).order_by("-question_count")[:limit]

        tag_names = []
        tag_counts = []
        for tag in tags:
            if not tag.question_count:
                continue
            tag_names.append(tag.name)
            tag_counts.append(tag.question_count)

        return {"labels": tag_names, "data": tag_counts}

    def get_questions_per_day(self, start_date, end_date):
        from datetime import datetime, timedelta

        from django.db.models import Count
        from django.db.models.functions import TruncDate

        if not end_date:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, "%d-%m-%Y")

        if not start_date:
            start_date = end_date - timedelta(weeks=20)
        else:
            start_date = datetime.strptime(start_date, "%d-%m-%Y")

        questions_per_day = (
            Question.objects.filter(post__created_at__range=[start_date, end_date + timedelta(days=1)])
            .annotate(date=TruncDate("post__created_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        answers_per_day = (
            Answer.objects.filter(post__created_at__range=[start_date, end_date + timedelta(days=1)])
            .annotate(date=TruncDate("post__created_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        dates = []
        question_counts = []
        answer_counts = []

        for entry in questions_per_day:
            dates.append(entry["date"].strftime("%d %b"))
            question_counts.append(entry["count"])

        for entry in answers_per_day:
            answer_counts.append(entry["count"])

        return {
            "series": [
                {
                    "name": "Questions",
                    "data": question_counts,
                },
                {
                    "name": "Answers",
                    "data": answer_counts,
                },
            ],
            "dates": dates,
        }

    def get_most_active_faculties(self):
        faculties = Student.objects.values("faculty__name").annotate(student_count=Count("id"))
        return sorted(faculties, key=lambda x: x["student_count"], reverse=True)

    @action(detail=False, methods=["get"], url_path="export_excel")
    def export_data_as_excel(self, request):
        fields_mapping = {
            "id": "ID",
            "post__user__username": "Created By",
            "created_at": "Creation Date",
            "updated_at": "Last Updated",
            "title": "Title",
            "post__body": "Body",
            "tags__name": "Tags",
            "is_answered": "Is Answered",
            "post__score": "Score",
            "view_count": "View Count",
            "answer_count": "Answer Count",
            "accepted_answer_id": "Accepted Answer ID",
            "is_closed": "Is Closed",
            "post__vote_count": "Vote Count",
        }

        queryset = Question.objects.all().values(*fields_mapping.keys())

        df = pd.DataFrame(list(queryset))

        df.rename(columns=fields_mapping, inplace=True)

        if not df.empty:
            for col in df.select_dtypes(include=["datetime64[ns, UTC]"]).columns:
                df[col] = df[col].dt.tz_localize(None)

            for col in df.select_dtypes(include=["boolean"]).columns:
                df[col] = df[col].astype(bool)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=data.xlsx"

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        response_size = response.tell()
        print(f"Response size: {response_size}")

        return response
