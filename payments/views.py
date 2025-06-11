from django.shortcuts import render

# Course Order

# class CourseOrderListAPIView(generics.ListAPIView):
#
#     def get_serializer_class(self):
#         if self.request.user.is_staff:
#             return CourseOrderForAdminSerializer
#         return CourseOrderSerializer
#
#     def get_queryset(self):
#         return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
#

# class CourseOrderRetrieveAPIView(generics.RetrieveAPIView):
#
#     def get_serializer_class(self):
#         if self.request.user.is_staff:
#             return CourseOrderForAdminSerializer
#         return CourseOrderSerializer
#
#     def get_queryset(self):
#         return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
#
#
# class CourseOrderCreateAPIView(generics.CreateAPIView):
#     serializer_class = CourseOrderCreateSerializer
#
#     def get_queryset(self):
#         return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
#
#
# class CourseOrderUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = CourseOrderUpdateSerializer
#
#     def get_queryset(self):
#         return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
#
#
# class CourseOrderDeleteAPIView(generics.DestroyAPIView):
#     serializer_class = CourseOrderSerializer
#
#     def get_queryset(self):
#         return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
