FROM ghcr.io/getzola/zola:v0.23.3 AS builder

WORKDIR /site
COPY . .
RUN ["/zola", "build"]

FROM nginx:1.29.1-alpine

COPY --from=builder /site/public /usr/share/nginx/html

EXPOSE 80
