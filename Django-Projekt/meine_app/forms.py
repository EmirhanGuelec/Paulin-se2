from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Was möchtest du schreiben?',
                'rows': 4,
            }
        ),
        required=False,  # Validierung im clean()
    )

    class Meta:
        model = Post
        fields = ['content', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content', '').strip()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if not content and not image and not video:
            raise forms.ValidationError(
                "Du musst entweder Text eingeben oder ein Bild/Video hochladen."
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Dein Kommentar...',
                'rows': 2,
            }
        ),
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']

class ProfileForm(forms.Form):
    avatar = forms.ImageField(
        label="Profilbild",
        required=False
    )
    bio = forms.CharField(
        label="Biografie",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Erzähl etwas über dich…'}),
        required=False
    )
    location = forms.CharField(
        label="Ort",
        max_length=100,
        required=False
    )


