#include <stdio.h>
#include<map>

#include <iostream>         /* std::cout */
#include <string>           /* std::string */
#include <sstream>          /* std::stringbuf */  

#include <stdlib.h>         /* atoi */
#include <string.h>         /* memset */

#if defined (WIN32)
#   include <winsock2.h>    /* socket */
#   include <ws2tcpip.h>    /* ipv6 */
#else
#   include <sys/socket.h>  /* socket */
#   include <netinet/in.h>  /* socket */
#   include <arpa/inet.h>   /* socket */
#   include <unistd.h>      
#	include <poll.h>
#	include <signal.h>
#   define SOCKET int
#   define INVALID_SOCKET -1
#   define SOCKET_ERROR -1
#endif
#include <mysql.h>
#define READ_WAIT_MS 50

class SocketWorker
{
public:
    SocketWorker():m_socket(INVALID_SOCKET) {}
    ~SocketWorker() { CloseMySocket(); }
    /// Возвращает код ошибки
    static int ErrorCode()
    {
#if defined (WIN32)
        return WSAGetLastError();
#else
        return errno;
#endif
    }
protected:
    void CloseMySocket()
    {
        CloseSocket(m_socket);
        m_socket = INVALID_SOCKET;
    }
    void CloseSocket(SOCKET sock)
    {
        if (sock == INVALID_SOCKET)
            return;
#if defined (WIN32)
        shutdown(sock, SD_SEND);
        closesocket(sock);
#else
        shutdown(sock, SHUT_WR);
        close(sock);
#endif
    }
    SOCKET m_socket;
};

class Request {
	public:
		std::string http_method;
		std::string URL;
		std::map<std::string, std::string> query_params;
		
		Request(char *request) {
			char* header = strtok(request, "\n");
			char* token = strtok(header, " ");
			http_method = token;
			char *path = strtok(NULL, " ");
			URL = strtok(path, "?");
			char* query_string = strtok(NULL, "?");
			if (query_string != NULL) {
				char *query_param;
				char *query_param_save;
				
				query_param = strtok_r(query_string, "&", &query_param_save);
				while (query_param != NULL) {
					char* key = strtok(query_param, "=");
					char* val = strtok(NULL, "=");
					query_params.insert(std::make_pair(key, val));
					query_param = strtok_r(NULL, "&", &query_param_save);
				}
			}
	}
};

char* getCurrentTemperature() {
	MYSQL *con = mysql_init(NULL);
	if (mysql_real_connect(con, "localhost", "root", "admin", "temperature", 0, NULL, 0) == NULL) {
		fprintf(stderr, "%s\n", mysql_error(con));
		mysql_close(con);
	};
	if (mysql_query(con, "SELECT * FROM current_temp where id=(SELECT max(id) from current_temp)")) {
		fprintf(stderr, "%s\n", mysql_error(con));
		mysql_close(con);
	};
	MYSQL_RES *result = mysql_store_result(con);
	MYSQL_ROW row = mysql_fetch_row(result);
	
	mysql_close(con);
	return row[2];
}

MYSQL_TIME mapStringToMySqlTime(const char *datetime) {
	MYSQL_TIME ts;
	sscanf(datetime ,"%02d.%02d.%04d,%%20%02d:%02d:%02d", &ts.day, &ts.month, &ts.year, &ts.hour, &ts.minute, &ts.second);
	ts.second_part = 0;
	return ts;
}

std::string timeToIsoString(MYSQL_TIME tm) {
	char *s = (char*) malloc (sizeof (char) * 64);
	sprintf(s, "%04d-%02d-%02d %02d:%02d:%02d", tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second);
	
	return std::string(s);
}

