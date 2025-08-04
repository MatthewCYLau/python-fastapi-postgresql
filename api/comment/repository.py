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
