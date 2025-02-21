from django import forms

from home.models import Message


class ContactForm(forms.Form):
    name = forms.CharField(max_length=10, label='Your Name')
    text = forms.CharField(max_length=10, label='Your Message')

    def clean(self):
        name = self.cleaned_data.get('name')
        text = self.cleaned_data.get('text')

        if name == text:
            raise forms.ValidationError('name and text are same', code='name_text_same')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if 'a' in name:
            raise forms.ValidationError('a can not be in name', code='a_in_name')
        return name


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your Message'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }