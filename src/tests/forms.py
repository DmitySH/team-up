from django import forms
from django.utils.translation import gettext_lazy as _


class BelbinPartForm(forms.Form):
    """
    Form with belbin test questions.
    """

    answer0 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer1 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer2 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer3 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=5)
    answer4 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer5 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer6 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=0)
    answer7 = forms.IntegerField(max_value=10, min_value=0, required=True,
                                 initial=5)

    error = ''

    def validate_sum(self):
        if sum(map(int, self.cleaned_data.values())) != 10:
            self.error = 'Неправильно заполнен блок'
            return False
        else:
            self.error = ''
            return True


class MBTIPartForm(forms.Form):
    """
    Form with mbti test questions.
    """

    answer1 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer2 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer3 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer4 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer5 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer6 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))
    answer7 = forms.TypedChoiceField(required=True, initial=1,
                                     coerce=lambda x: int(x))


class LSQPartForm(forms.Form):
    """
    Form with lsq test questions.
    """

    NO_YES_CHOICES = (
        (None, '-----'),
        (0, _('Нет')),
        (1, _('Да')),
    )

    answer1 = forms.TypedChoiceField(required=True, initial=0,
                                     choices=NO_YES_CHOICES,
                                     coerce=lambda x: int(x)
                                     )
    answer2 = forms.TypedChoiceField(required=True, initial=1,
                                     choices=NO_YES_CHOICES,
                                     coerce=lambda x: int(x)

                                     )
    answer3 = forms.TypedChoiceField(required=True, initial=1,
                                     choices=NO_YES_CHOICES,
                                     coerce=lambda x: int(x)
                                     )
    answer4 = forms.TypedChoiceField(required=True, initial=0,
                                     choices=NO_YES_CHOICES,
                                     coerce=lambda x: int(x)
                                     )
