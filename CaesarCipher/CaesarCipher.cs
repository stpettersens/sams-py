/*
    CaesarCipher
    Version 1.0

    A simple .NET library to encrypt and decrypt
    sensitive strings with a simple Ceasar/Cicero cipher

    Copyright (c) 2009 Sam Saint-Pettersen
    Released under the MIT License
    
    WARNING: Do not use this library to encrypt highly
    sensitive information. It is hardly Blowfish or AES-256!
    It is just designed to make text less obvious.
    I will probably make improvements here in the future.
*/
using System;
using System.Collections.Generic;
using System.Text;

namespace SamsPy {

    public class CaesarCipher {

        private char[] keys = { 
        'h', 'z', 'f', 'y', 'k', 'i', 'b', 'c', 'p', 'n', 'o', 'q', 'd', 'x', 'u', 'g', 
        's', 'a', 't', 'e', 'v', 'j', 'l', 'w', 'm', 'r',
        'H', 'Z', 'F', 'Y', 'K', 'I', 'B', 'C', 'P', 'N', 'O', 'Q', 'D', 'X', 'U', 'G', 
        'S', 'A', 'T', 'E', 'V', 'J', 'L', 'W', 'M', 'R', 
        '1', '5', '6', '9', '7', '3', '2', '4', '0', '8' 
        };
        private char[] vals = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        };

        private Dictionary<char, char> caesar = new Dictionary<char, char>();
        private Dictionary<char, char> cicero = new Dictionary<char, char>();
        public CaesarCipher() { // Populate Caesar and Cicero dictionaries on initialization
            int i = 0;
            foreach(char v in vals) {
                caesar.Add(v, keys[i]);
                i += 1;
            }
            i = 0;
            foreach(char k in keys) {
                cicero.Add(k, vals[i]);
                i += 1;
            }
        }

        // Caesar encrypts
        private char getKey(char val) {
            return caesar[val];
        }

        // Cicero decrypts
        private char getVal(char key) {
            return cicero[key];
        }

        /// <summary>
        /// Encrypt a string using Caesar's dictionary
        /// </summary>
        /// <param name="unencrypted">String to encrypt</param>
        /// <returns>Encypted string</returns>
        public string encryptStr(string unencrypted) {
            string encrypted = null;
            foreach(char ch in unencrypted) {
                // Only encrypt characters where there exists 
                // a replacement cipher key
                if(caesar.ContainsKey(ch)) encrypted += getKey(ch);
                else encrypted += ch;
            }
            return encrypted;
        }

        /// <summary>
        /// Decrypt a string using Cicero's dictionary
        /// </summary>
        /// <param name="encrypted">String to decrypt</param>
        /// <returns>Decrypted string</returns>
        public string decryptStr(string encrypted) {
            string decrypted = null;
            foreach(char ch in encrypted) {
                // Only decrypt existing cipher keys
                if(cicero.ContainsKey(ch)) decrypted += getVal(ch);
                else decrypted += ch;
            }
            return decrypted;
        }
    }
}
