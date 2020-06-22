from django.utils.safestring import mark_safe

from .models import Category, CPU, Product, ProductImage, Manufacturer, RatingStar, Rating, Reviews, Feedback
from multiprocessing import Process, Queue
from django.contrib import admin
from django.core.mail import send_mail
from jinja2 import Template


class EmailReply(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.email_reply_text:
            return
        if not obj.email_address:
            return

        recipients = [
            obj.email_address,
        ]

        if not obj.verified:
            recipients.append(obj.email_address)

        def send_message(queue, num):
            i = 0
            message = Template('Hello \n {{email_reply_text}}\n').render(text=obj.email_reply_text)
            while i < num:
                mail = queue.get()
                send_mail(obj.email_reply_capt, message, 'gapankoff@gmail.com', mail)
                i = i + 1

        def creator(data, queue):
            for item in data:
                queue.put(item)

        if obj.verified:
            q = Queue()
            process_one = Process(target=creator, args=(recipients, q))
            process_one.start()
            send_message(q, recipients.len())
            q.close()
            q.join_thread()
            process_one.join()

        obj.email_reply = False
        obj.email_reply_capt = ''
        obj.email_reply_text = None

        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "cpus")
    search_fields = ("title", "category__name")
    inlines = [ReviewInLine]
    save_on_top = True


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product", "id")


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "get_image")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="30" height = "30"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "product", "ip")


admin.site.register(CPU)

admin.site.register(ProductImage)

admin.site.register(RatingStar)

# Register your models here.
