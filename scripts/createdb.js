var connection = new Mongo();
var db = connection.getDB("stockboarddb");
db.stocklist.createIndex({ quote: 1 }, { unique: true });
db.stocks_current_data.createIndex({ symbol: 1 }, { unique: true });
