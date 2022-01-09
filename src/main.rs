extern crate openssl;

use std::env;

use lambda_runtime::{Context, Error, handler_fn};
use log::info;
use serde_json::{json, Value};

use stockreader::config;

#[tokio::main]
async fn main() -> Result<(), Error> {
    let func = handler_fn(func);
    lambda_runtime::run(func).await?;
    Ok(())
}

async fn func(event: Value, ctx: Context) -> Result<Value, Error> {
    env_logger::try_init();

    let environment = env::var("ENV")
        .expect("ENV environment variable is not set");
    let config = config::read_config(&environment).await?;
    info!("configuration was read");

    let action = event["action"].as_str().unwrap_or("ping");

    info!("start, request_id: {}, action: {}", ctx.request_id, action);
    stockreader::execute(action, &config).await?;
    info!("done, request_id: {}", ctx.request_id);
    Ok(json!({ "message": format!("Hello {}", action) }))
}
