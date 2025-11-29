// JavaScript for PDF Summarizer with custom prompts

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("pdfFile");
    const summaryTypeSelect = document.getElementById("summaryType");
    const customPromptContainer = document.getElementById("customPromptContainer");
    const customPromptInput = document.getElementById("customPrompt");
    const statusText = document.getElementById("status");
    const summaryBox = document.getElementById("summary");

    // Toggle custom prompt visibility based on selection
    summaryTypeSelect.addEventListener("change", (e) => {
        customPromptContainer.style.display = e.target.value === "custom" ? "block" : "none";
        if (e.target.value !== "custom") {
            customPromptInput.value = "";
        }
    });

    // Handle form submission
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        // Reset UI
        summaryBox.textContent = "";
        statusText.textContent = "";
        statusText.className = "status";

        // Validate file
        const file = fileInput.files[0];
        if (!file) {
            showError("Please choose a PDF file first.");
            return;
        }

        // Get form values
        const summaryType = summaryTypeSelect.value;
        const customPrompt = customPromptInput.value.trim();

        // Validate custom prompt if needed
        if (summaryType === "custom" && !customPrompt) {
            showError("Please enter a custom prompt.");
            customPromptInput.focus();
            return;
        }

        // Create FormData object
        const formData = new FormData();
        formData.append("file", file);
        formData.append("prompt_type", summaryType);
        
        // Only append custom_prompt if it's a custom type
        if (summaryType === "custom") {
            formData.append("custom_prompt", customPrompt);
        }

        // Show loading state
        statusText.textContent = "Processing your request...";
        statusText.className = "status processing";

        try {
            // Note: Don't set Content-Type header - the browser will set it with the correct boundary
            const response = await fetch("http://127.0.0.1:8000/summarize", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server responded with status ${response.status}`);
            }

            const data = await response.json();
            
            // Debug log
            console.log("Response data:", data);
            
            if (!data.summary) {
                throw new Error("No summary was returned from the server");
            }

            // Display the result
            summaryBox.innerHTML = formatSummary(data.summary);
            statusText.textContent = "Summary generated successfully!";
            statusText.className = "status success";
        } catch (error) {
            console.error("Error details:", error);
            showError(error.message || "Could not connect to the server. Please try again later.");
        }
    });

    // Helper function to show error messages
    function showError(message) {
        statusText.textContent = message;
        statusText.className = "status error";
    }

    // Helper function to format the summary text (preserving line breaks)
    function formatSummary(text) {
        if (!text) return "No summary available.";
        // Convert newlines to <br> and preserve multiple spaces
        return text
            .replace(/\n/g, '<br>')
            .replace(/  /g, ' &nbsp;');
    }
});
