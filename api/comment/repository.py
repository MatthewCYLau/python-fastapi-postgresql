from sqlalchemy import delete
from api.config.exception import NotFoundException
from api.config.logging import get_logger
from api.comment.models import Comment

logger = get_logger(__name__)


class CommentRepository:
    """Repository for handling comment database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, comment_data) -> Comment:

        comment = Comment(product_id=comment_data.product_id, body=comment_data.body)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

        logger.info(f"Created comment.")
        return comment

    def delete_comment_by_id(self, comment_id: str) -> None:

        query = delete(Comment).where(Comment.id == comment_id)
        result = self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Comment with id {comment_id} not found")

        self.session.commit()
        logger.info(f"Deleted comment with id {comment_id}")
