from django import forms

import class_room.models as m


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(
        help_text='To this email will be send user`s password.'
    )

    class Meta:
        model = m.User
        exclude = ('id', )
