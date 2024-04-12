from django import template
from ..models import Post, Comment

register = template.Library()

@register.inclusion_tag('likes.html')
def likes(request, value, object):
    if object == 'post':
        post = Post.objects.get(slug=value)
    else:
        post = Comment.objects.get(pk=value)
    user = request.user

    if 'like' in request.GET:
        if user not in post.likes.all():
            post.likes.add(user)
            post.dislikes.remove(user)
        elif user in post.likes.all():
            post.likes.remove(user)
    elif 'dislike' in request.GET: #
        if user not in post.dislikes.all():
            post.dislikes.add(user)
            post.likes.remove(user)
        elif user in post.dislikes.all():
            post.dislikes.remove(user)

    return {'post': post, 'user': user}
