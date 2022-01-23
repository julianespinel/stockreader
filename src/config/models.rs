use serde::{Deserialize, Serialize};

#[derive(Default, Deserialize, Serialize, Clone, Debug)]
pub struct IEXConfig {
    pub api_key: String,
    pub base_url: String,
}

#[derive(Default, Deserialize, Serialize, Debug)]
pub struct DatabaseConfig {
    pub host: String,
    pub username: String,
    pub password: String,
    pub port: u32,
    pub name: String,
}

#[derive(Default, Deserialize, Serialize)]
pub struct Configuration {
    pub iex: IEXConfig,
    pub database: DatabaseConfig,
}

impl DatabaseConfig {

    pub fn get_url(&self) -> String {
        if self.username.is_empty() { panic!("Database username is empty") }
        if self.password.is_empty() { panic!("Database password is empty") }
        if self.host.is_empty() { panic!("Database host is empty") }
        if self.port < 1 { panic!("Database port is < 1") }
        if self.name.is_empty() { panic!("Database name is empty") }
        format!(
            "postgres://{}:{}@{}:{}/{}",
            self.username,
            self.password,
            self.host,
            self.port,
            self.name
        )
    }
}

#[cfg(test)]
mod tests {

//-------------------------------------------------------------------------
// get_database_url tests
//-------------------------------------------------------------------------

    use crate::config::models::DatabaseConfig;

    #[test]
    fn get_database_url_returns_valid_url() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "test_db".to_string(),
        };
        let expected_url = "postgres://username:password@localhost:5432/test_db";
        // act
        let real_url = db_config.get_url();
        // assert
        assert_eq!(expected_url, real_url);
    }

    #[test]
    #[should_panic(expected = "Database password is empty")]
    fn get_database_url_panics_on_empty_password() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "test_db".to_string(),
        };
        // act
        db_config.get_url();
    }

    #[test]
    #[should_panic(expected = "Database port is < 1")]
    fn get_database_url_panics_on_port_less_than_1() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 0,
            name: "test_db".to_string(),
        };
        // act
        db_config.get_url();
    }
}
