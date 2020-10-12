# Encoding and decoding GPS coordinates

## Methodology

The GPS.py provides an payload encoder and decoder for use on the sending and receiving device respectively. It uses the coordinates for the center of Sheffield and submits the difference between it and the coordinates of the point being transmitted. Therefore, it can accurately send the coordinates using only three bytes. One for absolute longitude difference, one for absolute latitude difference, and one for an identifier of their respectives signs (+/-).


