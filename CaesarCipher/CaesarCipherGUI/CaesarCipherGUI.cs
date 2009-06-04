//
// Demonstrate the Caesar Cipher library
//
using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace SamsPy {
    static class CaesarCipherGUI {
        // Create new CeasarCipher object
        static CaesarCipher cipher = new CaesarCipher();

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main() {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new FormCaesar());
        }

        /// <summary>
        /// Encrypt the entered text
        /// </summary>
        public static string encrypt(string unencrypted) {
            return cipher.encryptStr(unencrypted);
        }

        /// <summary>
        ///  Decrypt the entered text
        /// </summary>
        public static string decrypt(string encrypted) {
            return cipher.decryptStr(encrypted);
        }
    }
}
