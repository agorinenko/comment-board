import uuid


async def test_add_comment(client):
    """
    Test add comment response
    :return:
    """
    create_payload = {
        "content": "Hello world!!!!!",
        "userName": "User 1",
        "boardId": str(uuid.uuid4())
    }
    response = await client.post("/api/v1/comments", data=create_payload)
    assert response.status == 200
    json = await response.json()
    assert create_payload['content'] in json['content']
    assert create_payload['userName'] in json['userName']
    assert create_payload['boardId'] in json['boardId']

    assert json['id'] is not None
    assert json['created'] is not None
    assert json['updated'] is None
    assert json['parentId'] is None



async def test_comments_list(client):
    """
    Test comments list response
    :return:
    """
    response = await client.get("/api/v1/comments?limit=20&offset=0")
    assert response.status == 200
    json = await response.json()
    assert "results" in json
    assert "count" in json
