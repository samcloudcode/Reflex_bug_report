import reflex as rx


class TestsConfig(rx.Config):
    pass


config = TestsConfig(
    app_name="tests",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)