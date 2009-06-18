/*
	MoPicchu stack engine
	Copyright (c) 2008 Samuel Saint-Pettersen
	Released under the MIT License
	Header file for MoPicchu stack engine
*/


#ifndef _MO_PICCHU_H_
#define _MO_PICCHU_H_

#include "IMoPicchu.h"

#define MO_PICCHU_CONTRACTID "@mopicchu.googlecode.com/MoPicchu;1"
#define MO_PICCHU_CLASSNAME "Stack engine for Mozilla"
#define MO_PICCHU_CID { 0xdc6741a9, 0xf202, 0x4b45, { 0x9d, 0xde, 0x3a, 0x2f, 0xa9, 0x5c, 0x6c, 0xe0 } }

class MoPicchu : public IMoPicchu
{
public:
  NS_DECL_ISUPPORTS
  NS_DECL_IMOPICCHU

  MoPicchu();

private:
  ~MoPicchu();
};

#endif
