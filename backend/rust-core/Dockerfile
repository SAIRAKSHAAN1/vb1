FROM rust:1.70 as builder

WORKDIR /usr/src/vector-db
COPY . .

RUN cargo build --release

FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y libssl1.1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/vector-db/target/release/vector-db-core /usr/local/bin/vector-db-core

EXPOSE 8001

CMD ["vector-db-core"] 