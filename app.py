from flask import Flask, request, render_template
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Set your User-Assigned Managed Identity Client ID (Find it in Azure Portal)
UAMI_CLIENT_ID = "47cefc22-e8b0-4e1f-9a68-4c1d4c8ed62a"

# Authenticate using Managed Identity
credential = ManagedIdentityCredential(client_id=UAMI_CLIENT_ID)

# Storage Account Configuration
STORAGE_ACCOUNT_NAME = "storageforwebappvikas"
CONTAINER_NAME = "containerforwebapp"

# Connect to Azure Storage Blob using UAMI
blob_service_client = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=credential
)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    try:
        # Upload file to Azure Storage using Managed Identity
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)
        return f"File '{file.filename}' uploaded successfully to Azure Storage!"
    
    except Exception as e:
        return f"Upload failed: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
