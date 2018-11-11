from bluetooth import *
import sys

def h(v):
    return binascii.unhexlify(v)

if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("no device specified.  Searching all nearby bluetooth devices for")
    print("the SampleServer service")
else:
    addr = sys.argv[1]
    print("Searching for SampleServer on %s" % addr)

# SPP
uuid = "00001101-0000-1000-8000-00805F9B34FB"
service_matches = find_service(uuid=uuid, address=addr)

if len(service_matches) == 0:
    print("couldn't find the service")
    sys.exit(1)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock = BluetoothSocket(RFCOMM)
sock.connect((host, port))

# 507 (log record # as shown in Wireshark)
sock.send(b"01234567")

# 508
sock.send(h("01fe0000510210000000008000000080"))
r = sock.recv(16)
assert r == h("01fe000041021000470c000000000000")

# 512
sock.send(h("01fe0000530018000000000000000080e1070b0b112e0a00"))
sock.send(h("01fe0000500a10000000008000000080"))
# This apparently reads current color of the lamp
sock.send(h("01fe0000518210000000000000000000"))
r = sock.recv(16)
print(repr(r))
#assert r == h("01fe00004182100000ff000000000000"), binascii.hexlify(r)

#
# Stuff below, while coded from btsnoop_hci.log, doesn't work -
# good-looking replies are received, but the bulb doesn't change
# the color.
#

# 519
sock.send(h("01fe0000510010000000008000000080"))
r = sock.recv(40)
# Values here can change over time, so don't assert on it
#assert r == h("01fe0000410028000000000000000000001f00160000000500000200000000000007467002100000")
print(repr(r))

sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 528
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 531
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 534
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 537
sock.send(h("01fe0000538310000000ff0000000000"))
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 542
sock.send(h("01fe0000510010000000008000000080"))
sock.send(h("01fe000053831000ff00000000000000"))
print("546", repr(sock.recv(40)))

# 547
sock.send(h("01fe0000510010000000008000000080"))
print("549", repr(sock.recv(40)))

# 555
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 592
sock.send(h("01fe0000510010000000008000000080"))
print(598, repr(sock.recv(40)))

# 599
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

# 602
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))
# 605
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))
# 608
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))
# 614
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))
# 617
sock.send(h("01fe0000510010000000008000000080"))
print(repr(sock.recv(40)))

sock.close()
