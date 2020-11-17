from views.comments_view import CommentsView

urlpatterns = [] + CommentsView.routes(path='/comments/')
