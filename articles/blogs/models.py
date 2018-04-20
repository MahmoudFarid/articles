from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ckeditor.fields import RichTextField


class Blog(TimeStampedModel):
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (IN_REVIEW, _('In-Review')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs', null=True, blank=True,
                             on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=128)
    description = models.TextField(_('Description'))
    content = RichTextField()
    gdoc_link = models.URLField(_('Google Doc Link'), null=True)
    status = models.CharField(('Status'), choices=STATUS_CHOICES, default=DRAFT, max_length=15)

    def __str__(self):
        return self.title
