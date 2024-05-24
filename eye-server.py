#!/usr/bin/env python3

import socket
import cv2
import numpy as np
import sys

PORT = 9999

winname = "esp-eye"
cv2.namedWindow(winname)
cv2.moveWindow(winname, 400, 50) 

def receive_jpeg_image(client_socket):
    image_data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        image_data += packet
    return image_data

def display_image_from_bytes(image_data):
    # Convert the received byte string to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    # Decode the numpy array into an image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow(winname, image)
    c = cv2.waitKey(1)
    if (c == ord('q')):
        sys.exit()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)
    print(f"Listening for TCP connections on port {PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        try:
            image_data = receive_jpeg_image(client_socket)
            display_image_from_bytes(image_data)
        except Exception as e:
            print(f"Error receiving/displaying image: {e}")
            break
        finally:
            client_socket.close()
    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

