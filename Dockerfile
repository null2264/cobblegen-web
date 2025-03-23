FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://git.sr.ht/~null2264/cobblegen-web"
LABEL org.opencontainers.image.description="A configurator webapp for CobbleGen (MC) Mod."
LABEL org.opencontainers.image.licenses=GPL-3.0-or-later

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:80", "webapp:app"]