from flask import Flask, request, render_template_string
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

STORAGE_ACCOUNT_URL = "https://storageforwebappvikas.blob.core.windows.net/"
CONTAINER_NAME = "containerforwebapp"

html_form = """
    <h2>Upload a File</h2>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file"/>
      <input type="submit" value="Upload"/>
    </form>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        credential = ManagedIdentityCredential()
        blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.upload_blob(file, overwrite=True)
        return f"Uploaded <b>{file.filename}</b> successfully!"

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
