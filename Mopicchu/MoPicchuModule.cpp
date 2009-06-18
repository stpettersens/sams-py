/*
	MoPicchu stack engine
	Copyright (c) 2008 Samuel Saint-Pettersen
	Released under the MIT License
	Module definition for MoPicchu stack engine
*/

#include "nsIGenericFactory.h"
#include "MoPicchu.h"

NS_GENERIC_FACTORY_CONSTRUCTOR(MoPicchu)

static nsModuleComponentInfo components[] = {
	{
		MO_PICCHU_CLASSNAME,
		MO_PICCHU_CID,
		MO_PICCHU_CONTRACTID,
		MoPicchuConstructor,
	}
};

NS_IMPL_NSGETMODULE("MoPicchu", components)
