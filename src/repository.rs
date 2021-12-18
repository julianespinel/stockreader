use csv::Writer;
use crate::models::Symbol;

pub fn write_to_csv(symbols: Vec<Symbol>) -> Result<(), csv::Error> {
    let mut writer = Writer::from_path("symbols.csv")?;
    for (i, symbol) in symbols.iter().enumerate() {
        writer.write_record([&symbol.symbol, &symbol.name])?;
        if i % 100 == 0 { writer.flush()? }
    }
    writer.flush()?;
    Ok(())
}
