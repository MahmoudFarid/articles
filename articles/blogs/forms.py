from django import forms
from django.utils.translation import ugettext_lazy as _

from ckeditor.widgets import CKEditorWidget

from .models import Blog


class UpdateBlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=True)

    class Meta:
        model = Blog
        fields = ('content', 'gdoc_link',)

    def clean_gdoc_link(self):
        # https://docs.google.com/document/d/1NcF8_6ZMraTXp7H7DVzR6pbqzJgNIyg3gYLUUoFoYe8/edit
        gdoc_link = self.cleaned_data.get('gdoc_link')

        if 'docs.google.com/document/d/' not in gdoc_link:
            raise forms.ValidationError(_('It should be Google Doc URL!'))

        key = gdoc_link.split('/d/')[1].split('/')[0]
        if len(key) != 44:
            raise forms.ValidationError(_("The key should be 44 as a length, it's only {}!".format(len(key))))

        return gdoc_link


class BlogApprovalForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('status',)


class ReassignBlogUserForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('user',)
