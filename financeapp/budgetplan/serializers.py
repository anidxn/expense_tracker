from rest_framework import serializers
from . models import Category,Activity

#company model serializer
class CatSerializer(serializers.HyperlinkedModelSerializer):
    cat_id=serializers.ReadOnlyField()#display read only fields

    class Meta:
        model=Category
        fields="__all__"#serialize all fields of company models
        #('name','location','active') serialise only these 3 fields
        
# ===============================================================
#   In this Serializer Category is treated as a link (URL)
# ===============================================================
class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    ac_id=serializers.ReadOnlyField()#display read only fields
    
    class Meta:
        model=Activity
        fields="__all__" # serialize all fields of company models
        #('name','location','active') serialise only these 3 fields

# ==============================================================================
#   In this Serializer Category is treated as a nested object for easier Read
# ==============================================================================
class ActivityCategoryLinkSerializer(serializers.HyperlinkedModelSerializer):
    ac_id=serializers.ReadOnlyField()#display read only fields
    # * * * * * * * * * * * *
    a_cat = CatSerializer()  # Use a nested serializer to include the related category data (FKEY linked model)

    class Meta:
        model=Activity
        fields="__all__"