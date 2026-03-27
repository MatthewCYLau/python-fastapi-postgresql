from api.comment.models import Comment
from api.comment.repository import CommentRepository
from api.comment.schemas import CommentBase, CommentResponse


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create_comment(self, comment_data: CommentBase) -> Comment:
        return self.repository.create(comment_data)

    def get_all_comments(
        self,
    ) -> list[CommentResponse]:
        products = self.repository.get_all()
        return [CommentResponse.model_validate(product) for product in products]

    def delete_comment_by_id(self, comment_id: str) -> None:
        self.repository.delete_comment_by_id(comment_id)
