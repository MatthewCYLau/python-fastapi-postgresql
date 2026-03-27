import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.comment.repository import CommentRepository
from api.comment.schemas import CommentBase, CommentResponse
from api.comment.service import CommentService
from api.config.logging import get_logger
from api.config.database import get_session

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/comments", tags=["comments"])


def get_comment_service(session: Session = Depends(get_session)) -> CommentService:
    repository = CommentRepository(session)
    return CommentService(repository)


@router.get("/", response_model=list[CommentResponse | CommentBase])
def get_all_products(
    service: CommentService = Depends(get_comment_service),
    groupByProductId: str = None,
) -> list[CommentResponse | CommentBase]:
    """Get all comments."""
    logger.debug("Fetching all comments")
    try:

        if groupByProductId:
            res = service.get_comments_group_by_order_id(groupByProductId)
            return res

        commments = service.get_all_comments()
        logger.info(f"Retrieved {len(commments)} commments")
        return commments
    except Exception as e:
        logger.error(f"Failed to fetch commments: {str(e)}")
        raise


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentBase, service: CommentService = Depends(get_comment_service)
):
    """Register a new comment."""
    logger.info(f"Registering comment for product ID {comment_data.product_id}")
    return service.create_comment(comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: uuid.UUID,
    service: CommentService = Depends(get_comment_service),
):
    logger.info(f"Deleting comment: {comment_id}")
    service.delete_comment_by_id(comment_id)
