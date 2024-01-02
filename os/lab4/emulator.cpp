#include "my_serial.hpp"
#include <iostream>

#if !defined (WIN32)
#	include <unistd.h>
#	include <time.h>
#endif

void csleep(double timeout) {
#if defined (WIN32)
	if (timeout <= 0.0)
        ::Sleep(INFINITE);
    else
        ::Sleep((DWORD)(timeout * 1e3));
#else
    if (timeout <= 0.0)
        pause();
    else {
        struct timespec t;
        t.tv_sec = (int)timeout;
        t.tv_nsec = (int)((timeout - t.tv_sec)*1e9);
        nanosleep(&t, NULL);
    }
#endif
}

double getTemperature() {
   int randq =  -10 + rand() / (RAND_MAX / (21) + 1);
   return (double) 5 + 0.02 * randq;
}

int main(int argc, char** argv)
{
	srand(time(NULL));
	if (argc < 2) {
		std::cout << "Usage: sertest [port]" << std::endl;
		return -1;
	}

	cplib::SerialPort smport(std::string(argv[1]),cplib::SerialPort::BAUDRATE_115200);
	if (!smport.IsOpen()) {
		std::cout << "Failed to open port '" << argv[1] << "'! Terminating..." << std::endl;
		return -2;
	}
	std::string mystr;
	for (;;) {
		mystr = std::to_string(getTemperature());
		std::cout << mystr << std::endl;
		smport << mystr;
		csleep(1.0);
	}
    return 0;
}