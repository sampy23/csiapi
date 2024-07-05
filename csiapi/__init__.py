import clr

# pythonnet clr-loader import of Marshal ~ ETABS API requirement \
#                               (for interacting with managed memory and convert between managed and unmanaged memory).
clr.AddReference(r"System.Runtime.InteropServices")
from System.Runtime.InteropServices import Marshal

# pythonnet clr-loader try import of ETABS API DLL (ETABSv1.dll)
etabs_api_path = r'C:\Program Files\Computers and Structures\ETABS 21\ETABSv1.dll'
clr.AddReference(etabs_api_path)