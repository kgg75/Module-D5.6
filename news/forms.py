from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    MY_CHOICES = (
        ('0', 'Политика'),
        ('1', 'Культура'),
        ('2', 'Авто'),
        ('3', 'Спорт'),
    )
    #post_category = forms.CharField(min_length=2, max_length=32)
    post_category = forms.ChoiceField(choices=MY_CHOICES)
    #post_category = forms.ChoiceField(choices=Post.postCategory.name)
    title = forms.CharField(max_length=128)
    text = forms.Textarea() # .CharField()    #min_length=10)

    class Meta:
        model = Post
        fields = [
            #'datetime',
            'post_category',
            'title',
            'text',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # print("cleaned_data.get(post_category) = ", cleaned_data.get("post_category"))
    #     post_category = self.MY_CHOICES[int(cleaned_data.get("post_category"))][1]
    #     title = cleaned_data.get("title")
    #     text = cleaned_data.get("text")
    #     print("post_category = ", post_category)
    #     print("title = ", title)
    #     print("text = ", text)
    #
    #     # if name == description:
    #     #     raise ValidationError(
    #     #         "Описание не должно быть идентично названию."
    #     #     )
    #
    #     return cleaned_data