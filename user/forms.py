from django import forms
from .models import Account, ContactUS
from django.utils.translation import gettext

class AccountForm(forms.ModelForm):
  confirm_password = forms.CharField()
  password = forms.CharField()

  class Meta:
    model = Account
    fields = ["first_name", "last_name", "email", "phone_number", "password",]

  def __init__(self, *args, **kwargs):
    super(AccountForm, self).__init__(*args, **kwargs)
    for field_key, field_value in self.fields.items():
      field_value.widget.attrs["class"] = "form-control"
      field_value.required = True
    
  # def clean(self):
  #   cleaned_data = self.cleaned_data
  #   password = cleaned_data["password"]
  #   confirm_password = cleaned_data["confirm_password"]
  #   email = cleaned_data["email"]
    
  #   try:
  #     Account.objects.get(email = email)
  #     self.add_error("email", gettext("This email is already used"))
  #   except Account.DoesNotExist:
  #     pass
  #   if len(password) >= 8 :
  #     if password != confirm_password :
  #       self.add_error("confirm_password", "")
  #       self.add_error("password", gettext("Passwords do not match."))
  #   else:
  #       self.add_error("confirm_password", "")
  #       self.add_error("password", gettext("Password must have at least 8 characters"))
  #   return cleaned_data

class ContactUsForm(forms.ModelForm):
  class Meta:
    model = ContactUS
    fields = "__all__"
  def __init__(self, *args, **kwargs):
    super(ContactUsForm, self).__init__(*args, **kwargs)
    for field_key, field_value in self.fields.items():
      field_value.widget.attrs["class"] = "form-control"
      field_value.required = True