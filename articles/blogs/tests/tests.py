from django.test import Client, TestCase
from django.urls import reverse_lazy

from .factories import Blogfactory, create_user_writer_with_permission, create_editor_user_with_permission
from ..models import Blog
from ..error_messages import (INVALID_GOOGLE_DOC_URL, INVALID_KEY_IN_GOOGLE_DOC_URL,
                              INVALID_STATUS_WHEN_REASSIGN_BLOG_USER)
from ..utils import get_google_doc_key


class BlogTest(TestCase):

    def setUp(self):

        self.wirter_user = create_user_writer_with_permission()
        self.editor_user = create_editor_user_with_permission()

        self.writer_client = Client()
        self.writer_client.force_login(self.wirter_user)

        self.editor_client = Client()
        self.editor_client.force_login(self.editor_user)

    def test_list_open_blogs(self):

        Blogfactory.create_batch(5, status=Blog.DRAFT, user=None)
        Blogfactory.create_batch(6, status=Blog.IN_REVIEW)
        Blogfactory.create_batch(7, status=Blog.APPROVED)
        Blogfactory.create_batch(8, status=Blog.REJECTED)

        url = reverse_lazy('blogs:list')
        resp1 = self.writer_client.get(url)

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.context.get('blogs').count(), 5)

    def test_list_user_blog(self):
        Blogfactory.create_batch(10)
        Blogfactory.create_batch(15, status=Blog.DRAFT, user=self.wirter_user)
        url = reverse_lazy('blogs:list_user_blog')
        resp1 = self.writer_client.get(url)

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.context.get('blogs').count(), 15)

    def test_assign_blog_to_writer(self):
        Blogfactory.create_batch(10, user=None)
        blog = Blog.objects.first()

        self.assertEqual(blog.user, None)
        url = reverse_lazy('blogs:update_assignee', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url)

        blog.refresh_from_db()
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(blog.user, self.wirter_user)

    def test_save_blog_with_empty_data(self):
        blog = Blogfactory(gdoc_link='https://google.com', user=self.wirter_user)

        url = reverse_lazy('blogs:update', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url)
        self.assertFormError(resp1, 'form', 'gdoc_link', ['This field is required.'])
        self.assertFormError(resp1, 'form', 'content', ['This field is required.'])

    def test_save_blog_with_invalid_google_doc_link(self):
        blog = Blogfactory(gdoc_link='https://google.com', user=self.wirter_user)

        url = reverse_lazy('blogs:update', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url, data=({'gdoc_link': blog.gdoc_link, 'content': 'content'}))
        self.assertFormError(resp1, 'form', 'gdoc_link', [INVALID_GOOGLE_DOC_URL])

    def test_save_blog_with_invalid_google_doc_key(self):
        blog = Blogfactory(gdoc_link='https://docs.google.com/document/d/1NcF8_6ZMraTFoYe8/edit', user=self.wirter_user)

        key = get_google_doc_key(blog.gdoc_link)
        url = reverse_lazy('blogs:update', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url, data=({'gdoc_link': blog.gdoc_link, 'content': 'content'}))
        self.assertFormError(resp1, 'form', 'gdoc_link', [INVALID_KEY_IN_GOOGLE_DOC_URL.format(len(key))])

    def test_save_blog_valid_data(self):
        gdoc_link = 'https://docs.google.com/document/d/1NcF8_6ZMraTXp7H7DVzR6pbqzJgNIyg3gYLUUoFoYe8/edit'
        blog = Blogfactory(gdoc_link=None, content='', user=self.wirter_user, status=Blog.DRAFT)

        self.assertEqual(blog.gdoc_link, None)
        self.assertEqual(blog.content, '')

        url = reverse_lazy('blogs:update', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url, data=({'gdoc_link': gdoc_link, 'content': 'content'}))

        blog.refresh_from_db()
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(blog.gdoc_link, gdoc_link)
        self.assertEqual(blog.content, 'content')
        self.assertEqual(blog.status, Blog.DRAFT)

    def test_submit_blog_content(self):
        gdoc_link = 'https://docs.google.com/document/d/1NcF8_6ZMraTXp7H7DVzR6pbqzJgNIyg3gYLUUoFoYe8/edit'
        blog = Blogfactory(gdoc_link=None, content='', user=self.wirter_user, status=Blog.DRAFT)

        self.assertEqual(blog.gdoc_link, None)
        self.assertEqual(blog.content, '')

        url = reverse_lazy('blogs:update', kwargs={'pk': blog.pk})
        resp1 = self.writer_client.post(url, data=({'gdoc_link': gdoc_link, 'content': 'content', "review": ""}))

        blog.refresh_from_db()
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(blog.gdoc_link, gdoc_link)
        self.assertEqual(blog.content, 'content')
        self.assertEqual(blog.status, Blog.IN_REVIEW)

    def test_list_in_review_blogs(self):

        Blogfactory.create_batch(5, status=Blog.DRAFT, user=None)
        Blogfactory.create_batch(6, status=Blog.IN_REVIEW)
        Blogfactory.create_batch(7, status=Blog.APPROVED)
        Blogfactory.create_batch(8, status=Blog.REJECTED)

        url = reverse_lazy('blogs:need_approval')
        resp1 = self.editor_client.get(url)

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.context.get('blogs').count(), 6)

    def test_approve_blog(self):
        blog = Blogfactory(status=Blog.IN_REVIEW, user=self.editor_user)

        self.assertEqual(blog.status, Blog.IN_REVIEW)

        url = reverse_lazy('blogs:approval_action', kwargs={'pk': blog.pk})
        resp = self.editor_client.post(url, data=({'status': Blog.APPROVED}))
        blog.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(blog.status, Blog.APPROVED)

    def test_reject_blog(self):
        blog = Blogfactory(status=Blog.IN_REVIEW, user=self.editor_user)

        self.assertEqual(blog.status, Blog.IN_REVIEW)

        url = reverse_lazy('blogs:approval_action', kwargs={'pk': blog.pk})
        resp = self.editor_client.post(url, data=({'status': Blog.REJECTED}))
        blog.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(blog.status, Blog.REJECTED)

    def test_list_approved_blog(self):
        Blogfactory.create_batch(5, status=Blog.DRAFT, user=None)
        Blogfactory.create_batch(6, status=Blog.IN_REVIEW)
        Blogfactory.create_batch(7, status=Blog.APPROVED)
        Blogfactory.create_batch(8, status=Blog.REJECTED)

        url = reverse_lazy('blogs:approved')
        resp1 = self.editor_client.get(url)

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.context.get('blogs').count(), 7)

    def test_list_blog_to_reassign_user(self):
        Blogfactory.create_batch(5, status=Blog.DRAFT)
        Blogfactory.create_batch(6, status=Blog.IN_REVIEW)
        Blogfactory.create_batch(7, status=Blog.APPROVED)
        Blogfactory.create_batch(8, status=Blog.REJECTED)

        url = reverse_lazy('blogs:list_to_reassign')
        resp1 = self.editor_client.get(url)

        self.assertEqual(resp1.status_code, 200)
        # list all draft and reject blogs only
        self.assertEqual(resp1.context.get('blogs').count(), 13)

    def test_reassign_blog_from_writer_to_another_writer_witn_invalid_status(self):
        in_review_blog = Blogfactory(status=Blog.IN_REVIEW)
        approved_blog = Blogfactory(status=Blog.APPROVED)

        url = reverse_lazy('blogs:reassign_user', kwargs={'pk': in_review_blog.pk})
        resp = self.editor_client.post(url, data=({'user': self.wirter_user.pk}))
        self.assertFormError(resp, 'form', None, [INVALID_STATUS_WHEN_REASSIGN_BLOG_USER])

        url2 = reverse_lazy('blogs:reassign_user', kwargs={'pk': approved_blog.pk})
        resp2 = self.editor_client.post(url2, data=({'user': self.wirter_user.pk}))
        self.assertFormError(resp2, 'form', None, [INVALID_STATUS_WHEN_REASSIGN_BLOG_USER])

    def test_reassign_blog_from_writer_to_another_writer_witn_draft_status(self):
        draft_blog = Blogfactory(status=Blog.DRAFT)

        self.assertNotEqual(draft_blog.user, self.wirter_user)
        url = reverse_lazy('blogs:reassign_user', kwargs={'pk': draft_blog.pk})
        resp = self.editor_client.post(url, data=({'user': self.wirter_user.pk}))
        draft_blog.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(draft_blog.user, self.wirter_user)

    def test_reassign_blog_from_writer_to_another_writer_witn_reject_status(self):
        reject_blog = Blogfactory(status=Blog.REJECTED)

        self.assertNotEqual(reject_blog.user, self.wirter_user)
        url1 = reverse_lazy('blogs:reassign_user', kwargs={'pk': reject_blog.pk})
        resp1 = self.editor_client.post(url1, data=({'user': self.wirter_user.pk}))
        reject_blog.refresh_from_db()
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(reject_blog.user, self.wirter_user)