std::string getTemperatureForPeriod(const char* table_name, std::string start, std::string end) {
	MYSQL *con = mysql_init(NULL);
	if (mysql_real_connect(con, "localhost", "root", "admin", "temperature", 0, NULL, 0) == NULL) {
		fprintf(stderr, "%s\n", mysql_error(con));
		mysql_close(con);
	};
	MYSQL_STMT *stmt = mysql_stmt_init(con);
	std::map<const char *, const char *> prepared_statements;
	prepared_statements["current_temp"] = "SELECT * FROM current_temp WHERE date >= ? and date <= ?";
	prepared_statements["avg_hour_temp"] = "SELECT * FROM avg_hour_temp WHERE date >= ? and date <= ?";
	prepared_statements["avg_day_temp"] = "SELECT * FROM avg_day_temp WHERE date >= ? and date <= ?";
	if (mysql_stmt_prepare(stmt, prepared_statements.at(table_name), strlen(prepared_statements.at(table_name)))) {
		std::cout << mysql_stmt_error(stmt) << std::endl;
	}
	
	MYSQL_BIND bind[2];
	memset(bind,0,sizeof(MYSQL_BIND)*2);  
	MYSQL_TIME  start_ts = mapStringToMySqlTime(start.c_str());
	MYSQL_TIME  end_ts = mapStringToMySqlTime(end.c_str());	
	
	std::cout << start_ts.day << " " << start_ts.hour << " " << start_ts.minute << std::endl; 
	
	bind[0].buffer_type= MYSQL_TYPE_DATETIME;
	bind[0].buffer= (char *)&start_ts;
	bind[0].is_null= 0;
	bind[0].length= 0;
	
	bind[1].buffer_type= MYSQL_TYPE_DATETIME;
	bind[1].buffer= (char *)&end_ts;
	bind[1].is_null= 0;
	bind[1].length= 0;
	mysql_stmt_bind_param(stmt, bind);
		
	int id;
	MYSQL_TIME ts;
	double temp;
	MYSQL_BIND res_bind[3];
	memset(res_bind,0,sizeof(MYSQL_BIND)*3);  
	res_bind[0].buffer_type = MYSQL_TYPE_LONG; 
    res_bind[0].buffer = (char *)&id;
	res_bind[1].buffer_length = 10;
    res_bind[0].is_null = 0; 
	res_bind[0].length = 0; 

    res_bind[1].buffer_type = MYSQL_TYPE_DATETIME; 
    res_bind[1].buffer = (char *)&ts;; 
    res_bind[1].buffer_length = 100;
    res_bind[1].is_null = 0; 
    res_bind[1].length = 0; 

    res_bind[2].buffer_type = MYSQL_TYPE_DOUBLE; 
    res_bind[2].buffer = (char *)&temp; 
    res_bind[2].buffer_length = 100;
    res_bind[2].is_null = 0;
    res_bind[2].length = 0; 
	mysql_stmt_bind_result(stmt, res_bind);
	mysql_stmt_store_result(stmt);
	
	MYSQL_RES* prepare_meta_result = mysql_stmt_result_metadata(stmt);
	if (!prepare_meta_result) {
	  fprintf(stderr,
			 " mysql_stmt_result_metadata(), \
			   returned no meta information\n");
	  fprintf(stderr, " %s\n", mysql_stmt_error(stmt));
	  exit(0);
	}
	
	std::stringstream response;
	mysql_stmt_execute(stmt);
	std::cout << mysql_stmt_error(stmt) << std::endl;
	response << "[";
	while(1) {
        int result = mysql_stmt_fetch(stmt); 
        if (result == MYSQL_NO_DATA){
            printf("there is not data any more\n");
            break; 
        }
        if (result != 0){
            printf("error happened while fetch data error code is:%d\n", result);
            printf("error str is %s \n", mysql_error(con));
            break; 
        }
        
        response << "{\"date\": " << "\"" << timeToIsoString(ts) << "\"" << "," << "\"temp\": " << temp << "},"; 
    }
	response.seekp(-1, response.cur);
	response << "]";
	mysql_stmt_close(stmt);
	mysql_close(con);
	return response.str().length() > 1 ? response.str() : "";
}


