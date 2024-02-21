opcode = {
    "MOV": {
        "byte": 1,
        "A,A": "7F",
        "A,B": "78",
        "A,C": "79",
        "A,D": "7A",
        "A,E": "7B",
        "A,H": "7C",
        "A,L": "7D",
        "A,M": "7E",
        "B,A": "47",
        "B,B": "40",
        "B,C": "41",
        "B,D": "42",
        "B,E": "43",
        "B,H": "44",
        "B,L": "45",
        "B,M": "46",
        "C,A": "4F",
        "C,B": "48",
        "C,C": "49",
        "C,D": "4A",
        "C,E": "4B",
        "C,H": "4C",
        "C,L": "4D",
        "C,M": "4E",
        "D,A": "57",
        "D,B": "50",
        "D,C": "51",
        "D,D": "52",
        "D,E": "53",
        "D,H": "54",
        "D,L": "55",
        "D,M": "56",
        "E,A": "5F",
        "E,B": "58",
        "E,C": "59",
        "E,D": "5A",
        "E,E": "5B",
        "E,H": "5C",
        "E,L": "5D",
        "E,M": "5E",
        "H,A": "67",
        "H,B": "60",
        "H,C": "61",
        "H,D": "62",
        "H,E": "63",
        "H,H": "64",
        "H,L": "65",
        "H,M": "66",
        "L,A": "6F",
        "L,B": "68",
        "L,C": "69",
        "L,D": "6A",
        "L,E": "6B",
        "L,H": "6C",
        "L,L": "6D",
        "L,M": "6E",
        "M,A": "77",
        "M,B": "70",
        "M,C": "71",
        "M,D": "72",
        "M,E": "73",
        "M,H": "74",
        "M,L": "75",
    },
     "MVI": {
        "byte": 2,
        "B": "06",
        "C": "0E",
        "D": "16",
        "E": "1E",
        "H": "26",
        "L": "2E",
        "M": "36",
        "A": "3E"
    },
    "LXI": {
        "byte":3,
        "B": "01",
        "D": "11",
        "H": "21",
        "SP":"31"
    },
    "XCHG":{
        "byte":1,
        "op":"EB"
    },
    "LDAX":{
        "byte":1,
        "B":"0A",
        "D":"1A"
    },
    "LHLD":{
        "byte":3,
        "op":"2A"
    },
    "LDA":{
        "byte":3,
        "op":"3A"
    },
    "STAX":{
        "byte":1,
        "B":"02",
        "D":"12",
    },
    "SHLD":{
        "byte":3,
        "op":"22"
    },
    "STA":{
        "byte":3,
        "op":"32"
    },
    "ADD":{
        "byte": 1,
        "A": "87",
        "B": "80",
        "C": "81",
        "D": "82",
        "E": "83",
        "H": "84",
        "L": "85",
        "M": "86"  
    },
    "ADC":{
        "byte":1,
        "A": "8F",
        "B": "88",
        "C": "89",
        "D": "8A",
        "E": "8B",
        "H": "8C",
        "L": "8D",
        "M": "8E",
    },
    "SUB":{
        "byte":1,
        "A": "97",
        "B": "90",
        "C": "91",
        "D": "92",
        "E": "93",
        "H": "94",
        "L": "95",
        "M": "96",
    },
    "SBB": {
        "byte": 1,
        "A": "9F",
        "B": "98",
        "C": "99",
        "D": "9A",
        "E": "9B",
        "H": "9C",
        "L": "9D",
        "M": "9E",
    },
    "DAD":{
        "byte": 1,
        "B": "09",
        "D": "19",
        "H": "29",
        "SP": "39"    
    },
    "INR":{
        "byte": 1,
        "A": "3C",
        "B": "04",
        "C": "0C",
        "D": "14",
        "E": "1C",
        "H": "24",
        "L": "2C",
        "M": "34"
    },
    "INX":{
        "byte":1,
        "B": "03",
        "D": "13",
        "H": "23",
        "SP": "33"
    },
    "DCR":{
        "byte":1,
        "A": "3D",
        "B": "05",
        "C": "0D",
        "D": "15",
        "E": "1D",
        "H": "25",
        "L": "2D",
        "M": "35"
    },
     "DCX": {
        "byte": 1,
        "B": "0B",
        "D": "1B",
        "H": "2B",
        "SP": "3B"
    },
     "ANA": {
        "byte": 1,
        "A": "A7",
        "B": "A0",
        "C": "A1",
        "D": "A2",
        "E": "A3",
        "H": "A4",
        "L": "A5",
        "M": "A6"
    },
      "XRA": {
        "byte": 1,
        "A": "AF",
        "B": "A8",
        "C": "A9",
        "D": "AA",
        "E": "AB",
        "H": "AC",
        "L": "AD",
        "M": "AE"
    },
    "ORA": {
        "byte": 1,
        "A": "B7",
        "B": "B0",
        "C": "B1",
        "D": "B2",
        "E": "B3",
        "H": "B4",
        "L": "B5",
        "M": "B6"
    },
    "CMP": {
        "byte": 1,
        "A": "BF",
        "B": "B8",
        "C": "B9",
        "D": "BA",
        "E": "BB",
        "H": "BC",
        "L": "BD",
        "M": "BE"
    },
    "RLC": {
        "byte": 1,
        "op": "07"
    },
    "RRC": {
        "byte": 1,
        "op": "0F"
    },
    "RAL": {
        "byte": 1,
        "op": "17"
    },
    "RAR": {
        "byte": 1,
        "op": "1F"
    },
    "ADI": {
        "byte": 2,
        "op": "C6"
    },
    "ACI": {
        "byte": 2,
        "op": "CE"
    },
    "SUI": {
        "byte": 2,
        "op": "D6"
    },
    "SBI": {
        "byte": 2,
        "op": "DE"
    },
    "ANI": {
        "byte": 2,
        "op": "E6"
    },
    "XRI": {
        "byte": 2,
        "op": "EE"
    },
    "ORI": {
        "byte": 2,
        "op": "F6"
        },
    "CPI": {
        "byte": 2,
        "op": "FE"
    },

    "IN": {
        "byte": 2,
        "op": "DB"
    },
    "OUT": {
        "byte": 2,
        "op": "D3"
    },
    "JMP": {
        "byte": 3,
        "op": "C3"
    },
    "JNZ": {
        "byte": 3,
        "op": "C2"
    },
    "JZ": {
        "byte": 3,
        "op": "CA"
    },
    "JNC": {
        "byte": 3,
        "op": "D2"
    },
    "JC": {
        "byte": 3,
        "op": "DA"
    },
    "JPO": {
        "byte": 3,
        "op": "E2"
    },
    "JPE": {
        "byte": 3,
        "op": "EA"
    },
    "JP": {
        "byte": 3,
        "op": "F2"
    },
    "JM": {
        "byte": 3,
        "op": "FA"
    },
    "XTHL": {
        "byte": 1,
        "op": "E3"
    },
    "SPHL": {
        "byte": 1,
        "op": "F9"
    },
    "PUSH": {
        "byte": 1,
        "B": "C5",
        "D": "D5",
        "H": "E5",
        "PSW": "F5"
    },
    "POP": {
        "byte": 1,
        "B": "C1",
        "D": "D1",
        "H": "E1",
        "PSW": "F1"
    },
    "HLT": {
        "byte": 1,
        "op": "76"
    } 
}