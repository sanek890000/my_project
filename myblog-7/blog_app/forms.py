from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'tags', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        return [tag.strip() for tag in tags.split(',')]

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if not instance.pk:
            instance.author = self.initial['author']

        if commit:
            instance.save()
            self.save_tags(instance)
        return instance

    def save_tags(self, instance):
        tags = self.cleaned_data['tags']
        instance.tags.set(*[Tag.objects.get_or_create(name=tag)[0] for tag in tags])