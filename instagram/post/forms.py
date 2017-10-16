from django import forms

from .models import Post, PostComment


class PostForm(forms.Form):
    photo = forms.ImageField(required=True)
    # Text를 받을 수 있는 field 추가
    text = forms.CharField(max_length=5)

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('All text must be uppercase!')
        return data

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
