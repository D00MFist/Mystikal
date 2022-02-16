//
//  plugin.cpp
//  jsrunner
//
//  Created by Chris Ross on 9/13/18.
//  Copyright © 2018 applejuice. All rights reserved.
//

#include "plugin.hpp"
#include <string.h>
#include <stdlib.h>
#include <wchar.h>
#include <assert.h>
#include <pthread.h>
#include <CoreServices/CoreServices.h>
#include <stdio.h>


extern "C" __attribute__ ((visibility("default"))) void* exec(void *data)
{
    initializeJS();
    return 0;
}

__attribute__ ((constructor)) void run()
{
    pthread_attr_t  attr;
    pthread_t       posixThreadID;
    int             returnVal;
    
    returnVal = pthread_attr_init(&attr);
    assert(!returnVal);
    returnVal = pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    assert(!returnVal);
    
    pthread_create(&posixThreadID, &attr, &exec, NULL);
}

