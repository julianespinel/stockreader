cd ..
alias rust-musl-builder='docker run --rm -it -v "$(pwd)":/home/rust/src -v cargo-git:/home/rust/.cargo/git -v cargo-registry:/home/rust/.cargo/registry ekidd/rust-musl-builder'
rust-musl-builder sudo chown -R rust:rust /home/rust/.cargo/git /home/rust/.cargo/registry
rust-musl-builder cargo build --release --target x86_64-unknown-linux-musl
cp target/x86_64-unknown-linux-musl/release/stockreader bootstrap
zip lambda.zip bootstrap
rm bootstrap
