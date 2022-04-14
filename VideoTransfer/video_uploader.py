import http 
import http.server
import requests
'''
    Take a video and send it via a HTTP request to a given URL.
'''
def post_video(video_path, url):
    # Open the video file
    video_file = open(video_path, "rb")
    # Create a dictionary with the file and the name of the form field
    files = {"form_field_name": video_file}
    # Send the request
    response = requests.post(url, files = files)
    # Close the file
    video_file.close()
    # Check if the request was successful
    new_file=open("response.txt",mode="a+",encoding="utf-8")
    if response.ok:
        new_file.write("Upload completed successfully!\n")        
        new_file.write(response.text)
    else:
        new_file.write("Something went wrong!")
    new_file.close()
        
# Test the function
test_url = "http://httpbin.org/post"        
post_video("sample-video.mp4", test_url)

'''
    Create a function that creates a server that can recieve HTTP requests. Return the URL of the server.
'''
def create_server():
    # Create a server
    server = http.server.HTTPServer(("", 0), http.server.SimpleHTTPRequestHandler)
    # Start the server
    server.serve_forever()
    # Get the URL of the server
    url = "http://localhost:{}".format(server.server_port)
    # Return the URL
    return url
