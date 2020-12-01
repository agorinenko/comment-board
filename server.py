from api.app import create_app


async def app():
    """
    For start gunicorn in production
    :return:
    """
    return create_app()
