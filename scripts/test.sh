cd ..
export $(cat .env | xargs);
cargo test
