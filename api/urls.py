from api.views.comments_view import CommentsView

urlpatterns = [] + CommentsView.routes(prefix='/api/v1', path='comments')
