from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.comment.repository import CommentRepository
from api.comment.schemas import CommentBase
from api.comment.service import CommentService
from api.config.logging import get_logger
from api.config.database import get_session

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/comments", tags=["comments"])


def get_comment_service(session: Session = Depends(get_session)) -> CommentService:
    repository = CommentRepository(session)
    return CommentService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentBase, service: CommentService = Depends(get_comment_service)
):
    """Register a new comment."""
    logger.info(f"Registering comment for product ID {comment_data.product_id}")
    return service.create_comment(comment_data)
