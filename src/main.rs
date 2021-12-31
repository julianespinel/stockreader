use anyhow::Result;
use log4rs;
use log::info;

#[tokio::main]
async fn main() -> Result<()> {
    log4rs::init_file("log4rs.yaml", Default::default())
        .expect("Could not initialize log4rs logger");
    info!("start");
    stockreader::download_symbols("config-dev.toml").await?;
    info!("done");
    Ok(())
}
