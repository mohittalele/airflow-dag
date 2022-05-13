import hashlib
import sys
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

resmd5 = md5("./validation-data/yoda.jpg")
print("calculated checksum is ", resmd5)
checksum = "2624daf668b78c8f72c9895318d9703e"
print("expected checsum is" , checksum)
if resmd5 == checksum :
    print( "Checksum matched" )
    sys.exit(0)
else :
    sys.exit(1)