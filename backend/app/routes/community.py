"""Community features — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/community", tags=["community"])


@router.get("/feed")
async def get_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    async with get_session() as session:
        # Query community posts from PostgreSQL
        result = await session.execute(
            select(
                CommunityPost.id,
                CommunityPost.user_id,
                CommunityPost.content,
                CommunityPost.type,
                CommunityPost.code,
                CommunityPost.language,
                CommunityPost.created_at,
            ).order_by(CommunityPost.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        posts = result.fetchall()

        # Get total count
        count_result = await session.execute(select(func.count()).select_from(CommunityPost))
        total = count_result.scalar()

    output = []
    for row in posts:
        output.append({
            "id": row[0],
            "user_id": row[1],
            "content": row[2],
            "type": row[3],
            "code": row[4],
            "language": row[5],
            "likes": 0,
            "liked_by": [],
            "comments": [],
            "created_at": row[6].isoformat() if row[6] else "",
        })

    return {
        "posts": output,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("/post")
async def create_post(
    content: str,
    type: str = "post",
    code: Optional[str] = None,
    language: Optional[str] = None,
    user=Depends(get_current_user),
):
    async with get_session() as session:
        post_id = str(user["id"]) + "-" + str(datetime.now().timestamp())
        # Insert community post
        await session.execute(
            """INSERT INTO community_posts (id, user_id, content, type, code, language, created_at)
               VALUES (:id, :user_id, :content, :type, :code, :language, :created_at)""",
            {
                "id": post_id,
                "user_id": user["id"],
                "content": content,
                "type": type,
                "code": code,
                "language": language,
                "created_at": datetime.now(timezone.utc),
            },
        )
        await session.commit()
    return {"id": post_id, "success": True}


@router.post("/comment")
async def create_comment(
    post_id: str,
    content: str,
    user=Depends(get_current_user),
):
    async with get_session() as session:
        # Verify post exists
        count_result = await session.execute(
            select(func.count()).select_from(CommunityPost).where(CommunityPost.id == post_id)
        )
        if count_result.scalar() == 0:
            raise HTTPException(status_code=404, detail="Post not found")

        comment_id = str(user["id"]) + "-" + str(datetime.now().timestamp())
        # Insert community comment
        await session.execute(
            """INSERT INTO community_comments (id, post_id, user_id, content, created_at)
               VALUES (:id, :post_id, :user_id, :content, :created_at)""",
            {
                "id": comment_id,
                "post_id": post_id,
                "user_id": user["id"],
                "content": content,
                "created_at": datetime.now(timezone.utc),
            },
        )
        await session.commit()
    return {"id": comment_id, "success": True}


@router.get("/posts/{post_id}")
async def get_post(post_id: str, user=Depends(get_current_user)):
    async with get_session() as session:
        result = await session.execute(
            select(
                CommunityPost.id,
                CommunityPost.user_id,
                CommunityPost.content,
                CommunityPost.type,
                CommunityPost.code,
                CommunityPost.language,
                CommunityPost.created_at,
            ).where(CommunityPost.id == post_id)
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": row[0],
        "user_id": row[1],
        "content": row[2],
        "type": row[3],
        "code": row[4],
        "language": row[5],
        "likes": 0,
        "liked_by": [],
        "comments": [],
        "created_at": row[6].isoformat() if row[6] else "",
    }