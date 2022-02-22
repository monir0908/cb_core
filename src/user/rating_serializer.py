from typing import Dict

from base.serializers import BaseModelSerializer, ReadWriteSerializerMethodField
from user.models import RatingReview
from user.serializers import UserSerializer


class RatingReviewSerializer(BaseModelSerializer):
    given_to = ReadWriteSerializerMethodField()

    class Meta:
        model = RatingReview
        fields = '__all__'

    def get_given_to(self, instance: RatingReview) -> Dict:
        return UserSerializer(instance.given_to).data
