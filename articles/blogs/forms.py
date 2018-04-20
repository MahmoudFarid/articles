from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Blog
from .error_messages import (INVALID_GOOGLE_DOC_URL, INVALID_KEY_IN_GOOGLE_DOC_URL,
                             INVALID_STATUS_WHEN_REASSIGN_BLOG_USER)
from .utils import get_google_doc_key


class UpdateBlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=True)

    class Meta:
        model = Blog
        fields = ('content', 'gdoc_link',)

    def clean_gdoc_link(self):
        # https://docs.google.com/document/d/1NcF8_6ZMraTXp7H7DVzR6pbqzJgNIyg3gYLUUoFoYe8/edit
        gdoc_link = self.cleaned_data.get('gdoc_link')

        if 'docs.google.com/document/d/' not in gdoc_link:
            raise forms.ValidationError(INVALID_GOOGLE_DOC_URL)

        key = get_google_doc_key(gdoc_link)
        if len(key) != 44:
            raise forms.ValidationError(INVALID_KEY_IN_GOOGLE_DOC_URL.format(len(key)))

        return gdoc_link


class BlogApprovalForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('status',)


class ReassignBlogUserForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('user',)

    def clean(self):
        if self.instance.status == Blog.APPROVED or self.instance.status == Blog.IN_REVIEW:
            raise forms.ValidationError(INVALID_STATUS_WHEN_REASSIGN_BLOG_USER)
