from django.contrib import admin
from omg_app.models import User, Posting, AIModel, Message, ChatRoom, Data, Payment, SubscriptionProduct

admin.site.register(User)


admin.site.register(Posting)


admin.site.register(AIModel)


admin.site.register(Message)


admin.site.register(ChatRoom)


admin.site.register(Data)


admin.site.register(Payment)

admin.site.register(SubscriptionProduct)