from django import forms

class GetQueryForm(forms.Form):
    query_date = forms.DateTimeField(label='dateTime')