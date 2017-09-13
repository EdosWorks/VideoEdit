#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

FILE *fp;
FILE *fpout;

int height = 720;
int width = 1280;
int height2 = height+height/2;
const int frame_size = height2 * width;
char *buffer = (char*)malloc( sizeof(char) * (frame_size + 1) );
char *outbuffer = (char*)malloc( sizeof(char) * (frame_size + 1) );

fp = fopen("<<name_of_input_file>>.yuv","rb");
fpout = fopen("<<name_of_output_file>>.yuv","wb");
unsigned int frame_number = 0;

if(fp)
{
	while( fp != NULL )
	{
		int read = 0;
		read = fread(buffer, 1, frame_size, fp);
		if( read == frame_size )
		{
			frame_number++;
			buffer[frame_size] = '\0';
			read = 0;
			//Mat src =  Mat(height2,width, CV_8UC1, buffer); // create opencv mat object
			// some function call
			//mat object 'src' modified in function call
			if(src.data != NULL)
			{
				outbuffer = src.data;
			}
			if(fpout != NULL)
			{
				fwrite(outbuffer,1,frame_size,fpout);
			}
		}
		else
		{
			break;
		}
	}
}
else
{
	printf("\nError in opening file. Exiting...\n");
	exit(0);
}