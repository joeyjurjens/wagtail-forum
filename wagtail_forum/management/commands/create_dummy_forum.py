from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from wagtail.models import Page, Site

from faker import Faker
from wagtail_forum.basic.models import (
    ForumIndex,
    ForumCategory,
    ForumTopic,
    ForumTopicReply,
)
from pickle import OBJ


class Command(BaseCommand):
    help = "Creates a dummy forum with users, categories, topics, and replies"

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()

        root_page = Page.objects.filter(depth=1).first()

        # Delete any existing pages
        ForumIndex.objects.all().delete()

        # Create new ForumIndex as site root
        forum_index = ForumIndex(title="Community Forum")
        root_page.add_child(instance=forum_index)

        Site.objects.update(root_page=forum_index)

        # Create users
        users = []
        for username in ["johndoe", "janedoe", "techguy", "forumqueen", "supportninja"]:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": f"{username}@example.com"}
            )
            if created:
                user.set_password("testpassword")
                user.save()
            users.append(user)

        # Create categories and subcategories
        for category_title, subcategories in [
            (
                "Programming",
                [
                    ("Python", "Python programming discussions"),
                    ("JavaScript", "Web and frontend development"),
                    ("Django", "Web framework discussions"),
                ],
            ),
            (
                "Community",
                [
                    ("General Discussion", "Off-topic conversations"),
                    ("Introductions", "Welcome new members"),
                ],
            ),
        ]:
            category = ForumCategory(
                title=category_title, slug=category_title.lower().replace(" ", "-")
            )
            forum_index.add_child(instance=category)
            for subcategory_title, subcategory_description in subcategories:
                subcategory = ForumCategory(
                    title=subcategory_title,
                    slug=subcategory_title.lower().replace(" ", "-"),
                    description=subcategory_description,
                )
                category.add_child(instance=subcategory)

        # Create topics and replies, topics can only be created on categories that have no subcategories anymore.
        for category in ForumCategory.objects.child_of(forum_index).filter(numchild=0):
            for _ in range(3):
                topic = ForumTopic(
                    title=fake.sentence(nb_words=6),
                    slug=fake.slug(),
                    content=fake.paragraph(),
                    created_by=users[_ % len(users)],
                    is_sticky=fake.boolean(chance_of_getting_true=20),
                )
                category.add_child(instance=topic)
                for __ in range(5):
                    reply = ForumTopicReply(
                        content=fake.paragraph(),
                        created_by=users[__ % len(users)],
                        topic=topic,
                    )
                    reply.save()

        self.stdout.write(self.style.SUCCESS("Successfully created dummy forum"))
