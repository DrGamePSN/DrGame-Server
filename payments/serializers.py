# class CourseOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseOrder
#         fields = ['id', 'course', 'payment_status', 'price', 'created_at', 'updated_at', ]
#         read_only_fields = ['payment_status', 'user']
#
#
# class CourseOrderForAdminSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='user.phone')
#
#     class Meta:
#         model = CourseOrder
#         fields = ['id', 'user', 'course', 'payment_status', 'price', 'created_at', 'updated_at', ]
#         read_only_fields = ['payment_status', 'user']
#
#
# class CourseOrderCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseOrder
#         fields = ['course']
#
#     def validate(self, data):
#         course = data['course']
#         if CourseOrder.objects.get(course=course):
#             raise serializers.ValidationError('You have already bought this course!')
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user_id = request.user.id
#         course = validated_data.get('course')
#         return CourseOrder.objects.create(user_id=user_id,
#                                           price=course.price,
#                                           **validated_data)
#
#
# class CourseOrderUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseOrder
#         fields = ['payment_status']
