#include "my_thread.hpp"
#include "my_shmem.hpp"
#include <iostream>
#include <string>
#include <time.h>
#include <sys/time.h>

using namespace cplib;

class FileLogger {
	public:
		FileLogger() {}
		virtual ~FileLogger() {}
		
		void log(std::string threadName, std::string message) {
			AutoMutex mt(_mut);
			fprintf(_log, "[%s] [%5d-%15s] - %s\n", getLocalTime(), getPid(), threadName.c_str(), message.c_str());
			fflush(_log);
		}
		
		int open() {
			_log = fopen("log.txt","a+");
			if (!_log) {
				return 1;
			}
			return 0;
		}
		
		void close() {
			fclose(_log);
		}
		
		int getPid() {
			#ifdef _WIN32
				return GetCurrentProcessId(); 
			#else
				return getpid();
			#endif
		}

	private:
		Mutex       _mut;
		FILE*		_log;
		
		char* getLocalTime() {
			timeval tp;
			gettimeofday(&tp, 0);
			time_t t = tp.tv_sec;
			struct tm *tm = localtime(&t); 
			char *s = (char*) malloc (sizeof (char) * 64);
			sprintf(s, "%04d-%02d-%02dT%02d:%02d:%02d:%03d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec, tp.tv_usec/1000);
			
			return s;
		}
	
};

struct LoggerMeta {
	public:
		LoggerMeta() : main_pid(-1), counter(0) {}
		int	main_pid;
		int	counter;
};

class LoggerChildThread1 : public Thread {
	public:
		LoggerChildThread1(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) :_mem(sh_mem), _logger(logger) {}
		virtual int MainStart() {
			_logger->log(threadName, "starting child 1 thread");
			return 0;
		}
		virtual void MainQuit() {
			_logger->log(threadName, "exit child 1 thread");
		}
		virtual void Main() {
			_mem->Lock();
			_mem->Data()->counter += 10;
			_mem->Unlock();
		}
	private:
		SharedMem<LoggerMeta>* _mem;
		FileLogger* _logger;
		std::string threadName = "logger-child-1";
};

class LoggerChildThread2 : public Thread {
	public:
		LoggerChildThread2(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) :_mem(sh_mem), _logger(logger) {}
		virtual int MainStart() {
			_logger->log(threadName, "starting child 2 thread");
			return 0;
		}
		virtual void MainQuit() {
			_logger->log(threadName, "exit child 2 thread");
		}
		virtual void Main() {
			_mem->Lock();
			_mem->Data()->counter *= 2;
			_mem->Unlock();
			Sleep(2);
			_mem->Lock();
			_mem->Data()->counter /= 2;
			_mem->Unlock();
		}
	private:
		SharedMem<LoggerMeta>* _mem;
		FileLogger* _logger;
		std::string threadName = "logger-child-2";
};

int IsProcessRunning(int pid) {
	#ifdef _WIN32
		HANDLE process = OpenProcess(SYNCHRONIZE, FALSE, pid);
		DWORD ret = WaitForSingleObject(process, 0);
		CloseHandle(process);
		return ret == WAIT_TIMEOUT;
	#else
		return !kill(pid, 0);
	#endif
}

class LoggerThread : public Thread {
	public:
		LoggerThread(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) :_mem(sh_mem), _logger(logger), 
											child1Thread(LoggerChildThread1(sh_mem, logger)),
											child2Thread(LoggerChildThread2(sh_mem, logger)) { }
		virtual int MainStart() {
			int ret = 0;
			ret = _logger->open();
			return ret;
		}
		virtual void MainQuit() {
			_logger->close();
		}
		virtual void Main() {
			if (isMainPid()) {
				_logger->log(threadName, "Main thread started");
			}
			clock_t lastIncrement = clock();
			clock_t lastLog = clock();
			clock_t lastChildrenStart = clock();
			while (true) {
				_mem->Lock();
				if (!IsProcessRunning(_mem->Data()->main_pid)) {
					_mem->Data()->main_pid = _logger->getPid();
				};
				_mem->Unlock();
				clock_t current = clock();
				if ((current - lastIncrement)*1000/CLK_TCK >= 300) {
					_mem->Lock();
					_mem->Data()->counter++;
					_mem->Unlock();
					lastIncrement = current;
				}
				if (((current - lastLog)*1000/CLK_TCK) >= 1000 && isMainPid()) {
					_mem->Lock();
					_logger->log(threadName, "Counter: " + std::to_string(_mem->Data()->counter));
					_mem->Unlock();
					lastLog = current;
				}
				if (((current - lastChildrenStart)*1000/CLK_TCK) >= 3000  && isMainPid()) {
					if (child1Thread.ThreadState() == STATE_STOPPED) {
						child1Thread.Start();
						lastChildrenStart = current;
					} else {
						_logger->log(threadName, "Can't start child 1 thread because its running");
					}
					if (child2Thread.ThreadState() == STATE_STOPPED) {
						child2Thread.Start();
						lastChildrenStart = current;
					} else {
						_logger->log(threadName, "Can't start child 2 thread because its running");
					}
				}
				CancelPoint();
				//Sleep(0.05);
			}
		}
		int isMainPid() {
			return _mem->Data()->main_pid == _logger->getPid();
		}
		
	private:
		FileLogger* _logger;
		SharedMem<LoggerMeta>* _mem;
		LoggerChildThread1 child1Thread;
		LoggerChildThread2 child2Thread;
		bool _isMainPid;
		std::string threadName = "logger-thread";
};

int main (int argc, char** argv) {
	SharedMem<LoggerMeta> loggerMeta("logger_meta");
	if (!loggerMeta.IsValid()) {
        std::cout << "Failed to create shared memory block!" << std::endl;
        return -1;
    }
	
	FileLogger fl;
	loggerMeta.Lock();
	if (loggerMeta.Data()->main_pid == -1) {
		loggerMeta.Data()->main_pid = fl.getPid();
	}
	loggerMeta.Unlock();
	LoggerThread loggerThread(&loggerMeta, &fl);
	loggerThread.Start();
	loggerThread.WaitStartup();
	
	int counter;
	while (true) {
		std::cout << "Enter counter value: ";
		std::cin >> counter;
		loggerMeta.Lock();
		loggerMeta.Data()->counter = counter;
		loggerMeta.Unlock();
	}
	loggerThread.Stop();
}