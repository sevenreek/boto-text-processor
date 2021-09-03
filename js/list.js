var SELECTED_FILES = new Set();
console.log("Hello world!");

function selectFile(filename) {
    if (SELECTED_FILES.has(filename))
        SELECTED_FILES.delete(filename);
    else
        SELECTED_FILES.add(filename)
}

function startProcess() {
    const feedback = document.getElementById("processFeedback")
    const feedbackText = document.getElementById("processFeedbackText");
    if (SELECTED_FILES.size == 0) {
        feedback.classList.remove("d-none");
        feedback.classList.remove("text-success", "text-danger", "text-info");
        feedback.classList.add("text-info");
        feedbackText.innerHTML = "❓ Select something first.";
        return;
    }
    var data = JSON.stringify([...SELECTED_FILES]);
    fetch("/process", { // Your POST endpoint
        method: 'POST',
        body: data
    }).then(response => {
        feedback.classList.remove("d-none");
        feedback.classList.remove("text-success", "text-danger", "text-info");
        if (response.ok) {
            feedback.classList.add("text-success");
            feedbackText.innerHTML = "✔️ Processing requested. Refresh the page to see progress.";
        } else {
            feedback.classList.add("text-danger");
            feedbackText.innerHTML = "❌ Request failed.";
        }
    })
}

function fileUploadChanged(self) {
    console.log(self);
    if (self.files.length) {
        document.getElementById("uploadButton").disabled = false;
    } else {
        document.getElementById("uploadButton").disabled = true;
    }
}

function startUpload() {
    const feedbackElement = document.getElementById("uploadFeedback");
    const feedbackText = document.getElementById("uploadFeedbackText");
    const feedbackSpinner = document.getElementById("uploadSpinner");
    feedbackElement.classList.remove('d-none');
    feedbackText.innerHTML = "Uploading...";
    feedbackElement.classList.remove("text-danger", "text-warning", "text-secondary", "text-success");
    feedbackElement.classList.add("text-secondary");
    feedbackSpinner.classList.remove('d-none');
    fetch('/upload')
        .then(presignResponse => {
            if (presignResponse.ok)
                return presignResponse.json();
            else {
                feedbackText.innerHTML = "Failed to fetch upload URL.";
                feedbackElement.classList.remove("text-danger", "text-warning", "text-secondary", "text-success");
                feedbackElement.classList.add("text-danger");
                feedbackSpinner.classList.add('d-none');
                throw new Error("Did not receive presigned URL from server.");
            }
        })
        .then(presignedPostData => {
            console.log(presignedPostData);
            file = document.getElementById("fileToUpload").files[0];
            var formData = new FormData();
            Object.keys(presignedPostData.fields).forEach(key => {
                formData.append(key, presignedPostData.fields[key]);
            });
            // Actual file has to be appended last.
            formData.append("file", file);
            fetch(presignedPostData.url, { // Your POST endpoint
                    method: 'POST',
                    /*headers: {
                        // Content-Type may need to be completely **omitted**
                        // or you may need something
                        "Content-Type": "You will perhaps need to define a content-type here"
                    },*/
                    body: formData
                })
                .then(
                    response => {
                        if (response.ok) {
                            feedbackText.innerHTML = `${file.name} uploaded`;
                            feedbackElement.classList.remove("text-danger", "text-warning", "text-secondary", "text-success");
                            feedbackElement.classList.add("text-success");
                            feedbackSpinner.classList.add('d-none');
                            document.getElementById("fileToUpload").value = "";
                            document.getElementById("uploadButton").disabled = true;
                        }
                    }
                )
        })
}