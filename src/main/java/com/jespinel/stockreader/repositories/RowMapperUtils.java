package com.jespinel.stockreader.repositories;

import java.sql.Date;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;

public class RowMapperUtils {

    static LocalDate getDate(ResultSet resultSet, String key) throws SQLException {
        Date date = resultSet.getDate(key);
        if (date == null) {
            return null;
        }
        return date.toLocalDate();
    }
}