class HTTPServer: public SocketWorker {
public:
	// Регистрируем сокет на прослушку подключения
    SOCKET Listen(const std::string& interface_ip, short int port)
    {
        // Создаем сокет ipv4
        m_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (m_socket == INVALID_SOCKET) {
            std::cout << "Cant open socket: " << ErrorCode() << std::endl;
            return INVALID_SOCKET;
        }
        // Биндим сокет на адрес и порт
        sockaddr_in local_addr;
        memset(&local_addr, 0, sizeof(local_addr));
        local_addr.sin_family = AF_INET;
        local_addr.sin_addr.s_addr = inet_addr(interface_ip.c_str());
        local_addr.sin_port = htons(port);
        if (bind(m_socket, (struct sockaddr*)&local_addr, sizeof(local_addr))) {
            std::cout << "Failed to bind: " << ErrorCode() << std::endl;
            CloseMySocket();
            return INVALID_SOCKET;
        }
        // Запускаем прослушку на сокете
        if (listen(m_socket, SOMAXCONN)) {
            std::cout << "Failed to start listen: " << ErrorCode() << std::endl;
            CloseMySocket();
            return INVALID_SOCKET;
        }
        return m_socket;
    }
	// Обработаем подключение клиента (браузера), возвращая ему строку с железки
    void ProcessClient(const char* device_str)
    {
        // Принимаем входящие соединения
        SOCKET client_socket = accept(m_socket, NULL, NULL);
        if (client_socket == INVALID_SOCKET) {
            std::cout << "Error accepting client: " << ErrorCode() << std::endl;
            CloseSocket(client_socket);
            return;
        }
        // Хочет ли клиент с нами говорить?
		// (современные браузеры могу открыть два подключения сразу)
        struct pollfd polstr;
        memset(&polstr, 0, sizeof(polstr));
        polstr.fd = client_socket;
        polstr.events |= POLLIN;
#ifdef WIN32
        int ret = WSAPoll(&polstr, 1, READ_WAIT_MS);
#else
        int ret = poll(&polstr, 1, READ_WAIT_MS);
#endif
		// Не хочет - закрываем сокет
        if (ret <= 0) {
            CloseSocket(client_socket);
            return;
        }
        // Прочитаем, что клиент нам сказал (блокирующий вызов!!)
        int result = recv(client_socket, m_input_buf, sizeof(m_input_buf), 0);
        if (result == SOCKET_ERROR) {
            std::cout << "Error on client receive: " << result << std::endl;
            CloseSocket(client_socket);
            return;
        } else if (result == 0) {
            std::cout << "Client closed connection before getting any data!" << std::endl;
            CloseSocket(client_socket);
            return;
        }
		Request req(m_input_buf);
		std::cout << req.URL << std::endl;
		std::string response;
		if (req.http_method != "GET") {
			response = methodNotAllowedResponse;
		} else {
			if (req.URL == "/current-temp") {
				response = handleCurrentTempRequest();
			}
			if (req.URL == "/temp-for-period") {
				if (!requestWithPeriodIsCorrect(req)) {
					response = badRequestResponse;
				} else {
					std::string start = req.query_params.at("start");
					std::string end = req.query_params.at("end");
					response = handleTempForPeriodRequest("current_temp", start, end);
				}
			}
			if (req.URL == "/temp-for-period/avg-hour") {
				if (!requestWithPeriodIsCorrect(req)) {
					response = badRequestResponse;
				} else {
					std::string start = req.query_params.at("start");
					std::string end = req.query_params.at("end");
					response = handleTempForPeriodRequest("avg_hour_temp", start, end);
				}
			}
			if (req.URL == "/temp-for-period/avg-day") {
				if (!requestWithPeriodIsCorrect(req)) {
					response = badRequestResponse;
				} else {
					std::string start = req.query_params.at("start");
					std::string end = req.query_params.at("end");
					response = handleTempForPeriodRequest("avg_day_temp", start, end);
				}
			}	
		}

        // Отправляем ответ клиенту
        result = send(client_socket, response.c_str(), (int)response.length(), 0);
        if (result == SOCKET_ERROR) {
            // произошла ошибка при отправке данных
            std::cout << "Failed to send response to client: " << ErrorCode() << std::endl;
        }
        // Закрываем соединение к клиентом
        CloseSocket(client_socket);
        std::cout << "Answered to client!" << std::endl;
    }
private:
	// Буфер для чтения запроса браузера
    char   m_input_buf[1024];
	std::string badRequestResponse = "HTTP/1.0 400 Bad Request\r\nVersion: HTTP/1.1\r\n\r\n";
	std::string methodNotAllowedResponse = "HTTP/1.0 405 Method Not Allowed\r\nVersion: HTTP/1.1\r\n\r\n";
	
