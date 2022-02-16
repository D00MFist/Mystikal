/*******
* NAME:   dlopen.c
* AUTHOR: Clif Flynt
* DATE:   10/3/2002
* DESC:   Loads a shared library without requiring an xx_Init
*         function for the Tcl interpreter.
*         This supports extensions that may require other
*         shared libraries being resident before they are
*         loaded.
*
* CALL:   From Tcl:
*         dlopen /full/path/library.EXT
*
* PARAMETERS: 
*         path:  A full path to the shared object, .dll or .so
*
************/

static char *cpy="This code Copyright 2002 to Clif Flynt";

/***********************************************************
# This code is written and copyrighted by Clif Flynt, 2002
#
# It is licenced for public use with these terms:
#
#  This licence agreement must remain intact with the code.
# 
#  You may use this code freely for non-commercial purposes.
#
#  You may examine and modify the code to your heart's content.
#
#  You may not claim to have authored the code (aside from 
#  modifications you may have made.)
#
#  You may not distribute the code without this license agreement
#
#  You may not sell this code or distribute it with a commercial product
#      without arrangements with Noumena Corporation.
#
#  Maintenance, extension, modification, etc can be performed by:
#
#   Noumena Corporation
#   9300 Fleming Rd.
#   Dexter, MI  48130
#
#   Contact: clif@noucorp.com
#
# $Header$
****************************************************************/

#include <stdio.h>
#if defined (_WIN32)
#include <windows.h>
#else
#include <dlfcn.h>
#endif
#include <tcl.h>

Tcl_HashTable *dlopen_hashtablePtr;
extern int dummyDebugPrint;

void dlopen_InitHashTable () {
    dlopen_hashtablePtr = (Tcl_HashTable *) ckalloc(sizeof(Tcl_HashTable));
    Tcl_InitHashTable(dlopen_hashtablePtr, TCL_STRING_KEYS);
}
  

static int
dlOpen(ClientData x, Tcl_Interp* interp, int objc, Tcl_Obj*CONST* objv)
{
	char hash_handle[50];
        char *tmp;
        void *handle;
        Tcl_HashEntry *hashEntryPtr;
        Tcl_Obj *returnObjPtr;
	int isNew;


        if (objc > 1)
        {
            tmp = Tcl_GetStringFromObj(objv[1], NULL);
	    #if defined (_WIN32)
	        handle = LoadLibrary(tmp);
	    #else
                handle = dlopen(tmp, RTLD_NOW | RTLD_GLOBAL);
	    #endif

            if (!handle) {
                      fprintf(stderr, "FAIL IN DLOPEN: %s\n", tmp);
	    #if defined (_WIN32)
                      fprintf (stderr, "%s\n", "Is there a windows errro fcn");
	    #else
                      fprintf (stderr, "%s\n", dlerror());
	    #endif
                      return(TCL_ERROR);
                  }
	    
        } else {
          Tcl_WrongNumArgs(interp, 1, objv,
              "path-to-library");

                      return(TCL_ERROR);
	}

    /*
     * Allocate the space and initialize the return structure.
     */

    sprintf(hash_handle, "X%x", handle);
    
    hashEntryPtr = Tcl_CreateHashEntry(dlopen_hashtablePtr, hash_handle, &isNew);
    Tcl_SetHashValue(hashEntryPtr, handle);

    returnObjPtr = Tcl_NewStringObj(hash_handle, -1);  
    
    Tcl_SetObjResult(interp, returnObjPtr);

    return TCL_OK;
}

__getfpucw() {printf("hit getfpucw\n"); fflush(stdout);}


#if defined (_WIN32)

static int
dlSym(ClientData x, Tcl_Interp* interp, int objc, Tcl_Obj*CONST* objv) {

     Tcl_Obj *returnObjPtr;

     returnObjPtr = Tcl_NewStringObj("dlSym not implemented for Windows", -1);  
    
     Tcl_SetObjResult(interp, returnObjPtr);
    return TCL_OK;
}

#else

static int
dlSym(ClientData x, Tcl_Interp* interp, int objc, Tcl_Obj*CONST* objv)
{
	char *hash_handle;
        char *tmp;
        void *handle;
        Tcl_HashEntry *hashEntryPtr;
        Tcl_Obj *returnObjPtr;
	void *locat;
	char rtnString[20];


        if (objc > 1)
        {
            hash_handle = Tcl_GetStringFromObj(objv[1], NULL);
            hashEntryPtr = Tcl_FindHashEntry(dlopen_hashtablePtr, hash_handle);
            if (hashEntryPtr == (Tcl_HashEntry *) NULL) {
        char errString[80];
        Tcl_Obj *errCodePtr;
     
        /*
         * Define an error code from an integer, and set errorCode.
         */
        errCodePtr = Tcl_NewIntObj(554);
        Tcl_SetObjErrorCode(interp, errCodePtr);

        /*
         * This string will be placed in the global variable errorInfo
         */
     
        sprintf(errString, "Hash object \"%s\" does not exist.", hash_handle);
        Tcl_AddErrorInfo(interp, errString);
         
        /* 
         * This string will be returned as the result of the command.
         */
        Tcl_AppendResult(interp, "can not find hashed object named \"",
                hash_handle, "\"", (char *) NULL);
        return TCL_ERROR;
	    }
	    
	handle = (char *)Tcl_GetHashValue(hashEntryPtr);

	tmp = Tcl_GetStringFromObj(objv[2], NULL);
	
	locat = dlsym(handle, tmp);
	
	sprintf(rtnString, "%x", locat);
	
        }

    /*
     * Allocate the space and initialize the return structure.
     */

    
     returnObjPtr = Tcl_NewStringObj(rtnString, -1);  
    
     Tcl_SetObjResult(interp, returnObjPtr);

	return TCL_OK;
}
#endif

#if defined (_WIN32)

    #define WINEXPORT(t) __declspec(dllexport) t
#elif defined (_WIN)
    #define WINEXPORT(t) t _export
#else
    #define WINEXPORT(t) t
#endif

#if defined (__MWERKS__)
    #pragma export on
#endif


WINEXPORT(int) Dlopen_Init(Tcl_Interp* interp)
{
	Tcl_CreateObjCommand(interp, "dlopen", dlOpen, 0, 0);
	Tcl_CreateObjCommand(interp, "dlsym", dlSym, 0, 0);

	dlopen_InitHashTable ();

	Tcl_PkgProvide(interp, "dlopen", "1.0");

	return TCL_OK;
}

WINEXPORT(int) Dlopen_SafeInit(Tcl_Interp* interp)
{
	return Dlopen_Init(interp);
}
