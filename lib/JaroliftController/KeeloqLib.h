/*
  Keeloq.h - Crypto library
  Written by Frank Kienast in November, 2010

  This implementations might be useful if you are playing around with [Microchip
  Keeloq](http://www.microchip.com/pagehandler/en-us/technology/embeddedsecurity/technology/keeloqencoderdl.html) chips. I verified that this
  algorithm gives the same results as that produced by the Microchip SDK for several test cases. The Keeloq algorithm is not patented. However, since
  Microchip does hold a patent on its application to secure keyless entry, it probably would not be wise to make a commercial secure keyless entry
  product using this algorithm in a non-Microchip processor. Personal experimentation should be okay.

*/
#pragma once

#include <Arduino.h>

class Keeloq {
public:
  Keeloq(const unsigned long keyHigh, const unsigned long keyLow);

  unsigned long encrypt(const unsigned long data);
  unsigned long decrypt(const unsigned long data);

private:
  unsigned long _keyHigh;
  unsigned long _keyLow;
};

