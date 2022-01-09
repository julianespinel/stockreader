use std::env;

pub fn get_env_variable(variable_name: &str) -> String {
    env::var(variable_name)
        .expect(&format!("{} environment variable is not set", variable_name))
}
