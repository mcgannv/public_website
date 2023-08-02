from sqlalchemy import create_engine


def create_and_connect(url):
    """
    Creates the .db files if they don't exist
    :param url: sqlite uri
    """
    engine = create_engine(url)
    with engine.connect() as conn:
        pass
