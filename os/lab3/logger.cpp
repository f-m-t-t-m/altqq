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
			sprintf(s, "%04d-%02d-%02dT%02d:%02d:%02d:%03ld", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec, tp.tv_usec/1000);
			
			return s;
		}
	
};

struct LoggerMeta {
	public:
		LoggerMeta() : main_pid(-1), counter(0) {}
		int	main_pid;
		int	counter;
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


void processCopy1(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) {
	logger->open();
	logger->log("child-1", "starting child 1 process");
	sh_mem->Lock();
	sh_mem->Data()->counter += 10;
	sh_mem->Unlock();
	logger->log("child-1", "exit child 1 process");
	logger->close();

}

void processCopy2(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) {
	logger->open();
	logger->log("child-2", "starting child 2 process");
	sh_mem->Lock();
	sh_mem->Data()->counter *= 2;
	sh_mem->Unlock();

	Thread::Sleep(2.0);

	sh_mem->Lock();
	sh_mem->Data()->counter /= 2;
	sh_mem->Unlock();
	logger->log("child-2", "exit child 2 process");
	logger->close();
}

class LoggerThread : public Thread {
	public:
		LoggerThread(SharedMem<LoggerMeta>* sh_mem, FileLogger* logger) { 
												_mem = sh_mem;
												_logger = logger;
											}
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
				if ((current - lastIncrement)*1000/CLOCKS_PER_SEC >= 300) {
					_mem->Lock();
					_mem->Data()->counter++;
					_mem->Unlock();
					lastIncrement = current;
				}
				if (((current - lastLog)*1000/CLOCKS_PER_SEC) >= 1000 && isMainPid()) {
					_mem->Lock();
					_logger->log(threadName, "Counter: " + std::to_string(_mem->Data()->counter));
					_mem->Unlock();
					lastLog = current;
				}
				if (((current - lastChildrenStart)*1000/CLOCKS_PER_SEC) >= 3000  && isMainPid()) {
					#ifdef _WIN32
					if (child1Pid == -1 || !IsProcessRunning(child1Pid)) {
					#else
					if (!child1IsAlive) {
					#endif
						startChildProcess(1);
						lastChildrenStart = current;
					} else if (child1Pid != -1) {
						_logger->log(threadName, "Can't start child 1 process because its running");
					}
					#ifdef _WIN32
					if (child2Pid == -1 || !IsProcessRunning(child2Pid)) {
					#else
					if (!child2IsAlive) {
					#endif
						startChildProcess(2);
						lastChildrenStart = current;
					} else if (child2Pid != -1)  {
						_logger->log(threadName, "Can't start child 2 process because its running");
					}
				}
				CancelPoint();
			}
		}
		int isMainPid() {
			return _mem->Data()->main_pid == _logger->getPid();
		}
		
	private:
		FileLogger* _logger;
		SharedMem<LoggerMeta>* _mem;
		std::string threadName = "logger-thread";
		int child1Pid = -1;
		int child2Pid = -1;
		bool child1IsAlive = false;
		bool child2IsAlive = false;
		
		void startChildProcess(int childProcessNumber) {
		#ifdef _WIN32
			STARTUPINFO si;     
			PROCESS_INFORMATION pi;
			
			ZeroMemory( &si, sizeof(si) );
			si.cb = sizeof(si);
			ZeroMemory( &pi, sizeof(pi) );
			
			std::string commandLine = "logger.exe " + std::to_string(childProcessNumber);
			
			CreateProcess( NULL,
						   const_cast<char*>(commandLine.c_str()),
						   NULL,
						   NULL,
						   FALSE,
						   0,
						   NULL,
						   NULL,
						   &si,
						   &pi
						);
			if (childProcessNumber == 1) {
				child1Pid = GetProcessId(pi.hProcess);
			} else {
				child2Pid = GsetProcessId(pi.hProcess);
			}
			CloseHandle( pi.hProcess );
			CloseHandle( pi.hThread );
		#else
		int pid = fork();
		if (pid == 0) {
			FileLogger fl;
			if (childProcessNumber == 1) {
				child1IsAlive = true;
				processCopy1(_mem, &fl);
				child1IsAlive = false;
			} else {
				child2IsAlive = true;
				processCopy2(_mem, &fl);
				child2IsAlive = false;
			}
			exit(0);
		} else if (pid > 0) {
			if (childProcessNumber == 1) {
				child1Pid = pid;
			} else {
				child2Pid = pid;
			}
		}
		#endif
		}
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
	
	if (argc == 2) {
		if (strcmp(argv[1],"1") == 0) {
			processCopy1(&loggerMeta, &fl);
		} else if (strcmp(argv[1], "2") == 0) {
			processCopy2(&loggerMeta, &fl);
		}
		return 0;
    }
	
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