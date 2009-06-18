/*
 * DO NOT EDIT.  THIS FILE IS GENERATED FROM IMoPicchu.idl
 */

#ifndef __gen_IMoPicchu_h__
#define __gen_IMoPicchu_h__


#ifndef __gen_nsISupports_h__
#include "nsISupports.h"
#endif

/* For IDL files that don't want to include root IDL files. */
#ifndef NS_NO_VTABLE
#define NS_NO_VTABLE
#endif

/* starting interface:    IMoPicchu */
#define IMOPICCHU_IID_STR "832a4adf-f123-4e48-b322-e3563b7b1034"

#define IMOPICCHU_IID \
  {0x832a4adf, 0xf123, 0x4e48, \
    { 0xb3, 0x22, 0xe3, 0x56, 0x3b, 0x7b, 0x10, 0x34 }}

class NS_NO_VTABLE IMoPicchu : public nsISupports {
 public: 

  NS_DEFINE_STATIC_IID_ACCESSOR(IMOPICCHU_IID)

  /* long Define (in long psize); */
  NS_IMETHOD Define(PRInt32 psize, PRInt32 *_retval) = 0;

  /* void Drop (in string pval); */
  NS_IMETHOD Drop(const char *pval) = 0;

  /* ACString Pull (); */
  NS_IMETHOD Pull(nsACString & _retval) = 0;

  /* void Reset (); */
  NS_IMETHOD Reset(void) = 0;

};

/* Use this macro when declaring classes that implement this interface. */
#define NS_DECL_IMOPICCHU \
  NS_IMETHOD Define(PRInt32 psize, PRInt32 *_retval); \
  NS_IMETHOD Drop(const char *pval); \
  NS_IMETHOD Pull(nsACString & _retval); \
  NS_IMETHOD Reset(void); 

/* Use this macro to declare functions that forward the behavior of this interface to another object. */
#define NS_FORWARD_IMOPICCHU(_to) \
  NS_IMETHOD Define(PRInt32 psize, PRInt32 *_retval) { return _to Define(psize, _retval); } \
  NS_IMETHOD Drop(const char *pval) { return _to Drop(pval); } \
  NS_IMETHOD Pull(nsACString & _retval) { return _to Pull(_retval); } \
  NS_IMETHOD Reset(void) { return _to Reset(); } 

/* Use this macro to declare functions that forward the behavior of this interface to another object in a safe way. */
#define NS_FORWARD_SAFE_IMOPICCHU(_to) \
  NS_IMETHOD Define(PRInt32 psize, PRInt32 *_retval) { return !_to ? NS_ERROR_NULL_POINTER : _to->Define(psize, _retval); } \
  NS_IMETHOD Drop(const char *pval) { return !_to ? NS_ERROR_NULL_POINTER : _to->Drop(pval); } \
  NS_IMETHOD Pull(nsACString & _retval) { return !_to ? NS_ERROR_NULL_POINTER : _to->Pull(_retval); } \
  NS_IMETHOD Reset(void) { return !_to ? NS_ERROR_NULL_POINTER : _to->Reset(); } 

#if 0
/* Use the code below as a template for the implementation class for this interface. */

/* Header file */
class _MYCLASS_ : public IMoPicchu
{
public:
  NS_DECL_ISUPPORTS
  NS_DECL_IMOPICCHU

  _MYCLASS_();

private:
  ~_MYCLASS_();

protected:
  /* additional members */
};

/* Implementation file */
NS_IMPL_ISUPPORTS1(_MYCLASS_, IMoPicchu)

_MYCLASS_::_MYCLASS_()
{
  /* member initializers and constructor code */
}

_MYCLASS_::~_MYCLASS_()
{
  /* destructor code */
}

/* long Define (in long psize); */
NS_IMETHODIMP _MYCLASS_::Define(PRInt32 psize, PRInt32 *_retval)
{
    return NS_ERROR_NOT_IMPLEMENTED;
}

/* void Drop (in string pval); */
NS_IMETHODIMP _MYCLASS_::Drop(const char *pval)
{
    return NS_ERROR_NOT_IMPLEMENTED;
}

/* ACString Pull (); */
NS_IMETHODIMP _MYCLASS_::Pull(nsACString & _retval)
{
    return NS_ERROR_NOT_IMPLEMENTED;
}

/* void Reset (); */
NS_IMETHODIMP _MYCLASS_::Reset()
{
    return NS_ERROR_NOT_IMPLEMENTED;
}

/* End of implementation class template. */
#endif


#endif /* __gen_IMoPicchu_h__ */
