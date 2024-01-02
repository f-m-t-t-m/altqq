#include "my_serial.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <sstream> 
#include <iostream>
#include <time.h>
#include <string.h>
#include <mysql.h>
#include<map>


struct tm getLocalTime() {
	time_t t = time(NULL);
	struct tm* tm = localtime(&t); 
	return *tm;
}

int daysInMonth(int month, int year) {
    if ( month > 12 || month < 1 ) return 0;

    if (month == 4 || month == 6 || month == 9 || month == 11) return 30;
    else if (month == 2) return (((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) ? 29 : 28);
    return 31;
}

MYSQL_TIME map_tm_to_ts(struct tm* datetime) {
	MYSQL_TIME  ts;
	ts.year = datetime->tm_year+1900;
	ts.month = datetime -> tm_mon+1;
	ts.day = datetime->tm_mday;
	
	ts.hour = datetime->tm_hour;
	ts.minute = datetime->tm_min;
	ts.second = datetime->tm_sec;
	
	return ts;
}

int insert_temp(MYSQL* con, const char* table_name, const char* temp) {
	char format[] = "INSERT INTO %s VALUES(NULL, NOW(), %s)";
	char sql[1000];
	sprintf(sql, format, table_name, temp);
	return mysql_query(con, sql);
}

int delete_rows_that_older_than_given_seconds(MYSQL* con, const char* table_name, int seconds) {
	MYSQL_STMT *stmt = mysql_stmt_init(con);
	std::map<const char *, const char *> prepared_statements;
	prepared_statements["current_temp"] = "DELETE FROM current_temp WHERE date < (DATE_SUB(NOW(), INTERVAL ? SECOND))";
	prepared_statements["avg_hour_temp"] = "DELETE FROM avg_hour_temp WHERE date < (DATE_SUB(NOW(), INTERVAL ? SECOND))";
	prepared_statements["avg_day_temp"] = "DELETE FROM avg_day_temp WHERE date < (DATE_SUB(NOW(), INTERVAL ? SECOND))";
	if (mysql_stmt_prepare(stmt, prepared_statements.at(table_name), strlen(prepared_statements.at(table_name)))) {
		std::cout << mysql_stmt_error(stmt) << std::endl;
	}
	
	MYSQL_BIND bind[1];
	bind[0].buffer_type= MYSQL_TYPE_LONG;
	bind[0].buffer= &seconds;
	bind[0].is_null= 0;
	bind[0].length= 0;
	mysql_stmt_bind_param(stmt, bind);
	
	return mysql_stmt_execute(stmt);
}

int calculate_avg_hour_temp(MYSQL* con) {
	const char* sql = "INSERT INTO avg_hour_temp(id, date, temp) SELECT 0 as id, NOW() as date, AVG(temp) as temp FROM current_temp ct WHERE ct.date >= DATE_SUB(NOW(), INTERVAL 1 HOUR)";
	return mysql_query(con, sql);
}

int calculate_avg_day_temp(MYSQL* con) {
	const char* sql = "INSERT INTO avg_day_temp(id, date, temp) SELECT 0 as id, NOW() as date, AVG(temp) as temp FROM current_temp ct WHERE ct.date >= DATE_SUB(NOW(), INTERVAL 1 DAY)";
	return mysql_query(con, sql);
}

int main(int argc, char** argv)
{
	if (argc < 2) {
		std::cout << "Usage: sertest [port]" << std::endl;
		return -1;
	}
	
	cplib::SerialPort smport(std::string(argv[1]),cplib::SerialPort::BAUDRATE_115200);
	if (!smport.IsOpen()) {
		std::cout << "Failed to open port '" << argv[1] << "'! Terminating..." << std::endl;
		return -2;
	}
	struct tm tm = getLocalTime();
	int startHour = tm.tm_hour;
	int startDay = tm.tm_mday;
	std::string mystr;
	smport.SetTimeout(1.0);
	MYSQL *con = mysql_init(NULL);
	if (mysql_real_connect(con, "localhost", "root", "admin",
          "temperature", 0, NULL, 0) == NULL) {
			fprintf(stderr, "%s\n", mysql_error(con));
			mysql_close(con);
			exit(1);
	}
	for (;;) {
		smport >> mystr;
		if (atof(mystr.c_str())) {
			struct tm now = getLocalTime();
			if (now.tm_hour > startHour || now.tm_hour == 0 && startHour == 23) {
				std::cout << "evaluating avg hour temp" << std::endl;
				int month_in_seconds = daysInMonth(now.tm_mday, now.tm_year) * 60 * 60 * 24;
				delete_rows_that_older_than_given_seconds(con, "avg_hour_temp", month_in_seconds);
				calculate_avg_hour_temp(con);
				startHour = now.tm_hour;
			}
			if (now.tm_mday > startDay || now.tm_mday == 1 && startDay == daysInMonth(now.tm_mon, now.tm_year+1900)) {
				std::cout << "evaluating avg day temp" << std::endl;
				int year_in_seconds = 365 * 60 * 60 * 24;
				delete_rows_that_older_than_given_seconds(con, "avg_day_temp", year_in_seconds);
				calculate_avg_day_temp(con);
				startDay = now.tm_mday;
			}
			int day_in_seconds = 60*60*24;
			delete_rows_that_older_than_given_seconds(con, "current_temp", day_in_seconds);
			if (insert_temp(con, "current_temp", mystr.c_str())) {
				fprintf(stderr, "%s\n", mysql_error(con));
			}
		}
	}
	
	mysql_close(con);
    return 0;
}