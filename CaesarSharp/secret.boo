"""
Demonstrate CaesarSharp library in booish
"""
import CaesarSharp.Cipher
c = CaesarSharp.Cipher()
secret = "Samuel likes fish and chips."
print("The encrypted secret: ${c.encryptStr(secret)}")
print("The decrypted secret: ${secret}")

secret = "Tgkfphq Hbkxe B. Lche muv hak akhypxb pt cpbcqm fqhttpipky!"
print("The encrypted secret: ${secret}")
print("The decrypted secret: ${c.decryptStr(secret)}")

