from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from django.db.models import Q


class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
         try:
           blogs = Post.objects.filter(user = request.user)

           if request.GET.get('search'):
                search = request.GET.get('search')
                blogs - blogs.filter(Q(title = search) | Q(blog_text_iscontains = search))

           serializer = BlogSerializer(blogs, many=True)

           return Response({
                'data': serializer.data,
                'message': 'blog fetched'
            }, status = status.HTTP_201_CREATED)

         except Exception as e:
            return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        try:
            data=request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'blog created'
            }, status = status.HTTP_201_CREATED)

        
        except Exception as e:
            return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
        

    def update(self, request):
        try:
            data=request.data
            blog = Post.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': serializer.errors,
                    'message': 'invalid blog uid'
            }, status = status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message': 'not authorized'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(blog[0], data = data , partial = True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'blog updated'
            }, status = status.HTTP_201_CREATED)


        
        except Exception as e:
            return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            data=request.data
            blog = Post.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data':{},
                    'message': 'invalid blog uid'
            }, status = status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message': 'not authorized'
                }, status = status.HTTP_400_BAD_REQUEST)

            blog[0].delete()

            return Response({
                'data': {},
                'message': 'blog deleted'
            }, status = status.HTTP_201_CREATED)

        
        except Exception as e:
            return Response({
                    'data': {},
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
        

        
