from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (ListBlogView, UpdateAssigneeBlog, ListUserBlogView, UpdateBlogView, BlogDetailsView,
                    ListBlogWithActionRequire, BlogApprovalView, ListApprovedBlogs, ListBlogToReassign,
                    ReassignBlogUserView)


urlpatterns = [
    path('list/', login_required(ListBlogView.as_view()), name='list'),
    path('list_user_blog/', login_required(ListUserBlogView.as_view()), name='list_user_blog'),
    path('update_assignee/<int:pk>', login_required(UpdateAssigneeBlog.as_view()), name='update_assignee'),
    path('update/<int:pk>', login_required(UpdateBlogView.as_view()), name='update'),
    path('details/<int:pk>', BlogDetailsView.as_view(), name='details'),
    path('need_approval', login_required(ListBlogWithActionRequire.as_view()), name='need_approval'),
    path('approval_action/<int:pk>', login_required(BlogApprovalView.as_view()), name='approval_action'),
    path('approved/', ListApprovedBlogs.as_view(), name='approved'),
    path('list_to_reassign/', login_required(ListBlogToReassign.as_view()), name='list_to_reassign'),
    path('<int:pk>/reassign_user/', login_required(ReassignBlogUserView.as_view()), name='reassign_user'),
]
