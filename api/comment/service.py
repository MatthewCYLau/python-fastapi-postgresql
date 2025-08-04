from api.comment.models import Comment
from api.comment.repository import CommentRepository
from api.comment.schemas import CommentBase


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create_comment(self, comment_data: CommentBase) -> Comment:
        return self.repository.create(comment_data)
