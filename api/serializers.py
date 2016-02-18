
from rest_framework import serializers
# from rest_framework.reverse import reverse
from claim.models import Claim, Organization, ClaimType


class ClaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = ('text', 'created', 'live', 'organization',
                  'servant', 'complainer', 'claim_type',
                  )


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type', 'total_claims')


class ClaimTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimType
        fields = ('id', 'name', 'org_type', 'icon')