	std::string handleCurrentTempRequest() {
        std::stringstream response;
        std::stringstream response_body;
		response_body << "{\"currentTemp\": " << getCurrentTemperature() << "}";
		std::cout << response_body.str() << std::endl;
        response << "HTTP/1.0 200 OK\r\n"
                 << "Version: HTTP/1.1\r\n"
                 << "Content-Type: application/json; charset=utf-8\r\n"
				 << "Access-Control-Allow-Origin: *\r\n"
                 << "Content-Length: " << response_body.str().length()
                 << "\r\n\r\n"
                 << response_body.str();
		 
		return response.str();
	}
	
	std::string handleTempForPeriodRequest(const char* table_name, std::string start, std::string end) {
        std::stringstream response;
        std::stringstream response_body;
		response_body << getTemperatureForPeriod(table_name, start, end);
		std::cout << response_body.str() << std::endl;
        response << "HTTP/1.0 200 OK\r\n"
                 << "Version: HTTP/1.1\r\n"
                 << "Content-Type: application/json; charset=utf-8\r\n"
				 << "Access-Control-Allow-Origin: *\r\n"
                 << "Content-Length: " << response_body.str().length()
                 << "\r\n\r\n"
                 << response_body.str();
		 
		return response.str();
	}
	
	bool requestWithPeriodIsCorrect(Request request) {
		return request.query_params.count("start") > 0 && request.query_params.count("end") > 0;
	}
	
};

int exit_with_error(MYSQL *con) {
	fprintf(stderr, "%s\n", mysql_error(con));
	mysql_close(con);
	exit(1);
}

MYSQL *init_db() {
	MYSQL *con = mysql_init(NULL);
	MYSQL *create_con = mysql_init(NULL);		
	if (mysql_real_connect(create_con, "localhost", "root", "admin",
		  NULL, 0, NULL, 0) == NULL) {
		exit_with_error(create_con);
	}
	if (mysql_query(create_con, "CREATE DATABASE temperature")) {
		exit_with_error(create_con);
	}
	mysql_real_connect(con, "localhost", "root", "admin",
	  "temperature", 0, NULL, 0);
	mysql_query(con, "CREATE TABLE current_temp(id INT PRIMARY KEY AUTO_INCREMENT, date DATETIME, temp DOUBLE)");
	mysql_query(con, "CREATE TABLE avg_hour_temp(id INT PRIMARY KEY AUTO_INCREMENT, date DATETIME, temp DOUBLE)");
	mysql_query(con, "CREATE TABLE avg_day_temp(id INT PRIMARY KEY AUTO_INCREMENT, date DATETIME, temp DOUBLE)");
	return con;
}

int main(int argc, char **argv) {	
// Инициализируем библиотеку сокетов (под Windows)
#if defined (WIN32)
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);
#else
    // Игнорируем SIGPIPE сигнал
    // чтобы программа не терминировалась при попытке записи в закрытый сокет
    signal(SIGPIPE, SIG_IGN);
#endif
	HTTPServer srv;
	SOCKET server_socket = srv.Listen("127.0.0.1", 80);
	if (server_socket == INVALID_SOCKET) {
        std::cout << "Terminating..." << std::endl;
#if defined (WIN32)
        WSACleanup();
#endif
        return -1;
    }
	struct pollfd polstr[1];
    memset(polstr, 0, sizeof(polstr));
    polstr[0].fd = server_socket;
    polstr[0].events |= POLLIN;
	
	for (;;) {
        int ret = 0;
#ifdef WIN32
        ret = WSAPoll(polstr, 1, -1);
#else
        ret = poll(polstr, 1, -1);
#endif
        // Ошибка сокета
        if (ret <= 0) {
            std::cout << "Error on poll: " << SocketWorker::ErrorCode() << std::endl;
            continue;
        }
        // Проверяем полученные события
        if (polstr[0].revents & POLLIN) {
            // Есть HTTP-клиент - возвращаем ему страницу
            srv.ProcessClient("123");
        }
    }
	
	exit(0);
}