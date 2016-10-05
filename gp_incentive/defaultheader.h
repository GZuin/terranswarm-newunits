#ifndef __MAIN_H__
#define __MAIN_H__

#include <windows.h>


#define DLL_EXPORT __declspec(dllexport)

extern "C"
{
    float DLL_EXPORT incentiveExp(float a, float b, float c, float d, float e, float f, float g, float h, float i);
}

#endif // __MAIN_H__
