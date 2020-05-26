/*
******************************************************************************
* @file       USB_SPI_W25Q32.cpp
* @Copyright: ViewTool
* @Revision : ver 1.0
* @Date     : 2014/12/17 17:03
* @brief    : USB_SPI_W25Q32 demo
******************************************************************************
* @attention
*
* Copyright 2009-2014, ViewTool
* http://www.viewtool.com/
* All Rights Reserved
*
******************************************************************************
*/

/*

Hardware Connection
W25Q32      Ginkgo USB-SPI Adapter
1.SI		<-->  SPI_MOSI(Pin17)
2.SCK		<-->  SPI_SCK(Pin13)
3.RESET		<-->  VCC(Pin2)
4.CS		<-->  SPI_SEL0(Pin11)
5.WP	    <-->  VCC(Pin2)
6.VCC	    <-->  VCC(Pin2)
7.GND	    <-->  GND(Pin19/Pin20)
8.SO	    <-->  SPI_MISO(Pin15)

*/


#include "stdafx.h"
#include "ControlSPI.h"
#include "func_map.h"

#define GINKGO_API_EX    1
uint8_t spi_channel[]={
J8_P2_P4_P6_P8_SPI0_NSS0,J8_P2_P4_P6_J50_P4_SPI0_NSS1,J8_P2_P4_P6_J50_P6_SPI0_NSS2,J8_P2_P4_P6_J50_P8_SPI0_NSS3,
J8_P2_P4_P6_J50_P10_SPI0_NSS4,J8_P2_P4_P6_J50_P12_SPI0_NSS5,J8_P2_P4_P6_J50_P14_SPI0_NSS6,J8_P2_P4_P6_J50_P16_SPI0_NSS7,
J8_P1_P3_P5_P7_SPI1_NSS8,J8_P1_P3_P5_J50_P7_SPI1_NSS9,J8_P1_P3_P5_J50_P7_SPI1_NSS10,J8_P1_P3_P5_J50_P7_SPI1_NSS11,
J8_P1_P3_P5_J50_P7_SPI1_NSS12,J8_P1_P3_P5_J50_P7_SPI1_NSS13,J8_P1_P3_P5_J50_P7_SPI1_NSS14,J8_P1_P3_P5_J50_P7_SPI1_NSS15,
};
int _tmain(int argc, _TCHAR* argv[])
{
	int ret, i,j;
	VSI_INIT_CONFIG_EX	SPI_Init;
	uint8_t	WriteDataTemp[512] = { 0 };
	uint8_t	ReadDataTemp[512] = { 0 };
	// Check the device number of connections
	ret = VSI_ScanDevice();
	if (ret > 0) {
		printf("The connected device number is:%d\n", ret);
	}
	else {
		printf("No device to connect!\n");
		return 0;
	}
	// Open Device
	ret = VSI_OpenDevice(VSI_USBSPI, 0, 0);
	if (ret != ERR_SUCCESS) {
		printf("Open device error :%d\n", ret);
		return ret;
	}
	else {
		printf("Open device success!\n");
	}
	for(j=0;j<16;j++)
	{
		// Device initialization
		SPI_Init.ClockSpeed = 1125000;
		SPI_Init.ControlMode = 1;
		SPI_Init.CPHA = 0;
		SPI_Init.CPOL = 0;
		SPI_Init.LSBFirst = 0;
		SPI_Init.MasterMode = 1;
		SPI_Init.SelPolarity = 0;
		SPI_Init.TranBits = 8;
		SPI_Init.SPIIndex = spi_channel[j];
		ret = VSI_InitSPIEx(VSI_USBSPI, 0, &SPI_Init);
		if (ret != ERR_SUCCESS) {
			printf("Initialization device error :%d\n", ret);
			return ret;
		}
		else {
			printf("Initialization device success!\n");
		}
		// JEDEC ID
		WriteDataTemp[0] = 0x9F;
		ret = VSI_WriteReadBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 1, ReadDataTemp, 3);
		if (ret != ERR_SUCCESS) {
			printf("Read flash ID error :%d\n", ret);
			return ret;
		}
		else {
			printf("Flash ID = 0x%06X\n", (ReadDataTemp[0] << 16) | (ReadDataTemp[1] << 8) | (ReadDataTemp[2]));
		}
		// Write Enable
		WriteDataTemp[0] = 0x06;
		ret = VSI_WriteBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 1);
		if (ret != ERR_SUCCESS) {
			printf("Flash write enable error :%d\n", ret);
			return ret;
		}
		else {
			printf("Write enable success!\n");
		}
		// Sector Erase (4KB)
		WriteDataTemp[0] = 0x20;
		WriteDataTemp[1] = 0x00;
		WriteDataTemp[2] = 0x00;
		WriteDataTemp[3] = 0x00;
		ret = VSI_WriteBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 4);
		if (ret != ERR_SUCCESS) {
			printf("Sector Erase start error :%d\n", ret);
			return ret;
		}
		else {
			printf("Sector erase start success!\n");
		}
		// Check the operation to complete
		do {
			WriteDataTemp[0] = 0x05;// Read Status Register-1
			ret = VSI_WriteReadBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 1, ReadDataTemp, 1);

		} while ((ReadDataTemp[0] & 0x01) && (ret == ERR_SUCCESS));
		if (ret != ERR_SUCCESS) {
			printf("Sector Erase error :%d\n", ret);
			return ret;
		}
		else {
			printf("Sector erase success!\n");
		}
		// Write Enable
		WriteDataTemp[0] = 0x06;
		ret = VSI_WriteBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 1);
		if (ret != ERR_SUCCESS) {
			printf("Flash write enable error :%d\n", ret);
			return ret;
		}
		else {
			printf("Write enable success!\n");
		}
		// Page Program
		WriteDataTemp[0] = 0x02;// Page Program command
		WriteDataTemp[1] = 0x00;// Address
		WriteDataTemp[2] = 0x00;
		WriteDataTemp[3] = 0x00;
		for (i = 4; i < (256 + 4); i++) {
			WriteDataTemp[i] = i - 4;
		}
		ret = VSI_WriteBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 256 + 4);
		if (ret != ERR_SUCCESS) {
			printf("Page program start error :%d\n", ret);
			return ret;
		}
		else {
			printf("Page program start success!\n");
		}
		// Check the operation to complete
		do {
			WriteDataTemp[0] = 0x05;// Read Status Register-1
			ret = VSI_WriteReadBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 1, ReadDataTemp, 1);

		} while ((ReadDataTemp[0] & 0x01) && (ret == ERR_SUCCESS));
		if (ret != ERR_SUCCESS) {
			printf("Page program error :%d\n", ret);
			return ret;
		}
		else {
			printf("Page program success!\n");
		}
		// Read Data
		WriteDataTemp[0] = 0x03;//Read Data command
		WriteDataTemp[1] = 0x00;//address
		WriteDataTemp[2] = 0x00;
		WriteDataTemp[3] = 0x00;
		ret = VSI_WriteReadBytes(VSI_USBSPI, 0, SPI_Init.SPIIndex, WriteDataTemp, 4, ReadDataTemp, 256);
		if (ret != ERR_SUCCESS) {
			printf("Read Data error :%d\n", ret);
			return ret;
		}
		else {
			printf("Read Data success\n");
		}
		for (i = 0; i < 256; i++) {
			if ((i % 26) == 0) {
				printf("\n");
			}
			printf("%02X ", ReadDataTemp[i]);
		}
		printf("\n\n");
		system("pause");	
	}
	return 0;
}