from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions import IsAdminOrIfAuthenticatedReadOnly
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follows")
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Retrieve the profiles with filters"""
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        phone = self.request.query_params.get("phone")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter by first_name (ex. ?first_name=john)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter by last_name (ex. ?first_name=doe)",
            ),
            OpenApiParameter(
                "phone",
                type=OpenApiTypes.STR,
                description="Filter by phone (ex. ?phone=140302)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreateProfileViewSet(generics.CreateAPIView):
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyProfileViewSet(
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class FollowViewSet(viewsets.ViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)

    def follow_list(self, request):
        queryset = request.user.profile.follows
        serializer = ProfileSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def followed_by_list(self, request):
        queryset = Profile.objects.filter(follows__pk=request.user.profile.pk)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def follow(self, request, pk):
        own_profile = request.user.profile
        following_profile = Profile.objects.get(id=pk)
        own_profile.follows.add(following_profile)

        return Response(
            {
                f"message": f"now you are following "
                            f"{following_profile.first_name} {following_profile.last_name}"
            },
            status=status.HTTP_200_OK,
        )

    def unfollow(self, request, pk):
        own_profile = request.user.profile
        following_profile = Profile.objects.get(id=pk)
        own_profile.follows.remove(following_profile)

        return Response(
            {
                f"message": f"now you are not following "
                            f"{following_profile.first_name} {following_profile.last_name}"
            },
            status=status.HTTP_200_OK,
        )
