from django import forms 
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['occupation', 'institution', 'birthday', 'bio']
        exclude = ['user',]

    _PROFILE_FIELDS = Meta.fields

    def __init__(self, *args, **kwargs):
        
        initial = {}
        if kwargs.get('initial'):
            for field in self._PROFILE_FIELDS:
                if getattr(kwargs.get('initial'), field):
                    initial[field] = getattr(kwargs.get('initial'), field)
        kwargs['initial'] = initial
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        self.cleaned_data = cleaned_data
        empty_form = True
        for field in self._PROFILE_FIELDS:
            if cleaned_data.get(field):
                empty_form = False
        self.empty_form = empty_form
        if empty_form:
            raise forms.ValidationError("empty form")
    
    def is_valid(self):
        super(ProfileForm, self).is_valid()
        return not self.empty_form
    
    def save(self, user):
        for field in self._PROFILE_FIELDS:
            if self.cleaned_data.get(field):
                profile_object = UserProfile.objects.get(user_id=user.id)
                setattr(profile_object, field, self.cleaned_data.get(field))
                profile_object.save()
    