FROM postgres:16.2-alpine

ENV POSTGRES_DB=ips
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=1234

EXPOSE 5432