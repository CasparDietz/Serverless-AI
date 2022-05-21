# How to deploy and invoke the code

## Step 1: Port Forwarding
```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```
## Step 2: Build and pusg the Function
```bash
faas-cli up -f flask-service.yml -g http://127.0.0.1:8080
```
## Step 3: Deploy the Function
```bash
faas-cli deploy -f flask-service.yml -g http://127.0.0.1:8080
```
## Step 3: Call the Function
```bash
python3 client.py 
```
- Client cuts the video, provided in the VideoInput folder, into frames
- CLient encodes the frames and creates a json file
- Client performs a POST request to the function

## Step 4: The Server recieves the json file 
- Server converts it back into in image
- Server calls the face detection Python function
- Server calls the face blur Python function
- Server saves the image
- Server encodes the frames and creates a json file
- Server sends back the image with blurred faces as a response, back to the client

# How to inspect the metrics of the running function
```bash
GRAFANA_PORT=$(kubectl -n openfaas get svc grafana -o jsonpath="{.spec.ports[0].nodePort}")
```
```bash
kubectl port-forward pod/grafana 3000:3000 -n openfaas
```
- Now open localhost:3000 in your browser