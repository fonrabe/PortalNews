from django import forms
from news.models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'text',
            'postCategory',
            'author'
        ]
        # widgets ={
        #     'title':forms.TextInput(),
        #     'text' : forms.Textarea(),
        #     'postCategory' : forms.Select()
        # }