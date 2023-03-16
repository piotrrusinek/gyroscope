#include <stdlib.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
#include <math.h>  //include libm

#include "mpu6050/mpu6050.h"

#define UART_BAUD_RATE 1000000
#include "uart/uart.h"

//---------UART--------------
/*
void uart_init()
{
	UCSRB = (1<<RXEN)|(1<<TXEN);
	UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0);
	UBRRH = 0;
	UBRRL = 0;
}

void uart_putc(unsigned char data)
{
	UDR = data;
	//while( (UCSRA&(1<<TXC)) == 0 );
	while( (UCSRA&(1<<UDRE)) == 0 );
}

void uart_puts(unsigned char data[])
{
	for(int i=0; data[i]!=NULL;i++)
	{
		uart_putc(data[i]);
	}
}
*/

#define LED 0b00000001

int main(void) {
	DDRB = LED;
	PORTB |= LED;
	

	
	long *ptr = 0;
	double qw = 1.0f;
	double qx = 0.0f;
	double qy = 0.0f;
	double qz = 0.0f;
	double roll = 0.0f;
	double pitch = 0.0f;
	double yaw = 0.0f;
	

	//init uart
	uart_init(UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU)); 

	//init interrupt
	sei();

	//init mpu6050
	mpu6050_init();
	_delay_ms(50);

	
	
	for(;;) {
		

		
		mpu6050_getQuaternion(&qw, &qx, &qy, &qz);
		mpu6050_getRollPitchYaw(&roll, &pitch, &yaw);
		_delay_ms(10);
		
		
		
		ptr = (long *)(&roll);
		uart_putc(*ptr);
		uart_putc(*ptr>>8);
		uart_putc(*ptr>>16);
		uart_putc(*ptr>>24);
		ptr = (long *)(&pitch);
		uart_putc(*ptr);
		uart_putc(*ptr>>8);
		uart_putc(*ptr>>16);
		uart_putc(*ptr>>24);
		ptr = (long *)(&yaw);
		uart_putc(*ptr);
		uart_putc(*ptr>>8);
		uart_putc(*ptr>>16);
		uart_putc(*ptr>>24);
		
		

	}

}
