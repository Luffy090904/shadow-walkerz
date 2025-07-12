from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Add comma-separated tags (e.g. Python, APIs)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
        widgets = {
            'description': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['description']
        widgets = {
            'description': forms.HiddenInput()
        }
