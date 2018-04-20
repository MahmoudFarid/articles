from django.views.generic import ListView, View, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

from .models import Blog
from .forms import UpdateBlogForm, BlogApprovalForm, ReassignBlogUserForm


class ListBlogView(PermissionRequiredMixin, ListView):
    permission_required = 'users.can_write_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(user__isnull=True)


class ListUserBlogView(PermissionRequiredMixin, ListView):
    permission_required = 'users.can_write_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/list_user_blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UpdateAssigneeBlog(PermissionRequiredMixin, View):
    permission_required = 'users.can_write_blogs'
    raise_exception = True

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog.user = self.request.user
        blog.save()
        return HttpResponseRedirect(reverse_lazy('blogs:list'))


class UpdateBlogView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.can_write_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/update.html'
    form_class = UpdateBlogForm
    context_object_name = 'blog'
    success_url = reverse_lazy('blogs:list_user_blog')

    def form_valid(self, form):
        if 'review' in form.data:
            blog = form.save(commit=False)
            blog.status = Blog.IN_REVIEW
        return super(UpdateBlogView, self).form_valid(form)


class BlogDetailsView(DetailView):
    model = Blog
    template_name = 'blogs/details.html'


class ListBlogWithActionRequire(PermissionRequiredMixin, ListView):
    permission_required = 'users.can_review_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/need_approval.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(status=Blog.IN_REVIEW)


class BlogApprovalView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.can_review_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/update.html'
    form_class = BlogApprovalForm
    context_object_name = 'blog'
    success_url = reverse_lazy('blogs:approved')


class ListApprovedBlogs(ListView):
    model = Blog
    template_name = 'blogs/approved.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(status=Blog.APPROVED)


class ListBlogToReassign(PermissionRequiredMixin, ListView):
    permission_required = 'users.can_review_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/list_to_reassign.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return self.model.objects.filter(user__isnull=False).filter(Q(status=Blog.DRAFT) | Q(status=Blog.REJECTED))


class ReassignBlogUserView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.can_review_blogs'
    raise_exception = True

    model = Blog
    template_name = 'blogs/reassign_user.html'
    form_class = ReassignBlogUserForm
    context_object_name = 'blog'
    success_url = reverse_lazy('blogs:approved')
