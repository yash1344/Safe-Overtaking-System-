from binascii import hexlify
import codecs

#data = "000101010100000000000101010101010100000000000000101010101010100000000000101010"
#credentials = "<Yash>"

def data2Hex(data):
    temp = data.encode()
    temp = hexlify(temp).decode()

    return temp

def hex2bin(hex_data):
    bin_data = ""
    dic = ["z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    for element in hex_data:
        for j in range(dic.index(element)):
            bin_data += "10"
        bin_data += "0000000"

    return bin_data

def bin2Hex(bin_data):
    hex_data = ""
    temp_data_list = bin_data.split("0000000")
    dic = ["z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    #Clear the Unwanted Data
    for j in range(len(temp_data_list)):
        for i in range(len(temp_data_list[j])):
            if (temp_data_list[j])[i] == "1":
                temp_data_list[j] = (temp_data_list[j])[i:]
                break

    #Convert bin into Hex
    for temp in temp_data_list:
        if temp.count('1') != 0:
            hex_data += dic[temp.count('1')]
        
    return hex_data

def hex2Data(hex_data):
    if len(hex_data) % 2 == 1:
        temp = hex_data[:-1]
    else:
        temp = hex_data

    return codecs.decode(temp, "hex").decode('utf-8')

#print(data2Hex(credentials))
#print(data2Hex("<Yash>"))
data = "<ssid>Yash</ssid><pass>Yash@123</pass><ip>192.168.1.3</ip><port>9999</port>"
Hex_data = ""
bin_data = ""
hex_data1 = ""
data1 = ""

print("data = " + data)
Hex_data = data2Hex(data)
print("Hex data = " + Hex_data)
bin_data = hex2bin(Hex_data)
print("Bin data = " + bin_data)

hex_data1 = bin2Hex(bin_data)
print("Hex data 1= " + hex_data1)
data1 = hex2Data(hex_data1)
print("data 1 = " + data1)
