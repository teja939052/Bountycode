"""Discussion routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.database import get_session
from sqlalchemy import select
from app.models.community import DiscussionPost, DiscussionReply
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/discussions", tags=["discussions"])


@router.post("/{question_id}")
async def create_discussion(
    question_id: str,
    content: str,
    code: Optional[str] = None,
    language: Optional[str] = None,
    discussion_type: str = "solution",
    user=Depends(get_current_user),
):
    async with get_session() as session:
        post = DiscussionPost(
            question_id=question_id,
            user_id=user["id"],
            user_name=user.get("name", "Anonymous"),
            content=content,
            code=code,
            language=language,
            discussion_type=discussion_type,
            upvotes=0,
            downvotes=0,
            replies=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return {
            "id": str(post.id),
            "question_id": post.question_id,
            "user_id": post.user_id,
            "user_name": post.user_name,
            "content": post.content,
            "code": post.code,
            "language": post.language,
            "discussion_type": post.discussion_type,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "replies": post.replies,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat(),
        }


@router.get("/{question_id}")
async def get_discussions(
    question_id: str,
    sort: str = "best",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    async with get_session() as session:
        if sort == "best":
            order_by = DiscussionPost.upvotes.desc(), DiscussionPost.created_at.desc()
        elif sort == "newest":
            order_by = DiscussionPost.created_at.desc()
        else:
            order_by = DiscussionPost.created_at.asc()
        skip = (page - 1) * limit
        query = select(DiscussionPost).where(DiscussionPost.question_id == question_id).order_by(*order_by)
        result = await session.execute(query.offset(skip).limit(limit))
        posts = result.scalars().all()
        count_result = await session.execute(select(func.count()).select_from(DiscussionPost).where(DiscussionPost.question_id == question_id))
        total = count_result.scalar_one()
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": str(post.id),
            "question_id": post.question_id,
            "user_id": post.user_id,
            "user_name": post.user_name,
            "content": post.content,
            "code": post.code,
            "language": post.language,
            "discussion_type": post.discussion_type,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "replies": post.replies,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat(),
        })
    return {
        "discussions": posts_data,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }