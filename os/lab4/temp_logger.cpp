#include "my_serial.hpp"
#include <sstream> 
#include <iostream>
#include <time.h>


struct tm getLocalTime() {
	time_t t = time(NULL);
	struct tm* tm = localtime(&t); 
	return *tm;
}

std::string timeToIsoString(struct tm* tm) {
	char *s = (char*) malloc (sizeof (char) * 64);
	sprintf(s, "%04d-%02d-%02dT%02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
	
	return std::string(s);
}

double calculateAvgTempForNLastSeconds(int n, struct tm *now, std::string path) {
	double tempCount = 0;
	int dayCount = 0;
	
	FILE* f = fopen(path.c_str(), "r");
	int year = 0;
	int month = 0;
	int day = 0;
	int hour = 0;
	int min = 0;
	int sec = 0;
	double temp = 0;
	while (fscanf(f,"%04d-%02d-%02dT%02d:%02d:%02d %f",&year, &month, &day, &hour, &min, &sec, &temp) != EOF) { 
		struct tm current;
		current.tm_year = year - 1900;
		current.tm_mon = month - 1;
		current.tm_mday = day;
		current.tm_hour = hour;
		current.tm_min = min;
		current.tm_sec = sec;
		current.tm_isdst = -1;
		time_t t = mktime(&current);
		if (difftime(mktime(now), t) < n) {
			tempCount += temp;
			++dayCount;
		}
	}
	fclose(f);
	return tempCount / dayCount;
}

int getNumberOfRowsToRemove(struct tm *now, double secDiffToDelete, std::string path) {
	FILE* f = fopen(path.c_str(), "r");
	int firstRowsToRemove = 0;
	int year = 0;
	int month = 0;
	int day = 0;
	int hour = 0;
	int min = 0;
	int sec = 0;
	double temp = 0;
	while (fscanf(f,"%04d-%02d-%02dT%02d:%02d:%02d %f",&year, &month, &day, &hour, &min, &sec, &temp) != EOF) {
		struct tm current;
		current.tm_year = year - 1900;
		current.tm_mon = month - 1;
		current.tm_mday = day;
		current.tm_hour = hour;
		current.tm_min = min;
		current.tm_sec = sec;
		current.tm_isdst = -1;
		
		time_t t = mktime(&current);
		if (difftime(mktime(now), t) > secDiffToDelete) {
			++firstRowsToRemove;
		} else {
			break;
		}
	}
	fclose(f);
	return firstRowsToRemove;
}

void deleteFirstNRowsFromFile(int n, std::string path) {
	FILE* f = fopen(path.c_str(), "r");
	FILE* tmp = fopen("tmp.txt", "w");
	char line[30];
	
	int skippedLines = 0;
	while (fgets(line, sizeof line, f) != NULL) {
		if (skippedLines == n) {
			fprintf(tmp, "%s", line);
		} else {
			++skippedLines;
		}
	}
	fclose(f);
	fclose(tmp);
	std::cout << "clearing file" << std::endl;
	remove(path.c_str());
	rename("tmp.txt", path.c_str());
	std::cout << "removed lines: " << n << std::endl;
}

int daysInMonth(int month, int year) {
    if ( month > 12 || month < 1 ) return 0;

    if (month == 4 || month == 6 || month == 9 || month == 11) return 30;
    else if (month == 2) return (((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) ? 29 : 28);
    return 31;
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
	for (;;) {
		smport >> mystr;
		if (mystr.size() == 8) {
			struct tm now = getLocalTime();
			if (now.tm_hour > startHour || now.tm_hour == 0 && startHour == 23) {
				std::cout << "evaluating avg hour temp" << std::endl;
				int monthDurationInSeconds = daysInMonth(now.tm_mday, now.tm_year) * 24 * 60 * 60 ;
				int rowsToRemove = getNumberOfRowsToRemove(&now, monthDurationInSeconds, "hourlyAvgLog.txt");
				if (rowsToRemove > 0) {
					deleteFirstNRowsFromFile(rowsToRemove, "hourlyAvgLog.txt");
				}
				double avgHourTemp = calculateAvgTempForNLastSeconds(60 * 60,  &now, "log.txt");
				FILE* hourlyAvgLog = fopen("hourlyAvgLog.txt","a+");
				std::string str =  timeToIsoString(&now) + " " + std::to_string(avgHourTemp) + "\n";
				fprintf(hourlyAvgLog, "%s", str.c_str());
				fclose(hourlyAvgLog);
				startHour = now.tm_hour;
			}
			if (now.tm_mday > startDay || now.tm_mday == 1 && startDay == daysInMonth(now.tm_mon, now.tm_year+1900)) {
				std::cout << "evaluating avg day temp" << std::endl;
				int yearDurationInSeconds = 365 * 24 * 60 * 60;
				int rowsToRemove = getNumberOfRowsToRemove(&now, yearDurationInSeconds, "dailyAvgLog.txt");
				if (rowsToRemove > 0) {
					deleteFirstNRowsFromFile(rowsToRemove, "dailyAvgLog.txt");
				}
				double avgDayTemp = calculateAvgTempForNLastSeconds(24 * 60 * 60,  &now, "hourlyAvgLog.txt");
				FILE* dailyAvgLog = fopen("dailyAvgLog.txt","a+");
				std::string str = timeToIsoString(&now) + " " + std::to_string(avgDayTemp) + "\n";
				fprintf(dailyAvgLog, "%s", str.c_str());
				fclose(dailyAvgLog);
				startDay = now.tm_mday;
			}
			int rowsToRemove = getNumberOfRowsToRemove(&now, 24 * 60 * 60, "log.txt");
			if (rowsToRemove > 0) {
				deleteFirstNRowsFromFile(rowsToRemove, "log.txt");
			}
			mystr = timeToIsoString(&now) + " " + mystr + "\n";
			FILE* log = fopen("log.txt","a+");
			fprintf(log, "%s", mystr.c_str());
			fclose(log);
		}
	}
	
    return 0;
}