from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Name:", max_length=100, help_text="100 car. max." , 
                                error_messages={"Required":"El nombre es obligatorio"},
                                widget=forms.Textarea(attrs={"class":"text-gray-400","rows":3,"cols":60}))
    