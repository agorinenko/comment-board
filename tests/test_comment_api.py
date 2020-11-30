import uuid
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db.utils import generate_db_url


async def test_add_comment(client):
    """
    Test add comment response
    :return:
    """
    create_parent_json = await create_comment(client)
    parent_id = create_parent_json["id"]

    create_payload = {
        "content": "Hello world!!!!!",
        "userName": "User 1",
        "boardId": str(uuid.uuid4()),
        "parentId": parent_id
    }
    create_response = await client.post("/api/v1/comments", data=create_payload)
    create_json = await create_response.json()
    assert create_response.status == 200

    assert create_payload['content'] == create_json['content']
    assert create_payload['userName'] == create_json['userName']
    assert create_payload['boardId'] == create_json['boardId']
    assert create_payload['parentId'] == create_json['parentId']
    assert create_json['id'] is not None
    assert create_json['created'] is not None
    assert create_json['updated'] is None

    get_response = await client.get(f"/api/v1/comments/{create_json['id']}")
    get_json = await get_response.json()
    assert get_response.status == 200

    assert create_json['content'] == get_json['content']
    assert create_json['userName'] == get_json['userName']
    assert create_json['boardId'] == get_json['boardId']
    assert create_json['parentId'] == get_json['parentId']
    assert get_json['created'] is not None
    assert get_json['updated'] is None


async def test_update_comment(client):
    """
    Test update comment response
    :return:
    """
    create_parent_json = await create_comment(client)
    comment_id = create_parent_json["id"]

    update_payload = {
        "content": "My new content!!!!",
        "userName": "User 2",
    }
    update_response = await client.put(f"/api/v1/comments/{comment_id}", data=update_payload)
    update_json = await update_response.json()
    assert update_response.status == 200

    assert update_payload['content'] == update_json['content']
    assert update_payload['userName'] == update_json['userName']
    assert update_json['id'] is not None
    assert update_json['created'] is not None
    assert update_json['updated'] is not None

    get_response = await client.get(f"/api/v1/comments/{comment_id}")
    get_json = await get_response.json()
    assert get_response.status == 200

    assert update_payload['content'] == get_json['content']
    assert update_payload['userName'] == get_json['userName']

    assert get_json['created'] is not None
    assert get_json['updated'] is not None


async def test_comments_list(client):
    """
    Test comments list response
    :return:
    """

    await delete_all_comments()

    board_id = str(uuid.uuid4())
    for i in range(12):
        await create_comment(client, board_id=board_id)

    limit = 10

    get_response = await client.get(f"/api/v1/comments?boardId={board_id}&limit={limit}&offset=0")
    get_json = await get_response.json()
    assert get_response.status == 200

    assert "results" in get_json
    assert "count" in get_json
    assert get_json["count"] == 12
    assert len(get_json["results"]) == limit


async def test_delete_comment(client):
    """
    Test delete comment response
    :return:
    """

    await delete_all_comments()

    create_json = await create_comment(client)
    comment_id = create_json["id"]

    delete_response = await client.delete(f"/api/v1/comments/{comment_id}")
    assert delete_response.status == 204

    get_response = await client.get(f"/api/v1/comments/{comment_id}")
    assert get_response.status == 404


async def create_comment(client,
                         content: Optional[str] = "Hello world!!!!!",
                         user_name: Optional[str] = "User 1",
                         board_id: Optional[str] = str(uuid.uuid4()),
                         parent_id: Optional[int] = None):
    create_payload = {
        "content": content,
        "userName": user_name,
        "boardId": board_id
    }
    if parent_id is not None:
        create_payload["parentId"] = parent_id

    create_response = await client.post("/api/v1/comments", data=create_payload)
    create_json = await create_response.json()
    assert create_response.status == 200

    return create_json


async def delete_all_comments():
    async with create_async_engine(generate_db_url()).begin() as conn:
        await conn.execute(text("DELETE FROM comments"))
