from celery import shared_task
from django.utils import timezone
from .models import Post

@shared_task
def schedule_post_publication(post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.status == 'scheduled' and post.scheduled_date <= timezone.now():
            post.status = 'published'
            post.published_date = post.scheduled_date
            post.save()
            return f"Successfully published post: {post.title}"
    except Post.DoesNotExist:
        return f"Post with id {post_id} not found"
    except Exception as e:
        return f"Error publishing post: {str(e)}"

@shared_task
def clean_old_draft_posts():
    """
    Delete draft posts older than 30 days
    """
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    old_drafts = Post.objects.filter(
        status='draft',
        created_at__lt=thirty_days_ago
    )
    count = old_drafts.count()
    old_drafts.delete()
    return f"Deleted {count} old draft posts"