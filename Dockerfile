# CiteGuard — local citation verifier CLI
# Build:  docker build -t citeguard .
# Demo:   docker run --rm -v "$PWD":/data -w /data citeguard check fixtures/mixed.md --fixtures
# Help:   docker run --rm citeguard --help

FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE requirements.txt ./
COPY citeguard ./citeguard
COPY fixtures ./fixtures
COPY corpus ./corpus

RUN pip install --no-cache-dir .

WORKDIR /data
ENTRYPOINT ["citeguard"]
CMD ["--help"]
