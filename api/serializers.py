from rest_framework import serializers
from .models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model"""
    class Meta:
        model = Member
        fields = ['id', 'username', 'display_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6, max_length=128)
    
    class Meta:
        model = Member
        fields = ['username', 'display_name', 'password']
    
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        return value
    
    def validate_display_name(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Display name is required")
        return value
    
    def create(self, validated_data):
        member = Member(
            username=validated_data['username'],
            display_name=validated_data['display_name']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    author = MemberSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
    
    def validate_text(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Message text cannot be empty")
        return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = Member
        fields = ['display_name']
    
    def validate_display_name(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Display name cannot be empty")
        return value
