cd ..
export $(cat .env_test | xargs);
cargo test
