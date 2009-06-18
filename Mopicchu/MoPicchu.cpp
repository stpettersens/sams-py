/*
	MoPicchu stack/queue engine
	Copyright (c) 2008 Samuel Saint-Pettersen
	Released under the MIT License
	Implementation code for MoPicchu Structure engine
*/

#include "MoPicchu.h"
#include "nsStringAPI.h"
#include <cstring>

NS_IMPL_ISUPPORTS1(MoPicchu, IMoPicchu)

// 
// Constructor
//
MoPicchu::MoPicchu() {}

// 
// Destructor
//
MoPicchu::~MoPicchu() {}

//
// Declare Structure class
//
class Structure {
public:
	int i; // Index
	char val[100][50]; // Array holding values
	int size; // Number of values the Structure can store

	Structure() { i = 0; } // Structure constructor; set index to 0
	void defSize(int s) { size = s; } // Define size for Structure
	int retIndex() { return i; } // Return the current index of the Structure
	int retSize() { return size; } // Return size of the Structure
	void drop(const char v[]) { // Drop passed value to selected index on the Structure
		strcpy(&val[i][0], v); 
	} 
	char *pull() { return val[i]; } // Pull value from the current index on the Structure
	void pop() { // Pop (clear) value from the current index on the Structure
		const char v[] = "";
		strcpy(&val[i][0], v);
	} 
};

//
// Declare Stack class
//
class Stack : public Structure {
public:
	void shiftUp() { i++; } // Shift up to next index for next value drop on the Stack
	void shiftDwn() { i--; } // Shift to previous index for next value pull on the Stack
	void setTop() { int top = size - 1; i = top; } // Set index to top of the Stack
};

//
// Declare Queue class
//
class Queue : public Structure {
public:
	void shiftUp() { i++; } // Shift up to next index for next value drop on the Queue
	void shiftDwn() { i++; } // Shift to next index for next value pull on the Queue
	void setTop() { int top = 0; i = top; } // Set index to top of the Queue
};

// 
// Create the Stack or Queue object
//
Stack IStructure;

//
// Define size of the Structure (or return sizes with argument -1/-2) 
//
NS_IMETHODIMP MoPicchu::Define(PRInt32 psize, PRInt32 *_retval) {

	int max = 100; // Define maximum allowable Structure size

	// Define the Structure size if psize > 0 and <= max size
	if(psize > 0 && psize <= max) {
		IStructure.defSize(psize);
	}

	// If invalid size is provided, force maximum allowable size
	else if(psize == 0 || psize > max) IStructure.defSize(max);

	// If argument is -1, return size of the Structure
	else if(psize == -1) *_retval = IStructure.retSize();

	// If argument is -2, return maximum allowable Structure size
	else if(psize == -2) *_retval = max;

    return NS_OK;
}

//
// Drop value onto the Structure (extra drop to indicate end of drops)
//
NS_IMETHODIMP MoPicchu::Drop(const char *pval) {

	// While current Structure index <= Structure size, drop value
	if(IStructure.retIndex() <= (IStructure.retSize() - 1)) { 
		IStructure.drop(pval);
		IStructure.shiftUp();
	}
	// On extra drop, set index to top for pulling
	else if(IStructure.retIndex() > (IStructure.retSize() - 1)) IStructure.setTop(); 

	return NS_OK;
}

//
// Pull value from the Structure
//
NS_IMETHODIMP MoPicchu::Pull(nsACString & _retval) {

	// While current Structure index > -1 and <= Structure size, pull value and decrement index
	if(IStructure.retIndex() > -1 && IStructure.retIndex() <= (IStructure.retSize() - 1)) {
		_retval.Assign(IStructure.pull());
		IStructure.pop();
		IStructure.shiftDwn();
	}
	else _retval.Assign("End"); // Otherwise, return "End"

    return NS_OK;
}

// 
// Reset the Structure
//
NS_IMETHODIMP MoPicchu::Reset() {

	// While incrementer < Structure size, pop current index value and decrement index
	for(int i = 0; i < (IStructure.retSize() - 1); i++) {
		IStructure.pop();
		IStructure.shiftDwn();
	}

    return NS_OK;
}
